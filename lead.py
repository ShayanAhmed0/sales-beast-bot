from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, converted, lost
    score = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with calls
    calls = db.relationship('Call', backref='lead', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'company': self.company,
            'industry': self.industry,
            'status': self.status,
            'score': self.score,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'calls_count': len(self.calls) if self.calls else 0
        }

class Call(db.Model):
    __tablename__ = 'calls'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)
    call_sid = db.Column(db.String(100), nullable=True)  # Twilio call SID
    status = db.Column(db.String(20), default='initiated')  # initiated, in_progress, completed, failed
    duration = db.Column(db.Integer, default=0)  # in seconds
    recording_url = db.Column(db.String(500), nullable=True)
    transcript = db.Column(db.Text, nullable=True)
    sentiment_score = db.Column(db.Float, default=0.0)
    outcome = db.Column(db.String(50), nullable=True)  # appointment, interested, not_interested, callback
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'call_sid': self.call_sid,
            'status': self.status,
            'duration': self.duration,
            'recording_url': self.recording_url,
            'transcript': self.transcript,
            'sentiment_score': self.sentiment_score,
            'outcome': self.outcome,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class SalesPlaybook(db.Model):
    __tablename__ = 'sales_playbooks'
    
    id = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.String(50), nullable=False, unique=True)
    opening_script = db.Column(db.Text, nullable=False)
    pain_points = db.Column(db.JSON, nullable=False)  # List of common pain points
    value_propositions = db.Column(db.JSON, nullable=False)  # List of value props
    objection_responses = db.Column(db.JSON, nullable=False)  # Dict of objection: response
    closing_techniques = db.Column(db.JSON, nullable=False)  # List of closing techniques
    follow_up_templates = db.Column(db.JSON, nullable=False)  # Dict of templates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'industry': self.industry,
            'opening_script': self.opening_script,
            'pain_points': self.pain_points,
            'value_propositions': self.value_propositions,
            'objection_responses': self.objection_responses,
            'closing_techniques': self.closing_techniques,
            'follow_up_templates': self.follow_up_templates,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

