# AI Voice Sales Agent

A production-ready, ultra-powerful AI Voice Sales Agent designed to convert leads into paying clients at the highest possible rate. This agent sounds 101% human, capable of real phone conversations with natural pauses, laughs, hesitations, and thinking moments.

## Features

### 🎯 Core Capabilities
- **Ultra-realistic voice synthesis** using ElevenLabs with emotion control
- **Automatic multilingual support** with language and accent adaptation
- **Natural human-like behaviors** including pauses, filler words, and emotional responses
- **Graceful interruption handling** that stops, listens, and resumes naturally
- **Industry-specific sales playbooks** for restaurants, car services, AI receptionists, and more

### 📞 Voice & Behavior
- Natural speech patterns with strategic pauses and filler words
- Real-time sentiment analysis and tone adjustment
- Emotional mirroring to build rapport with prospects
- Dynamic persona switching across different industries
- Contextual conversation flow management

### 🚀 Sales Engine
- Automated lead dialing using Twilio integration
- Dynamic objection handling with industry-specific responses
- Real-time negotiation strategy adaptation
- Comprehensive lead scoring and qualification
- Automated follow-up sequences via SMS and email

### 📊 Analytics & Monitoring
- Real-time call monitoring and sentiment analysis
- Comprehensive performance analytics and reporting
- Lead conversion funnel visualization
- Call transcript analysis and insights
- ROI tracking and optimization recommendations

### 🔧 Technical Stack
- **Backend**: Flask with SQLAlchemy ORM
- **Frontend**: React with Tailwind CSS and shadcn/ui
- **Voice**: ElevenLabs for TTS, Whisper/Deepgram for STT
- **Telephony**: Twilio for call management
- **AI**: OpenAI GPT-4 with Retrieval-Augmented Generation
- **Database**: SQLite (development) / PostgreSQL (production)
- **Analytics**: Real-time dashboard with Recharts

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- API keys for OpenAI, ElevenLabs, and Twilio

### Installation

1. **Clone and setup backend**:
```bash
cd ai_voice_sales_agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Initialize database**:
```bash
python src/seed_data.py
```

4. **Start backend server**:
```bash
python src/main.py
```

5. **Setup and start frontend** (in a new terminal):
```bash
cd ../ai_voice_sales_dashboard
pnpm install
pnpm run dev
```

6. **Access the application**:
- Dashboard: http://localhost:5173
- API: http://localhost:5000

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure the following:

#### Required API Keys
- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key for voice synthesis
- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number for outbound calls

#### Optional Configuration
- `SENDGRID_API_KEY`: For email follow-ups
- `DEFAULT_VOICE_ID`: ElevenLabs voice ID to use
- `MAX_CALL_DURATION`: Maximum call duration in seconds
- `CALL_TIMEOUT`: Timeout for call connection

### Sales Playbooks

The system comes with pre-configured playbooks for:
- **Restaurants**: Focus on online ordering and customer management
- **Car Services**: Emphasis on booking systems and no-show reduction
- **AI Receptionists**: Highlighting 24/7 availability and cost savings

You can customize playbooks through the admin interface or by modifying the seed data.

## Usage

### Lead Management
1. **Import leads**: Upload CSV files with lead information
2. **Manual entry**: Add individual leads through the dashboard
3. **Lead scoring**: Automatic scoring based on interaction quality
4. **Status tracking**: Monitor lead progression through the sales funnel

### Initiating Calls
1. **Single calls**: Click "Call" button next to any lead
2. **Bulk calling**: Select multiple leads for batch processing
3. **Scheduled calls**: Set up automated calling campaigns
4. **Follow-up calls**: Automatic scheduling based on call outcomes

### Monitoring & Analytics
1. **Live monitoring**: Watch active calls in real-time
2. **Call transcripts**: Review conversation details and sentiment
3. **Performance metrics**: Track conversion rates and ROI
4. **Custom reports**: Generate detailed analytics reports

## API Documentation

### Leads API
- `GET /api/leads` - List all leads with pagination
- `POST /api/leads` - Create a new lead
- `PUT /api/leads/{id}` - Update lead information
- `POST /api/leads/bulk` - Bulk import leads from CSV

### Voice Agent API
- `POST /api/voice/initiate-call` - Start a call to a lead
- `POST /api/voice/end-call` - End an active call
- `POST /api/voice/analyze-sentiment` - Analyze call sentiment
- `POST /api/voice/generate-follow-up` - Generate follow-up messages

### Analytics API
- `GET /api/analytics/dashboard` - Get dashboard metrics
- `GET /api/analytics/performance` - Get performance trends
- `GET /api/analytics/conversion` - Get conversion funnel data

## Advanced Features

### Custom Voice Profiles
Create industry-specific voice profiles with different:
- Tone and speaking style
- Accent and language preferences
- Emotional responsiveness patterns
- Conversation pacing

### Intelligent Follow-up
- Automatic email and SMS sequences
- Personalized content based on call outcomes
- Optimal timing prediction for follow-up contacts
- A/B testing for message effectiveness

### Integration Capabilities
- CRM system synchronization
- Calendar integration for appointment booking
- Payment processing for immediate conversions
- Third-party analytics and reporting tools

## Deployment

### Production Deployment
1. **Environment setup**: Configure production environment variables
2. **Database migration**: Set up PostgreSQL for production
3. **Service deployment**: Use Docker or cloud platforms
4. **SSL configuration**: Enable HTTPS for secure communications
5. **Monitoring setup**: Configure logging and error tracking

### Scaling Considerations
- **Concurrent calls**: Configure Twilio for high-volume calling
- **Database optimization**: Use connection pooling and indexing
- **Caching**: Implement Redis for session and data caching
- **Load balancing**: Distribute traffic across multiple instances

## Security

### Data Protection
- End-to-end encryption for all voice communications
- Secure API key management
- GDPR and CCPA compliance features
- Regular security audits and updates

### Access Control
- Role-based access control (RBAC)
- Multi-factor authentication
- API rate limiting
- Session management and timeout controls

## Troubleshooting

### Common Issues
1. **Call connection failures**: Check Twilio configuration and phone number format
2. **Voice synthesis errors**: Verify ElevenLabs API key and voice ID
3. **Database connection issues**: Ensure database is running and accessible
4. **CORS errors**: Verify Flask CORS configuration for frontend access

### Debug Mode
Enable debug mode by setting `FLASK_ENV=development` in your `.env` file.

### Logs
Check application logs for detailed error information:
- Backend logs: Console output from Flask server
- Frontend logs: Browser developer console
- Call logs: Twilio console for telephony issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is proprietary software for internal use only. All rights reserved.

## Support

For technical support or questions:
- Check the troubleshooting section
- Review API documentation
- Contact the development team

---

**Note**: This is a powerful sales automation tool. Please ensure compliance with local regulations regarding automated calling and data privacy when deploying in production.

