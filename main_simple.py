import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.leads import leads_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(leads_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Simple voice agent endpoints without external dependencies
@app.route('/api/voice/demo', methods=['GET'])
def voice_demo():
    """Demo endpoint showing voice agent capabilities"""
    return jsonify({
        'message': 'AI Voice Sales Agent Demo',
        'features': [
            'Ultra-realistic voice synthesis using ElevenLabs',
            'Natural human-like behaviors with pauses and emotions',
            'Industry-specific sales playbooks',
            'Real-time sentiment analysis',
            'Automated follow-up sequences',
            'Comprehensive analytics dashboard'
        ],
        'status': 'Ready for production deployment'
    })

@app.route('/api/voice/capabilities', methods=['GET'])
def voice_capabilities():
    """Show voice agent capabilities"""
    return jsonify({
        'voice_synthesis': {
            'provider': 'ElevenLabs',
            'features': ['Emotion control', 'Multilingual support', 'Interruption handling']
        },
        'telephony': {
            'provider': 'Twilio',
            'features': ['Auto-dialing', 'Call recording', 'SMS/Email follow-up']
        },
        'ai_engine': {
            'provider': 'OpenAI GPT-4',
            'features': ['Natural conversation', 'Objection handling', 'Industry adaptation']
        },
        'analytics': {
            'features': ['Real-time monitoring', 'Sentiment analysis', 'Performance tracking']
        }
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

