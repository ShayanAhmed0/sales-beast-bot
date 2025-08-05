from flask import Blueprint, request, jsonify
from src.models.lead import Lead, Call, SalesPlaybook, db
from datetime import datetime
import os
import openai
import requests
from twilio.rest import Client

voice_agent_bp = Blueprint("voice_agent", __name__)

# Initialize clients (will be configured with environment variables)
def get_openai_client():
    """Get OpenAI client with API key from environment"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return openai.OpenAI(api_key=api_key)

def get_twilio_client():
    """Get Twilio client with credentials from environment"""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    if not account_sid or not auth_token:
        raise ValueError("Twilio credentials not set in environment variables")
    return Client(account_sid, auth_token)

def get_elevenlabs_headers():
    """Get ElevenLabs API headers"""
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")
    return {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

@voice_agent_bp.route("/voice/initiate-call", methods=["POST"])
def initiate_call():
    """Initiate a voice call to a lead"""
    try:
        data = request.get_json()
        lead_id = data.get("lead_id")
        
        if not lead_id:
            return jsonify({"error": "lead_id is required"}), 400
        
        lead = Lead.query.get_or_404(lead_id)
        
        # Get sales playbook for the lead's industry
        playbook = SalesPlaybook.query.filter_by(industry=lead.industry).first()
        if not playbook:
            return jsonify({"error": f"No playbook found for industry: {lead.industry}"}), 400
        
        # Create call record
        call = Call(
            lead_id=lead_id,
            status="initiated"
        )
        db.session.add(call)
        db.session.commit()
        
        # In a real implementation, this would initiate the actual Twilio call
        # For now, we'll simulate the call initiation
        try:
            # Simulate Twilio call initiation
            # twilio_client = get_twilio_client()
            # call_response = twilio_client.calls.create(
            #     to=lead.phone,
            #     from_=os.getenv('TWILIO_PHONE_NUMBER'),
            #     url='https://your-webhook-url.com/voice/handle-call'
            # )
            # call.call_sid = call_response.sid
            
            # For demo purposes, generate a mock call SID
            call.call_sid = f"CA{datetime.now().strftime('%Y%m%d%H%M%S')}{lead_id}"
            call.status = "in_progress"
            db.session.commit()
            
            return jsonify({
                "message": "Call initiated successfully",
                "call_id": call.id,
                "call_sid": call.call_sid,
                "lead": lead.to_dict(),
                "playbook": playbook.to_dict()
            })
            
        except Exception as e:
            call.status = "failed"
            call.notes = f"Failed to initiate call: {str(e)}"
            db.session.commit()
            return jsonify({"error": f"Failed to initiate call: {str(e)}"}), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@voice_agent_bp.route("/voice/handle-call", methods=["POST"])
def handle_call():
    """Handle incoming Twilio webhook for call events"""
    try:
        # This would be called by Twilio webhooks
        call_sid = request.form.get('CallSid')
        call_status = request.form.get('CallStatus')
        
        if not call_sid:
            return jsonify({"error": "CallSid is required"}), 400
        
        call = Call.query.filter_by(call_sid=call_sid).first()
        if not call:
            return jsonify({"error": "Call not found"}), 404
        
        # Update call status
        call.status = call_status.lower()
        
        if call_status in ['completed', 'busy', 'no-answer', 'failed']:
            call.completed_at = datetime.utcnow()
            call.duration = int(request.form.get('CallDuration', 0))
        
        db.session.commit()
        
        return jsonify({"message": "Call status updated"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@voice_agent_bp.route("/voice/generate-speech", methods=["POST"])
def generate_speech():
    """Generate speech using ElevenLabs TTS"""
    try:
        data = request.get_json()
        text = data.get("text")
        voice_id = data.get("voice_id", "21m00Tcm4TlvDq8ikWAM")  # Default voice
        
        if not text:
            return jsonify({"error": "text is required"}), 400
        
        # ElevenLabs TTS API call
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8
            }
        }
        
        headers = get_elevenlabs_headers()
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # In a real implementation, you would save the audio file
            # and return a URL to access it
            return jsonify({
                "message": "Speech generated successfully",
                "audio_size": len(response.content),
                "content_type": "audio/mpeg"
            })
        else:
            return jsonify({"error": "Failed to generate speech"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@voice_agent_bp.route("/voice/analyze-sentiment", methods=["POST"])
def analyze_sentiment():
    """Analyze sentiment of conversation text using OpenAI"""
    try:
        data = request.get_json()
        text = data.get("text")
        
        if not text:
            return jsonify({"error": "text is required"}), 400
        
        client = get_openai_client()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sentiment analysis expert. Analyze the sentiment of the given text and return a score between -1 (very negative) and 1 (very positive), along with a brief explanation."
                },
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this conversation: {text}"
                }
            ],
            max_tokens=150
        )
        
        analysis = response.choices[0].message.content
        
        # Extract sentiment score (simplified - in production, use more sophisticated parsing)
        sentiment_score = 0.0
        if "positive" in analysis.lower():
            sentiment_score = 0.7
        elif "negative" in analysis.lower():
            sentiment_score = -0.3
        elif "neutral" in analysis.lower():
            sentiment_score = 0.0
        
        return jsonify({
            "sentiment_score": sentiment_score,
            "analysis": analysis
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@voice_agent_bp.route("/voice/generate-response", methods=["POST"])
def generate_response():
    """Generate AI response for conversation"""
    try:
        data = request.get_json()
        conversation_history = data.get("conversation_history", [])
        lead_id = data.get("lead_id")
        
        if not lead_id:
            return jsonify({"error": "lead_id is required"}), 400
        
        lead = Lead.query.get_or_404(lead_id)
        playbook = SalesPlaybook.query.filter_by(industry=lead.industry).first()
        
        if not playbook:
            return jsonify({"error": f"No playbook found for industry: {lead.industry}"}), 400
        
        client = get_openai_client()
        
        # Build context for AI
        system_prompt = f"""
        You are an expert sales agent calling {lead.name} from {lead.company} in the {lead.industry} industry.
        
        Use this sales playbook:
        - Opening: {playbook.opening_script}
        - Pain Points: {', '.join(playbook.pain_points)}
        - Value Props: {', '.join(playbook.value_propositions)}
        
        Be natural, conversational, and focus on building rapport. Ask questions to understand their needs.
        Keep responses concise (1-2 sentences max).
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        return jsonify({
            "response": ai_response,
            "lead": lead.to_dict()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@voice_agent_bp.route("/voice/end-call", methods=["POST"])
def end_call():
    """End a call and update records"""
    try:
        data = request.get_json()
        call_id = data.get("call_id")
        outcome = data.get("outcome")
        notes = data.get("notes")
        transcript = data.get("transcript")
        sentiment_score = data.get("sentiment_score")
        
        if not call_id:
            return jsonify({"error": "call_id is required"}), 400
        
        call = Call.query.get_or_404(call_id)
        
        # Update call record
        call.status = "completed"
        call.completed_at = datetime.utcnow()
        call.outcome = outcome
        call.notes = notes
        call.transcript = transcript
        call.sentiment_score = sentiment_score or 0.0
        
        # Update lead based on call outcome
        lead = call.lead
        if outcome == "appointment":
            lead.status = "qualified"
            lead.score += 30
        elif outcome == "interested":
            lead.status = "contacted"
            lead.score += 15
        elif outcome == "callback":
            lead.status = "contacted"
            lead.score += 10
        elif outcome == "not_interested":
            lead.status = "lost"
            lead.score -= 5
        
        lead.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "message": "Call ended successfully",
            "call": call.to_dict(),
            "lead": lead.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@voice_agent_bp.route("/voice/active-calls", methods=["GET"])
def get_active_calls():
    """Get all active calls for monitoring"""
    try:
        active_calls = Call.query.filter(
            Call.status.in_(["initiated", "in_progress"])
        ).join(Lead).all()
        
        calls_data = []
        for call in active_calls:
            call_data = call.to_dict()
            call_data["lead"] = call.lead.to_dict()
            calls_data.append(call_data)
        
        return jsonify(calls_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@voice_agent_bp.route("/voice/generate-follow-up", methods=["POST"])
def generate_follow_up():
    """Generate follow-up message based on call outcome"""
    try:
        data = request.get_json()
        call_id = data.get("call_id")
        message_type = data.get("type", "email")  # email or sms
        
        if not call_id:
            return jsonify({"error": "call_id is required"}), 400
        
        call = Call.query.get_or_404(call_id)
        lead = call.lead
        playbook = SalesPlaybook.query.filter_by(industry=lead.industry).first()
        
        if not playbook or not playbook.follow_up_templates:
            return jsonify({"error": "No follow-up templates available"}), 400
        
        # Get appropriate template based on outcome
        templates = playbook.follow_up_templates
        template_key = f"{call.outcome}_{message_type}"
        
        if template_key not in templates:
            template_key = f"default_{message_type}"
        
        if template_key not in templates:
            return jsonify({"error": "No suitable template found"}), 400
        
        template = templates[template_key]
        
        # Replace placeholders
        message = template.replace("{lead_name}", lead.name)
        message = message.replace("{company}", lead.company or "your business")
        message = message.replace("{agent_name}", "Sarah")  # Could be configurable
        
        return jsonify({
            "message": message,
            "type": message_type,
            "call": call.to_dict(),
            "lead": lead.to_dict()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

