from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin / company / student
    is_active = db.Column(db.Boolean, default=True)  # blacklist/deactivate flag
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("Student", backref="user", uselist=False, cascade="all, delete-orphan")
    company = db.relationship("Company", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "role": self.role, "is_active": self.is_active}


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    branch = db.Column(db.String(80))
    cgpa = db.Column(db.Float)
    year = db.Column(db.Integer)
    contact = db.Column(db.String(20))
    skills = db.Column(db.String(500))  # comma separated
    resume_filename = db.Column(db.String(255))

    applications = db.relationship("Application", backref="student", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "branch": self.branch,
            "cgpa": self.cgpa,
            "year": self.year,
            "contact": self.contact,
            "skills": self.skills,
            "resume_filename": self.resume_filename,
            "email": self.user.email if self.user else None,
            "is_active": self.user.is_active if self.user else None,
        }


class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(80))
    hr_contact = db.Column(db.String(20))
    website = db.Column(db.String(255))
    approval_status = db.Column(db.String(20), default="Pending")  # Pending / Approved / Rejected

    drives = db.relationship("Drive", backref="company", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "industry": self.industry,
            "hr_contact": self.hr_contact,
            "website": self.website,
            "approval_status": self.approval_status,
            "email": self.user.email if self.user else None,
            "is_active": self.user.is_active if self.user else None,
        }


class Drive(db.Model):
    """Placement Drive / Job Position"""
    __tablename__ = "drives"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text)
    branch_eligibility = db.Column(db.String(255))  # comma separated branches, "Any" for all
    min_cgpa = db.Column(db.Float, default=0)
    eligible_year = db.Column(db.Integer)  # graduation year eligible, null = any
    salary = db.Column(db.String(80))
    skills_required = db.Column(db.String(500))
    application_deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default="Pending")  # Pending / Approved / Rejected / Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="drive", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "company_name": self.company.name if self.company else None,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "branch_eligibility": self.branch_eligibility,
            "min_cgpa": self.min_cgpa,
            "eligible_year": self.eligible_year,
            "salary": self.salary,
            "skills_required": self.skills_required,
            "application_deadline": self.application_deadline.isoformat() if self.application_deadline else None,
            "status": self.status,
            "applicant_count": len(self.applications) if self.applications else 0,
        }


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drives.id"), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Applied")  # Applied/Shortlisted/Interview/Offer/Rejected/Placed
    feedback = db.Column(db.Text)
    interview_datetime = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint("student_id", "drive_id", name="unique_student_drive"),)

    placement = db.relationship("Placement", backref="application", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student.name if self.student else None,
            "drive_id": self.drive_id,
            "job_title": self.drive.job_title if self.drive else None,
            "company_name": self.drive.company.name if self.drive and self.drive.company else None,
            "application_date": self.application_date.isoformat() if self.application_date else None,
            "status": self.status,
            "feedback": self.feedback,
            "interview_datetime": self.interview_datetime.isoformat() if self.interview_datetime else None,
        }


class Placement(db.Model):
    __tablename__ = "placements"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    position = db.Column(db.String(150))
    salary = db.Column(db.String(80))
    joining_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "student_id": self.student_id,
            "company_id": self.company_id,
            "position": self.position,
            "salary": self.salary,
            "joining_date": self.joining_date.isoformat() if self.joining_date else None,
        }
