from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

from models import db, User, Student, Company

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password or not name:
        return jsonify({"error": "email, password, and name are required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(email=email, role="student", is_active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        name=name,
        branch=data.get("branch"),
        cgpa=data.get("cgpa"),
        year=data.get("year"),
        contact=data.get("contact"),
        skills=data.get("skills"),
    )
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Registered successfully. You can now log in."}), 201


@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password or not name:
        return jsonify({"error": "email, password, and name are required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(email=email, role="company", is_active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.id,
        name=name,
        industry=data.get("industry"),
        hr_contact=data.get("hr_contact"),
        website=data.get("website"),
        approval_status="Pending",
    )
    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Registered successfully. Awaiting admin approval before you can log in."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "Your account has been deactivated. Contact admin."}), 403

    if user.role == "company":
        company = Company.query.filter_by(user_id=user.id).first()
        if not company or company.approval_status != "Approved":
            return jsonify({"error": "Your company profile is not yet approved by admin."}), 403

    token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )
    return jsonify({"token": token, "user": user.to_dict()}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404

    profile = user.to_dict()
    if user.role == "student" and user.student:
        profile["profile"] = user.student.to_dict()
    elif user.role == "company" and user.company:
        profile["profile"] = user.company.to_dict()

    return jsonify(profile), 200
