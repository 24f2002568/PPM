from datetime import datetime

from flask import Blueprint, request, jsonify

from models import db, Company, Drive, Application
from routes.utils import role_required, current_user_id

company_bp = Blueprint("company", __name__)


def get_company_or_404():
    company = Company.query.filter_by(user_id=current_user_id()).first()
    if not company:
        return None
    return company


@company_bp.route("/profile", methods=["GET"])
@role_required("company")
def get_profile():
    company = get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404
    return jsonify(company.to_dict()), 200


@company_bp.route("/profile", methods=["PUT"])
@role_required("company")
def update_profile():
    company = get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404
    data = request.get_json()
    for field in ("name", "industry", "hr_contact", "website"):
        if field in data:
            setattr(company, field, data[field])
    db.session.commit()
    return jsonify(company.to_dict()), 200


@company_bp.route("/dashboard", methods=["GET"])
@role_required("company")
def dashboard():
    company = get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404
    drives = Drive.query.filter_by(company_id=company.id).all()
    total_applicants = sum(len(d.applications) for d in drives)
    return jsonify({
        "company": company.to_dict(),
        "total_drives": len(drives),
        "total_applicants": total_applicants,
        "drives": [d.to_dict() for d in drives],
    }), 200


# ---- Drive management ----

@company_bp.route("/drives", methods=["POST"])
@role_required("company")
def create_drive():
    company = get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404
    if company.approval_status != "Approved":
        return jsonify({"error": "Company not yet approved by admin"}), 403

    data = request.get_json()
    deadline = None
    if data.get("application_deadline"):
        deadline = datetime.strptime(data["application_deadline"], "%Y-%m-%d").date()

    drive = Drive(
        company_id=company.id,
        job_title=data.get("job_title"),
        job_description=data.get("job_description"),
        branch_eligibility=data.get("branch_eligibility", "Any"),
        min_cgpa=data.get("min_cgpa", 0),
        eligible_year=data.get("eligible_year"),
        salary=data.get("salary"),
        skills_required=data.get("skills_required"),
        application_deadline=deadline,
        status="Pending",
    )
    db.session.add(drive)
    db.session.commit()
    return jsonify(drive.to_dict()), 201


@company_bp.route("/drives", methods=["GET"])
@role_required("company")
def list_my_drives():
    company = get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404
    drives = Drive.query.filter_by(company_id=company.id).all()
    return jsonify([d.to_dict() for d in drives]), 200


@company_bp.route("/drives/<int:drive_id>", methods=["PUT"])
@role_required("company")
def update_drive(drive_id):
    company = get_company_or_404()
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id != company.id:
        return jsonify({"error": "Not your drive"}), 403

    data = request.get_json()
    for field in ("job_title", "job_description", "branch_eligibility", "min_cgpa",
                  "eligible_year", "salary", "skills_required"):
        if field in data:
            setattr(drive, field, data[field])
    if data.get("status") == "Closed":
        drive.status = "Closed"
    if data.get("application_deadline"):
        drive.application_deadline = datetime.strptime(data["application_deadline"], "%Y-%m-%d").date()
    db.session.commit()
    return jsonify(drive.to_dict()), 200


@company_bp.route("/drives/<int:drive_id>/applicants", methods=["GET"])
@role_required("company")
def drive_applicants(drive_id):
    company = get_company_or_404()
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id != company.id:
        return jsonify({"error": "Not your drive"}), 403
    apps = Application.query.filter_by(drive_id=drive_id).all()
    return jsonify([a.to_dict() for a in apps]), 200


# ---- Application management ----

VALID_STATUSES = ["Applied", "Shortlisted", "Interview", "Offer", "Rejected", "Placed"]


@company_bp.route("/applications/<int:application_id>", methods=["PUT"])
@role_required("company")
def update_application(application_id):
    company = get_company_or_404()
    app_obj = Application.query.get_or_404(application_id)
    if app_obj.drive.company_id != company.id:
        return jsonify({"error": "Not your application to manage"}), 403

    data = request.get_json()
    status = data.get("status")
    if status and status not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Must be one of {VALID_STATUSES}"}), 400

    if status:
        app_obj.status = status
    if "feedback" in data:
        app_obj.feedback = data["feedback"]
    if "interview_datetime" in data and data["interview_datetime"]:
        app_obj.interview_datetime = datetime.fromisoformat(data["interview_datetime"])

    if status == "Placed" and not app_obj.placement:
        from models import Placement
        placement = Placement(
            application_id=app_obj.id,
            student_id=app_obj.student_id,
            company_id=app_obj.drive.company_id,
            position=app_obj.drive.job_title,
            salary=app_obj.drive.salary,
        )
        db.session.add(placement)

    db.session.commit()
    return jsonify(app_obj.to_dict()), 200
