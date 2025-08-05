from flask import Blueprint, request, jsonify
from src.models.lead import Lead, Call, SalesPlaybook, db
from datetime import datetime
import csv
import io

leads_bp = Blueprint("leads", __name__)

@leads_bp.route("/leads", methods=["GET"])
def get_leads():
    """Get all leads with optional filtering"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        status = request.args.get("status")
        industry = request.args.get("industry")
        
        query = Lead.query
        
        if status:
            query = query.filter(Lead.status == status)
        if industry:
            query = query.filter(Lead.industry == industry)
            
        leads = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            "leads": [lead.to_dict() for lead in leads.items],
            "total": leads.total,
            "pages": leads.pages,
            "current_page": page
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@leads_bp.route("/leads", methods=["POST"])
def create_lead():
    """Create a new lead"""
    try:
        data = request.get_json()
        
        # Check if lead with phone already exists
        existing_lead = Lead.query.filter_by(phone=data["phone"]).first()
        if existing_lead:
            return jsonify({"error": "Lead with this phone number already exists"}), 400
        
        lead = Lead(
            name=data["name"],
            phone=data["phone"],
            email=data.get("email"),
            company=data.get("company"),
            industry=data["industry"],
            notes=data.get("notes")
        )
        
        db.session.add(lead)
        db.session.commit()
        
        return jsonify(lead.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@leads_bp.route("/leads/bulk", methods=["POST"])
def bulk_import_leads():
    """Bulk import leads from CSV"""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Read CSV content
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        imported_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_input, start=2):
            try:
                # Check required fields
                if not row.get("name") or not row.get("phone") or not row.get("industry"):
                    errors.append(f"Row {row_num}: Missing required fields (name, phone, industry)")
                    continue
                
                # Check if lead already exists
                existing_lead = Lead.query.filter_by(phone=row["phone"]).first()
                if existing_lead:
                    errors.append(f"Row {row_num}: Lead with phone {row["phone"]} already exists")
                    continue
                
                lead = Lead(
                    name=row["name"],
                    phone=row["phone"],
                    email=row.get("email", ""),
                    company=row.get("company", ""),
                    industry=row["industry"],
                    notes=row.get("notes", "")
                )
                
                db.session.add(lead)
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            "imported_count": imported_count,
            "errors": errors
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@leads_bp.route("/leads/<int:lead_id>", methods=["GET"])
def get_lead(lead_id):
    """Get a specific lead with call history"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        lead_data = lead.to_dict()
        lead_data["calls"] = [call.to_dict() for call in lead.calls]
        return jsonify(lead_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@leads_bp.route("/leads/<int:lead_id>", methods=["PUT"])
def update_lead(lead_id):
    """Update a lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        lead.name = data.get("name", lead.name)
        lead.email = data.get("email", lead.email)
        lead.company = data.get("company", lead.company)
        lead.industry = data.get("industry", lead.industry)
        lead.status = data.get("status", lead.status)
        lead.score = data.get("score", lead.score)
        lead.notes = data.get("notes", lead.notes)
        lead.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(lead.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@leads_bp.route("/leads/<int:lead_id>/calls", methods=["POST"])
def create_call(lead_id):
    """Create a new call record for a lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        call = Call(
            lead_id=lead_id,
            call_sid=data.get("call_sid"),
            status=data.get("status", "initiated"),
            duration=data.get("duration", 0),
            recording_url=data.get("recording_url"),
            transcript=data.get("transcript"),
            sentiment_score=data.get("sentiment_score", 0.0),
            outcome=data.get("outcome"),
            notes=data.get("notes")
        )
        
        if data.get("status") == "completed":
            call.completed_at = datetime.utcnow()
        
        db.session.add(call)
        db.session.commit()
        
        return jsonify(call.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@leads_bp.route("/playbooks", methods=["GET"])
def get_playbooks():
    """Get all sales playbooks"""
    try:
        playbooks = SalesPlaybook.query.all()
        return jsonify([playbook.to_dict() for playbook in playbooks])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@leads_bp.route("/playbooks", methods=["POST"])
def create_playbook():
    """Create a new sales playbook"""
    try:
        data = request.get_json()
        
        # Check if playbook for industry already exists
        existing_playbook = SalesPlaybook.query.filter_by(industry=data["industry"]).first()
        if existing_playbook:
            return jsonify({"error": "Playbook for this industry already exists"}), 400
        
        playbook = SalesPlaybook(
            industry=data["industry"],
            opening_script=data["opening_script"],
            pain_points=data["pain_points"],
            value_propositions=data["value_propositions"],
            objection_responses=data["objection_responses"],
            closing_techniques=data["closing_techniques"],
            follow_up_templates=data["follow_up_templates"]
        )
        
        db.session.add(playbook)
        db.session.commit()
        
        return jsonify(playbook.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@leads_bp.route("/analytics/dashboard", methods=["GET"])
def get_dashboard_analytics():
    """Get dashboard analytics data"""
    try:
        # Total leads
        total_leads = Lead.query.count()
        
        # Leads by status
        leads_by_status = db.session.query(
            Lead.status, 
            db.func.count(Lead.id)
        ).group_by(Lead.status).all()
        
        # Total calls
        total_calls = Call.query.count()
        
        # Calls by outcome
        calls_by_outcome = db.session.query(
            Call.outcome, 
            db.func.count(Call.id)
        ).group_by(Call.outcome).all()
        
        # Average call duration
        avg_duration = db.session.query(
            db.func.avg(Call.duration)
        ).filter(Call.duration > 0).scalar() or 0
        
        # Conversion rate
        converted_leads = Lead.query.filter_by(status="converted").count()
        conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
        
        # Recent calls
        recent_calls = Call.query.join(Lead).order_by(
            Call.created_at.desc()
        ).limit(10).all()
        
        return jsonify({
            "total_leads": total_leads,
            "total_calls": total_calls,
            "conversion_rate": round(conversion_rate, 2),
            "avg_call_duration": round(avg_duration, 2),
            "leads_by_status": dict(leads_by_status),
            "calls_by_outcome": dict(calls_by_outcome),
            "recent_calls": [
                {
                    **call.to_dict(),
                    "lead_name": call.lead.name,
                    "lead_company": call.lead.company
                } for call in recent_calls
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


