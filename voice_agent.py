from flask import Blueprint, request, jsonify
from src.models.lead import Lead, Call, SalesPlaybook, db
from datetime import datetime
import os
import json
import requests
import openai
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

voice_agent_bp = Blueprint('voice_agent', __name__)

# Initialize Twilio client
twilio_client = Client(
    os.getenv('TWILIO_ACCOUNT_SID', 'demo_sid'),
    os.getenv('TWILIO_AUTH_TOKEN', 'demo_token')
)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

@voice_agent_bp.route('/voice/initiate-call', methods=['POST'])
def initiate_call():
    """Initiate an outbound call to a lead"""
    try:
        data = request.get_json()
        lead_id = data.get('lead_id')
        
        if not lead_id:
            return jsonify({'error': 'Lead ID is required'}), 400
        
        lead = Lead.query.get_or_404(lead_id)
        
        # Create call record
        call = Call(
            lead_id=lead_id,
            status='initiated'
        )
        db.session.add(call)
        db.session.commit()
        
        # In a real implementation, this would initiate a Twilio call
        # For demo purposes, we'll simulate the call initiation
        if os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_ACCOUNT_SID') != 'demo_sid':
            try:
                twilio_call = twilio_client.calls.create(
                    to=lead.phone,
                    from_=os.getenv('TWILIO_PHONE_NUMBER'),
                    url=f"{request.host_url}api/voice/webhook/{call.id}",
                    record=True
                )
                call.call_sid = twilio_call.sid
                call.status = 'in_progress'
                db.session.commit()
                
                return jsonify({
                    'call_id': call.id,
                    'call_sid': twilio_call.sid,
                    'status': 'initiated',
                    'message': 'Call initiated successfully'
                })
            except Exception as e:
                call.status = 'failed'
                call.notes = f"Twilio error: {str(e)}"
                db.session.commit()
                return jsonify({'error': f'Failed to initiate call: {str(e)}'}), 500
        else:
            # Demo mode - simulate call
            call.call_sid = f"demo_call_{call.id}"
            call.status = 'in_progress'
            db.session.commit()
            
            return jsonify({
                'call_id': call.id,
                'call_sid': call.call_sid,
                'status': 'initiated',
                'message': 'Call initiated successfully (demo mode)'
            })
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@voice_agent_bp.route('/voice/webhook/<int:call_id>', methods=['POST'])
def voice_webhook(call_id):
    """Twilio webhook for handling voice interactions"""
    try:
        call = Call.query.get_or_404(call_id)
        lead = call.lead
        
        # Get sales playbook for the lead's industry
        playbook = SalesPlaybook.query.filter_by(industry=lead.industry).first()
        
        response = VoiceResponse()
        
        # Check if this is the initial call or a response
        if request.form.get('SpeechResult'):
            # Process customer speech
            customer_speech = request.form.get('SpeechResult')
            
            # Generate AI response based on customer input
            ai_response = generate_ai_response(customer_speech, lead, playbook, call)
            
            # Convert AI response to speech and play it
            response.say(ai_response, voice='alice')
            
            # Continue listening for customer response
            response.gather(
                input='speech',
                action=f'/api/voice/webhook/{call_id}',
                speech_timeout='auto',
                language='en-US'
            )
        else:
            # Initial greeting
            if playbook:
                greeting = playbook.opening_script
            else:
                greeting = f"Hello {lead.name}, this is Sarah from our sales team. How are you doing today?"
            
            response.say(greeting, voice='alice')
            
            # Start listening for customer response
            response.gather(
                input='speech',
                action=f'/api/voice/webhook/{call_id}',
                speech_timeout='auto',
                language='en-US'
            )
        
        return str(response)
        
    except Exception as e:
        response = VoiceResponse()
        response.say("I'm sorry, there was a technical issue. We'll call you back shortly.")
        response.hangup()
        return str(response)

def generate_ai_response(customer_speech, lead, playbook, call):
    """Generate AI response using OpenAI GPT-4"""
    try:
        # Build context for the AI
        context = f"""
        You are an expert sales agent calling {lead.name} from {lead.company or 'their business'} 
        in the {lead.industry} industry. 
        
        Customer just said: "{customer_speech}"
        
        Your goal is to:
        1. Be conversational and natural
        2. Identify pain points and needs
        3. Present relevant solutions
        4. Handle objections professionally
        5. Move towards scheduling a demo or appointment
        
        Keep responses under 50 words and sound human-like with natural speech patterns.
        """
        
        if playbook:
            context += f"""
            
            Use these industry-specific talking points:
            Pain Points: {', '.join(playbook.pain_points)}
            Value Propositions: {', '.join(playbook.value_propositions)}
            """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": customer_speech}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Log the interaction
        if not call.transcript:
            call.transcript = ""
        call.transcript += f"\nCustomer: {customer_speech}\nAgent: {ai_response}\n"
        db.session.commit()
        
        return ai_response
        
    except Exception as e:
        # Fallback response
        return "I understand. Could you tell me more about your current challenges in your business?"

@voice_agent_bp.route('/voice/end-call', methods=['POST'])
def end_call():
    """End a call and update records"""
    try:
        data = request.get_json()
        call_id = data.get('call_id')
        outcome = data.get('outcome')
        notes = data.get('notes', '')
        
        call = Call.query.get_or_404(call_id)
        call.status = 'completed'
        call.completed_at = datetime.utcnow()
        call.outcome = outcome
        call.notes = notes
        
        # Update lead status based on call outcome
        if outcome == 'appointment':
            call.lead.status = 'qualified'
            call.lead.score += 30
        elif outcome == 'interested':
            call.lead.status = 'contacted'
            call.lead.score += 15
        elif outcome == 'callback':
            call.lead.status = 'contacted'
            call.lead.score += 10
        elif outcome == 'not_interested':
            call.lead.status = 'lost'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Call ended successfully',
            'call': call.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@voice_agent_bp.route('/voice/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment of call transcript"""
    try:
        data = request.get_json()
        call_id = data.get('call_id')
        
        call = Call.query.get_or_404(call_id)
        
        if not call.transcript:
            return jsonify({'error': 'No transcript available'}), 400
        
        # Use OpenAI to analyze sentiment
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "Analyze the sentiment of this sales call transcript. Return a score from -1 (very negative) to 1 (very positive) and a brief explanation."
                },
                {"role": "user", "content": call.transcript}
            ],
            max_tokens=150
        )
        
        analysis = response.choices[0].message.content.strip()
        
        # Extract sentiment score (simplified - in production, use more sophisticated parsing)
        try:
            # Look for a number between -1 and 1 in the response
            import re
            score_match = re.search(r'-?0\.\d+|-?1\.0+|0\.0+', analysis)
            if score_match:
                sentiment_score = float(score_match.group())
            else:
                sentiment_score = 0.0
        except:
            sentiment_score = 0.0
        
        call.sentiment_score = sentiment_score
        call.notes = (call.notes or '') + f"\n\nSentiment Analysis: {analysis}"
        db.session.commit()
        
        return jsonify({
            'sentiment_score': sentiment_score,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@voice_agent_bp.route('/voice/generate-follow-up', methods=['POST'])
def generate_follow_up():
    """Generate follow-up message based on call outcome"""
    try:
        data = request.get_json()
        call_id = data.get('call_id')
        message_type = data.get('type', 'email')  # email or sms
        
        call = Call.query.get_or_404(call_id)
        lead = call.lead
        
        # Generate personalized follow-up message
        context = f"""
        Generate a {message_type} follow-up message for {lead.name} from {lead.company or 'their business'}.
        
        Call outcome: {call.outcome}
        Industry: {lead.industry}
        Call notes: {call.notes or 'No specific notes'}
        
        Make it professional, personalized, and include a clear next step.
        Keep it under 200 words for email, 160 characters for SMS.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": f"Generate a {message_type} follow-up message"}
            ],
            max_tokens=200 if message_type == 'email' else 50
        )
        
        follow_up_message = response.choices[0].message.content.strip()
        
        return jsonify({
            'message': follow_up_message,
            'type': message_type,
            'recipient': lead.email if message_type == 'email' else lead.phone
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@voice_agent_bp.route('/voice/bulk-call', methods=['POST'])
def initiate_bulk_calls():
    """Initiate calls to multiple leads"""
    try:
        data = request.get_json()
        lead_ids = data.get('lead_ids', [])
        
        if not lead_ids:
            return jsonify({'error': 'No lead IDs provided'}), 400
        
        results = []
        
        for lead_id in lead_ids:
            try:
                lead = Lead.query.get(lead_id)
                if not lead:
                    results.append({
                        'lead_id': lead_id,
                        'status': 'error',
                        'message': 'Lead not found'
                    })
                    continue
                
                # Create call record
                call = Call(
                    lead_id=lead_id,
                    status='initiated'
                )
                db.session.add(call)
                db.session.commit()
                
                # In demo mode, just mark as initiated
                call.call_sid = f"demo_bulk_call_{call.id}"
                call.status = 'queued'
                db.session.commit()
                
                results.append({
                    'lead_id': lead_id,
                    'call_id': call.id,
                    'status': 'queued',
                    'message': 'Call queued successfully'
                })
                
            except Exception as e:
                results.append({
                    'lead_id': lead_id,
                    'status': 'error',
                    'message': str(e)
                })
        
        return jsonify({
            'results': results,
            'total_queued': len([r for r in results if r['status'] == 'queued'])
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

