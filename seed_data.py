#!/usr/bin/env python3
"""
Seed data script for AI Voice Sales Agent
Populates the database with sample leads and sales playbooks
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.lead import Lead, SalesPlaybook, db
from src.main import app

def seed_playbooks():
    """Create sample sales playbooks for different industries"""
    
    playbooks_data = [
        {
            'industry': 'restaurant',
            'opening_script': "Hi {name}, this is Sarah from TechSolutions. I hope you're having a great day! I'm calling because I noticed your restaurant might benefit from our new customer management system that's helping restaurants like yours increase orders by 30%. Do you have just 2 minutes to hear how this could help your business?",
            'pain_points': [
                'Staff shortage and high turnover',
                'Managing online orders efficiently',
                'Customer service during peak hours',
                'Inventory management',
                'Marketing to repeat customers'
            ],
            'value_propositions': [
                'Automated order management reduces staff workload',
                '24/7 customer service with AI receptionist',
                'Integrated inventory tracking',
                'Customer loyalty program automation',
                'Real-time analytics and reporting'
            ],
            'objection_responses': {
                'too_expensive': "I understand cost is a concern. Let me ask you this - how much revenue do you lose when customers can't reach you after hours? Our system typically pays for itself within 2 months through increased orders alone.",
                'too_busy': "I completely understand you're busy - that's exactly why this system is perfect for you. It handles customer calls and orders automatically, so you can focus on what you do best - running your restaurant.",
                'already_have_system': "That's great that you have something in place. Many of our clients thought their current system was working until they saw what they were missing. Would you be open to a quick comparison to see if there are any gaps?"
            },
            'closing_techniques': [
                'Limited time offer: "We are offering a 30-day free trial, but only for the next 10 restaurants that sign up this month."',
                'Social proof: "Three restaurants in your area are already using this and seeing amazing results."',
                'Risk reversal: "What if I told you there is zero risk? If you do not see results in 30 days, we will refund every penny."'
            ],
            'follow_up_templates': {
                'email': "Hi {name}, Thank you for taking the time to speak with me today about how our restaurant management system can help {company}. As discussed, I'm attaching a case study showing how a similar restaurant increased their orders by 35% in just 6 weeks. I'd love to schedule a quick 15-minute demo at your convenience. When would work best for you this week?",
                'sms': "Hi {name}, thanks for our chat today! Here's the demo link I mentioned: [link]. When would be a good time for a quick call this week?"
            }
        },
        {
            'industry': 'car_service',
            'opening_script': "Hello {name}, this is Mike from AutoTech Solutions. I'm calling because I help car service businesses like yours streamline their booking process and reduce no-shows by up to 40%. I know you're probably busy, but could I have just 90 seconds to explain how this could help your business?",
            'pain_points': [
                'Customer no-shows and cancellations',
                'Scheduling conflicts and double bookings',
                'After-hours customer inquiries',
                'Managing customer communications',
                'Tracking service history and follow-ups'
            ],
            'value_propositions': [
                'Automated booking and reminder system',
                'Real-time schedule management',
                '24/7 customer service availability',
                'Customer history and service tracking',
                'Automated follow-up for maintenance'
            ],
            'objection_responses': {
                'too_expensive': "I hear you on the cost concern. But think about this - if you reduce no-shows by just 20%, how much additional revenue would that generate? Most of our clients see ROI within the first month.",
                'customers_prefer_calling': "You're absolutely right that some customers prefer calling. That's why our system handles phone calls automatically while also offering online booking for those who prefer it. You get the best of both worlds.",
                'too_complicated': "I understand that concern. That's exactly why we designed this to be incredibly simple. Most shops are up and running in under an hour, and we handle all the setup for you."
            },
            'closing_techniques': [
                'Urgency: "I have one spot left in our January implementation schedule. After that, the next availability is March."',
                'Value stack: "So you get the booking system, customer reminders, 24/7 phone coverage, AND our service tracking - all for less than what you probably spend on coffee each month."',
                'Assumptive close: "Based on what you have told me, this sounds like exactly what you need. Should we start with the 2-week free trial?"'
            ],
            'follow_up_templates': {
                'email': "Hi {name}, Great speaking with you about optimizing {company}'s booking process. As promised, I'm sending over the ROI calculator that shows potential savings from reducing no-shows. Based on your current volume, you could save approximately $X per month. Shall we schedule a brief demo for this week?",
                'sms': "Hi {name}, here's the demo I mentioned: [link]. Also attached the ROI calculator. When's good for a quick call?"
            }
        },
        {
            'industry': 'ai_receptionist',
            'opening_script': "Hi {name}, this is Alex from VirtualAssist Pro. I'm reaching out because I help businesses like {company} never miss another customer call, even after hours. Our AI receptionist has helped similar companies increase their lead capture by 50%. Do you have a moment to hear how this could benefit your business?",
            'pain_points': [
                'Missed calls during busy periods',
                'After-hours customer inquiries',
                'Receptionist costs and availability',
                'Inconsistent customer service quality',
                'Lead qualification and routing'
            ],
            'value_propositions': [
                '24/7 professional call answering',
                'Significant cost savings vs human receptionist',
                'Consistent, high-quality customer service',
                'Automatic lead qualification and routing',
                'Detailed call logs and analytics'
            ],
            'objection_responses': {
                'customers_want_human': "I totally understand that concern. Here's the thing - our AI is so natural that most customers don't even realize they're not speaking to a human. Plus, for complex issues, it seamlessly transfers to your team.",
                'too_impersonal': "That's a common misconception. Our AI is actually more personal because it remembers every customer interaction and can provide consistent, personalized service 24/7. Your human staff can then focus on the high-value interactions.",
                'what_if_it_breaks': "Great question. We have 99.9% uptime, and if there's ever an issue, calls automatically forward to your backup number. Plus, we monitor everything 24/7 to ensure smooth operation."
            },
            'closing_techniques': [
                'Risk-free trial: "How about we set up a 14-day trial where you can test it with real calls? If you are not completely satisfied, there is no charge."',
                'Cost comparison: "Think about it - you are probably spending $3000+ per month on reception staff. This gives you better coverage for a fraction of that cost."',
                'FOMO: "We are only taking on 5 new clients this month to ensure quality service. I would hate for you to miss out on this opportunity."'
            ],
            'follow_up_templates': {
                'email': "Hi {name}, Thank you for your time today discussing how an AI receptionist could benefit {company}. As mentioned, I'm attaching a comparison showing the cost savings vs. traditional reception staff. Most businesses save 60-80% while improving their customer service. Would you like to schedule a quick demo to see it in action?",
                'sms': "Hi {name}, thanks for our conversation! Here's the demo link: [link]. The cost comparison is eye-opening. When can we chat again?"
            }
        }
    ]
    
    for playbook_data in playbooks_data:
        existing = SalesPlaybook.query.filter_by(industry=playbook_data['industry']).first()
        if not existing:
            playbook = SalesPlaybook(**playbook_data)
            db.session.add(playbook)
            print(f"Created playbook for {playbook_data['industry']} industry")
        else:
            print(f"Playbook for {playbook_data['industry']} already exists")

def seed_leads():
    """Create sample leads for testing"""
    
    leads_data = [
        {
            'name': 'Mario Rossi',
            'phone': '+1-555-0101',
            'email': 'mario@rossirestaurant.com',
            'company': 'Rossi Italian Restaurant',
            'industry': 'restaurant',
            'notes': 'Family-owned Italian restaurant, struggling with online orders'
        },
        {
            'name': 'Sarah Johnson',
            'phone': '+1-555-0102',
            'email': 'sarah@johnsonauto.com',
            'company': 'Johnson Auto Repair',
            'industry': 'car_service',
            'notes': 'Auto repair shop with high no-show rate'
        },
        {
            'name': 'David Chen',
            'phone': '+1-555-0103',
            'email': 'david@chenlaw.com',
            'company': 'Chen & Associates Law Firm',
            'industry': 'ai_receptionist',
            'notes': 'Law firm missing calls during court hours'
        },
        {
            'name': 'Lisa Martinez',
            'phone': '+1-555-0104',
            'email': 'lisa@tacofiesta.com',
            'company': 'Taco Fiesta',
            'industry': 'restaurant',
            'notes': 'Mexican restaurant chain, 3 locations'
        },
        {
            'name': 'Robert Wilson',
            'phone': '+1-555-0105',
            'email': 'rob@wilsontires.com',
            'company': 'Wilson Tire Service',
            'industry': 'car_service',
            'notes': 'Tire shop with scheduling issues'
        },
        {
            'name': 'Jennifer Davis',
            'phone': '+1-555-0106',
            'email': 'jennifer@davisrealty.com',
            'company': 'Davis Real Estate',
            'industry': 'ai_receptionist',
            'notes': 'Real estate agency, agents often out showing properties'
        },
        {
            'name': 'Michael Brown',
            'phone': '+1-555-0107',
            'email': 'mike@brownscafe.com',
            'company': 'Browns Coffee & Cafe',
            'industry': 'restaurant',
            'notes': 'Coffee shop looking to expand delivery options'
        },
        {
            'name': 'Amanda Taylor',
            'phone': '+1-555-0108',
            'email': 'amanda@taylordetail.com',
            'company': 'Taylor Auto Detailing',
            'industry': 'car_service',
            'notes': 'Mobile auto detailing service'
        }
    ]
    
    for lead_data in leads_data:
        existing = Lead.query.filter_by(phone=lead_data['phone']).first()
        if not existing:
            lead = Lead(**lead_data)
            db.session.add(lead)
            print(f"Created lead: {lead_data['name']} - {lead_data['company']}")
        else:
            print(f"Lead with phone {lead_data['phone']} already exists")

def main():
    """Main function to seed the database"""
    with app.app_context():
        print("Seeding database with sample data...")
        
        # Create tables if they don't exist
        db.create_all()
        
        # Seed playbooks
        print("\n--- Seeding Sales Playbooks ---")
        seed_playbooks()
        
        # Seed leads
        print("\n--- Seeding Sample Leads ---")
        seed_leads()
        
        # Commit all changes
        db.session.commit()
        
        print("\n✅ Database seeding completed successfully!")
        print(f"Total leads: {Lead.query.count()}")
        print(f"Total playbooks: {SalesPlaybook.query.count()}")

if __name__ == '__main__':
    main()

