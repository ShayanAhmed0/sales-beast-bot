#!/usr/bin/env python3
"""
AI Voice Sales Agent Demo Script
Demonstrates the key capabilities of the system with simulated interactions
"""

import os
import sys
import time
import json
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.lead import Lead, Call, SalesPlaybook, db
from src.main import app

class VoiceSalesAgentDemo:
    def __init__(self):
        self.app = app
        self.demo_scenarios = [
            {
                'lead_name': 'Mario Rossi',
                'company': 'Rossi Italian Restaurant',
                'industry': 'restaurant',
                'scenario': 'successful_appointment',
                'duration': 285,
                'sentiment': 0.8,
                'outcome': 'appointment'
            },
            {
                'lead_name': 'Sarah Johnson', 
                'company': 'Johnson Auto Repair',
                'industry': 'car_service',
                'scenario': 'interested_callback',
                'duration': 195,
                'sentiment': 0.6,
                'outcome': 'callback'
            },
            {
                'lead_name': 'David Chen',
                'company': 'Chen & Associates Law Firm', 
                'industry': 'ai_receptionist',
                'scenario': 'objection_handling',
                'duration': 340,
                'sentiment': 0.4,
                'outcome': 'interested'
            }
        ]
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60)
    
    def print_step(self, step, description):
        """Print a formatted step"""
        print(f"\n[STEP {step}] {description}")
        print("-" * 50)
    
    def simulate_typing(self, text, delay=0.03):
        """Simulate typing effect for demo"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def demonstrate_voice_synthesis(self):
        """Demonstrate voice synthesis capabilities"""
        self.print_step(1, "Voice Synthesis & Human-like Behavior")
        
        print("🎤 AI Agent Voice Characteristics:")
        print("   • Ultra-realistic voice using ElevenLabs")
        print("   • Natural pauses and filler words")
        print("   • Emotional tone adaptation")
        print("   • Multilingual support")
        print("   • Interruption handling")
        
        print("\n📞 Sample Opening Script:")
        opening_script = """
        "Hi Mario, this is Sarah from TechSolutions. I hope you're having a great day! 
        *pause* I'm calling because I noticed your restaurant might benefit from our new 
        customer management system that's helping restaurants like yours increase orders 
        by 30%. *slight chuckle* Do you have just 2 minutes to hear how this could help 
        your business?"
        """
        self.simulate_typing(opening_script.strip(), 0.05)
        
        print("\n🧠 AI Behavior Features:")
        behaviors = [
            "Strategic pauses before complex responses",
            "Natural 'hmm' and 'let me think' moments", 
            "Emotional mirroring based on customer tone",
            "Graceful interruption handling",
            "Context-aware conversation flow"
        ]
        
        for behavior in behaviors:
            print(f"   ✓ {behavior}")
            time.sleep(0.5)
    
    def demonstrate_sales_engine(self):
        """Demonstrate sales engine capabilities"""
        self.print_step(2, "Sales Engine & Industry Playbooks")
        
        with self.app.app_context():
            playbooks = SalesPlaybook.query.all()
            
            print(f"📚 Loaded {len(playbooks)} Industry Playbooks:")
            for playbook in playbooks:
                print(f"\n🏢 {playbook.industry.upper()} Industry:")
                print(f"   • Pain Points: {len(playbook.pain_points)} identified")
                print(f"   • Value Props: {len(playbook.value_propositions)} ready")
                print(f"   • Objections: {len(playbook.objection_responses)} handled")
                print(f"   • Closing Techniques: {len(playbook.closing_techniques)} available")
        
        print("\n🎯 Objection Handling Example:")
        objection_example = """
        Customer: "This sounds too expensive for our small restaurant."
        
        AI Agent: "I understand cost is a concern, Mario. Let me ask you this - 
        how much revenue do you lose when customers can't reach you after hours? 
        *pause* Our system typically pays for itself within 2 months through 
        increased orders alone. Plus, we're offering a 30-day free trial, 
        so there's zero risk to try it out."
        """
        self.simulate_typing(objection_example.strip(), 0.04)
    
    def simulate_live_call(self, scenario):
        """Simulate a live call scenario"""
        lead_name = scenario['lead_name']
        company = scenario['company']
        industry = scenario['industry']
        
        print(f"\n📞 Initiating call to {lead_name} at {company}")
        print("   Status: Dialing...")
        time.sleep(2)
        
        print("   Status: Connected ✓")
        print("   Recording: Active 🔴")
        print("   Sentiment Analysis: Running 📊")
        
        # Simulate conversation progress
        conversation_stages = [
            ("Opening & Rapport Building", 30),
            ("Pain Point Discovery", 45), 
            ("Value Proposition Presentation", 60),
            ("Objection Handling", 25),
            ("Closing & Next Steps", 35)
        ]
        
        total_duration = 0
        for stage, duration in conversation_stages:
            print(f"\n   Current Stage: {stage}")
            for i in range(duration):
                total_duration += 1
                sentiment = scenario['sentiment'] + random.uniform(-0.1, 0.1)
                sentiment = max(0, min(1, sentiment))  # Clamp between 0 and 1
                
                print(f"\r   Duration: {total_duration:02d}:{total_duration%60:02d} | "
                      f"Sentiment: {'😊' if sentiment > 0.7 else '😐' if sentiment > 0.4 else '😟'} "
                      f"({sentiment:.1f})", end='', flush=True)
                time.sleep(0.1)
        
        print(f"\n\n   Call Completed ✓")
        print(f"   Final Duration: {scenario['duration']} seconds")
        print(f"   Outcome: {scenario['outcome'].upper()}")
        print(f"   Sentiment Score: {scenario['sentiment']:.1f}")
        
        return {
            'duration': scenario['duration'],
            'outcome': scenario['outcome'],
            'sentiment': scenario['sentiment']
        }
    
    def demonstrate_live_monitoring(self):
        """Demonstrate live call monitoring"""
        self.print_step(3, "Live Call Monitoring & Real-time Analytics")
        
        print("🖥️  Live Dashboard Features:")
        features = [
            "Real-time call status monitoring",
            "Live sentiment analysis",
            "Conversation transcript streaming", 
            "Agent performance metrics",
            "Immediate intervention capabilities"
        ]
        
        for feature in features:
            print(f"   ✓ {feature}")
            time.sleep(0.3)
        
        print("\n🎬 Simulating Live Calls...")
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"\n--- Call {i}/3 ---")
            call_result = self.simulate_live_call(scenario)
            
            # Store call result in database
            with self.app.app_context():
                lead = Lead.query.filter_by(name=scenario['lead_name']).first()
                if lead:
                    call = Call(
                        lead_id=lead.id,
                        call_sid=f"demo_call_{int(time.time())}_{i}",
                        status='completed',
                        duration=call_result['duration'],
                        sentiment_score=call_result['sentiment'],
                        outcome=call_result['outcome'],
                        transcript=f"Demo call transcript for {scenario['lead_name']}",
                        completed_at=datetime.utcnow()
                    )
                    db.session.add(call)
                    
                    # Update lead score based on outcome
                    if call_result['outcome'] == 'appointment':
                        lead.score += 30
                        lead.status = 'qualified'
                    elif call_result['outcome'] == 'interested':
                        lead.score += 15
                        lead.status = 'contacted'
                    elif call_result['outcome'] == 'callback':
                        lead.score += 10
                        lead.status = 'contacted'
                    
                    db.session.commit()
            
            time.sleep(1)
    
    def demonstrate_analytics(self):
        """Demonstrate analytics and reporting"""
        self.print_step(4, "Analytics & Performance Reporting")
        
        with self.app.app_context():
            total_leads = Lead.query.count()
            total_calls = Call.query.count()
            completed_calls = Call.query.filter_by(status='completed').count()
            
            if completed_calls > 0:
                avg_duration = db.session.query(db.func.avg(Call.duration)).filter(
                    Call.status == 'completed'
                ).scalar() or 0
                
                avg_sentiment = db.session.query(db.func.avg(Call.sentiment_score)).filter(
                    Call.status == 'completed'
                ).scalar() or 0
                
                appointments = Call.query.filter_by(outcome='appointment').count()
                conversion_rate = (appointments / completed_calls) * 100 if completed_calls > 0 else 0
            else:
                avg_duration = 0
                avg_sentiment = 0
                conversion_rate = 0
        
        print("📊 Real-time Performance Metrics:")
        print(f"   • Total Leads: {total_leads}")
        print(f"   • Total Calls: {total_calls}")
        print(f"   • Completed Calls: {completed_calls}")
        print(f"   • Average Call Duration: {avg_duration:.1f} seconds")
        print(f"   • Average Sentiment: {avg_sentiment:.2f}")
        print(f"   • Conversion Rate: {conversion_rate:.1f}%")
        
        print("\n📈 Analytics Features:")
        analytics_features = [
            "Real-time dashboard with live metrics",
            "Call outcome tracking and analysis", 
            "Sentiment analysis trends",
            "Lead scoring and qualification",
            "ROI and revenue attribution",
            "A/B testing for script optimization",
            "Industry-specific performance benchmarks"
        ]
        
        for feature in analytics_features:
            print(f"   ✓ {feature}")
            time.sleep(0.3)
    
    def demonstrate_follow_up(self):
        """Demonstrate follow-up automation"""
        self.print_step(5, "Automated Follow-up & Lead Nurturing")
        
        print("📧 Follow-up Automation Features:")
        followup_features = [
            "Immediate post-call SMS/email confirmation",
            "Personalized follow-up based on call outcome",
            "Intelligent scheduling for callback requests", 
            "Drip campaigns for long-term nurturing",
            "A/B testing for message optimization"
        ]
        
        for feature in followup_features:
            print(f"   ✓ {feature}")
            time.sleep(0.3)
        
        print("\n📱 Sample Follow-up Messages:")
        
        followup_examples = {
            'appointment': {
                'sms': "Hi Mario! Thanks for our chat today. Your demo is confirmed for tomorrow at 2 PM. Here's the meeting link: [link]. Looking forward to showing you how we can boost your restaurant's orders!",
                'email': "Hi Mario,\n\nThank you for taking the time to speak with me today about how our restaurant management system can help Rossi Italian Restaurant. As discussed, I'm attaching a case study showing how a similar restaurant increased their orders by 35% in just 6 weeks.\n\nYour demo is scheduled for tomorrow at 2:00 PM. I'll send you the meeting link shortly.\n\nBest regards,\nSarah"
            },
            'callback': {
                'sms': "Hi Sarah! Thanks for our conversation about reducing no-shows at Johnson Auto. I'll call you back Thursday at 10 AM as requested. In the meantime, here's that ROI calculator: [link]",
                'email': "Hi Sarah,\n\nGreat speaking with you about optimizing Johnson Auto Repair's booking process. As promised, I'm sending over the ROI calculator that shows potential savings from reducing no-shows.\n\nBased on your current volume, you could save approximately $2,400 per month. I'll call you back Thursday at 10 AM as requested.\n\nBest regards,\nMike"
            }
        }
        
        for outcome, messages in followup_examples.items():
            print(f"\n🎯 {outcome.upper()} Follow-up:")
            print(f"   SMS: {messages['sms'][:100]}...")
            print(f"   Email: {messages['email'][:100]}...")
    
    def show_system_overview(self):
        """Show complete system overview"""
        self.print_step(6, "Complete System Overview")
        
        print("🏗️  System Architecture:")
        architecture = [
            "Backend: Flask + SQLAlchemy + PostgreSQL",
            "Frontend: React + Tailwind CSS + shadcn/ui", 
            "Voice: ElevenLabs (TTS) + Whisper (STT)",
            "Telephony: Twilio for call management",
            "AI: OpenAI GPT-4 with RAG",
            "Analytics: Real-time dashboard with Recharts"
        ]
        
        for component in architecture:
            print(f"   • {component}")
            time.sleep(0.3)
        
        print("\n🔧 Deployment Options:")
        deployment = [
            "Local development with Docker Compose",
            "Cloud deployment (AWS, GCP, Azure)",
            "Kubernetes for auto-scaling",
            "CI/CD pipeline integration",
            "Production monitoring and logging"
        ]
        
        for option in deployment:
            print(f"   • {option}")
            time.sleep(0.3)
        
        print("\n🛡️  Security & Compliance:")
        security = [
            "End-to-end encryption for voice data",
            "GDPR and CCPA compliance features",
            "Role-based access control (RBAC)",
            "API rate limiting and security",
            "SOC 2 Type II compliance ready"
        ]
        
        for feature in security:
            print(f"   • {feature}")
            time.sleep(0.3)
    
    def run_complete_demo(self):
        """Run the complete demonstration"""
        self.print_header("AI VOICE SALES AGENT - LIVE DEMONSTRATION")
        
        print("🚀 Welcome to the AI Voice Sales Agent Demo!")
        print("   This demonstration showcases a production-ready system that")
        print("   converts leads into paying clients using ultra-realistic AI voices.")
        
        input("\nPress Enter to begin the demonstration...")
        
        # Run all demonstration steps
        self.demonstrate_voice_synthesis()
        input("\nPress Enter to continue to Sales Engine demo...")
        
        self.demonstrate_sales_engine()
        input("\nPress Enter to continue to Live Monitoring demo...")
        
        self.demonstrate_live_monitoring()
        input("\nPress Enter to continue to Analytics demo...")
        
        self.demonstrate_analytics()
        input("\nPress Enter to continue to Follow-up demo...")
        
        self.demonstrate_follow_up()
        input("\nPress Enter to see System Overview...")
        
        self.show_system_overview()
        
        self.print_header("DEMONSTRATION COMPLETE")
        print("🎉 Thank you for experiencing the AI Voice Sales Agent!")
        print("\n📋 What you've seen:")
        print("   ✓ Ultra-realistic voice synthesis with human-like behavior")
        print("   ✓ Industry-specific sales playbooks and objection handling")
        print("   ✓ Real-time call monitoring and sentiment analysis")
        print("   ✓ Comprehensive analytics and performance tracking")
        print("   ✓ Automated follow-up and lead nurturing")
        print("   ✓ Production-ready architecture and deployment options")
        
        print("\n🚀 Ready to deploy and start converting leads!")
        print("   • Dashboard: http://localhost:5173")
        print("   • API Documentation: http://localhost:5000/api")
        print("   • Configuration: Edit .env file with your API keys")

def main():
    """Main function to run the demo"""
    demo = VoiceSalesAgentDemo()
    
    try:
        demo.run_complete_demo()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user.")
        print("Thank you for your interest in the AI Voice Sales Agent!")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        print("Please check your configuration and try again.")

if __name__ == '__main__':
    main()

