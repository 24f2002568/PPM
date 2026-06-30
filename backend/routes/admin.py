from flask import Blueprint, request, jsonify

from models import db, User, Student, Company, Drive, Application
from routes.utils import role_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard", methods=["GET"])
@role_required("admin")
def dashboard():
    return jsonify({
        "total_students": Student.query.count(),
        "total_companies": Company.query.count(),
        "total_drives": Drive.query.count(),
        "total_applications": Application.query.count(),
        "pending_companies": Company.query.filter_by(approval_status="Pending").count(),
        "pending_drives": Drive.query.filter_by(status="Pending").count(),
    }), 200


# ---- Companies ----

@admin_bp.route("/companies", methods=["GET"])
@role_required("admin")
def list_companies():
    search = request.args.get("search", "").strip()
    query = Company.query
    if search:
        like = f"%{search}%"
        query = query.filter(db.or_(Company.name.ilike(like), Company.industry.ilike(like)))
    companies = query.all()
    return jsonify([c.to_dict() for c in companies]), 200


@admin_bp.route("/companies/<int:company_id>/approve", methods=["POST"])
@role_required("admin")
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = "Approved"
    db.session.commit()
    return jsonify(company.to_dict()), 200


@admin_bp.route("/companies/<int:company_id>/reject", methods=["POST"])
@role_required("admin")
def reject_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = "Rejected"
    db.session.commit()
    return jsonify(company.to_dict()), 200


@admin_bp.route("/companies/<int:company_id>", methods=["DELETE"])
@role_required("admin")
def remove_company(company_id):
    company = Company.query.get_or_404(company_id)
    user = User.query.get(company.user_id)
    db.session.delete(company)
    if user:
        db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Company removed"}), 200


@admin_bp.route("/companies/<int:company_id>/toggle-active", methods=["POST"])
@role_required("admin")
def toggle_company_active(company_id):
    company = Company.query.get_or_404(company_id)
    user = User.query.get(company.user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify(company.to_dict()), 200


# ---- Students ----

@admin_bp.route("/students", methods=["GET"])
@role_required("admin")
def list_students():
    search = request.args.get("search", "").strip()
    query = Student.query
    if search:
        like = f"%{search}%"
        query = query.join(User).filter(
            db.or_(Student.name.ilike(like), Student.contact.ilike(like), User.email.ilike(like))
        )
    students = query.all()
    return jsonify([s.to_dict() for s in students]), 200


@admin_bp.route("/students/<int:student_id>/toggle-active", methods=["POST"])
@role_required("admin")
def toggle_student_active(student_id):
    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify(student.to_dict()), 200


# ---- Drives ----

@admin_bp.route("/drives", methods=["GET"])
@role_required("admin")
def list_all_drives():
    drives = Drive.query.all()
    return jsonify([d.to_dict() for d in drives]), 200


@admin_bp.route("/drives/<int:drive_id>/approve", methods=["POST"])
@role_required("admin")
def approve_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    drive.status = "Approved"
    db.session.commit()
    return jsonify(drive.to_dict()), 200


@admin_bp.route("/drives/<int:drive_id>/reject", methods=["POST"])
@role_required("admin")
def reject_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    drive.status = "Rejected"
    db.session.commit()
    return jsonify(drive.to_dict()), 200


@admin_bp.route("/drives/<int:drive_id>", methods=["DELETE"])
@role_required("admin")
def remove_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    db.session.delete(drive)
    db.session.commit()
    return jsonify({"message": "Drive removed"}), 200


# ---- Applications (view all) ----

@admin_bp.route("/applications", methods=["GET"])
@role_required("admin")
def list_all_applications():
    applications = Application.query.all()
    return jsonify([a.to_dict() for a in applications]), 200
