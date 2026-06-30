from flask import Blueprint, request, jsonify

from models import db, Student, Drive, Application, Placement
from routes.utils import role_required, current_user_id

student_bp = Blueprint("student", __name__)


def get_student_or_404():
    return Student.query.filter_by(user_id=current_user_id()).first()


@student_bp.route("/profile", methods=["GET"])
@role_required("student")
def get_profile():
    student = get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    return jsonify(student.to_dict()), 200


@student_bp.route("/profile", methods=["PUT"])
@role_required("student")
def update_profile():
    student = get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    data = request.get_json()
    for field in ("name", "branch", "cgpa", "year", "contact", "skills", "resume_filename"):
        if field in data:
            setattr(student, field, data[field])
    db.session.commit()
    return jsonify(student.to_dict()), 200


@student_bp.route("/dashboard", methods=["GET"])
@role_required("student")
def dashboard():
    student = get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    apps = Application.query.filter_by(student_id=student.id).all()
    return jsonify({
        "student": student.to_dict(),
        "total_applications": len(apps),
        "applications": [a.to_dict() for a in apps],
    }), 200


# ---- Apply to drive ----

@student_bp.route("/drives/<int:drive_id>/apply", methods=["POST"])
@role_required("student")
def apply_to_drive(drive_id):
    student = get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    drive = Drive.query.get_or_404(drive_id)
    if drive.status != "Approved":
        return jsonify({"error": "This drive is not open for applications"}), 403

    # Prevent duplicate applications
    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        return jsonify({"error": "You have already applied to this drive"}), 400

    # Eligibility validation
    if drive.min_cgpa and (student.cgpa is None or student.cgpa < drive.min_cgpa):
        return jsonify({"error": f"You do not meet the minimum CGPA requirement ({drive.min_cgpa})"}), 403

    if drive.branch_eligibility and drive.branch_eligibility.lower() != "any":
        eligible_branches = [b.strip().lower() for b in drive.branch_eligibility.split(",")]
        if not student.branch or student.branch.lower() not in eligible_branches:
            return jsonify({"error": "You are not eligible for this drive based on your branch"}), 403

    if drive.eligible_year and student.year and student.year != drive.eligible_year:
        return jsonify({"error": "You are not eligible for this drive based on your graduation year"}), 403

    application = Application(student_id=student.id, drive_id=drive_id, status="Applied")
    db.session.add(application)
    db.session.commit()
    return jsonify(application.to_dict()), 201


@student_bp.route("/applications", methods=["GET"])
@role_required("student")
def list_my_applications():
    student = get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    apps = Application.query.filter_by(student_id=student.id).all()
    return jsonify([a.to_dict() for a in apps]), 200


@student_bp.route("/placements", methods=["GET"])
@role_required("student")
def my_placements():
    student = get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    placements = Placement.query.filter_by(student_id=student.id).all()
    return jsonify([p.to_dict() for p in placements]), 200
