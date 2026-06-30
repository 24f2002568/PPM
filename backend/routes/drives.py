from flask import Blueprint, request, jsonify

from models import db, Drive, Company
from routes.utils import role_required

drives_bp = Blueprint("drives", __name__)


@drives_bp.route("", methods=["GET"])
@role_required("student", "admin")
def list_approved_drives():
    """Students see approved/open drives; supports search by company, title, or skills."""
    search = request.args.get("search", "").strip()
    query = Drive.query.filter_by(status="Approved").join(Company)

    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Drive.job_title.ilike(like),
                Drive.skills_required.ilike(like),
                Company.name.ilike(like),
            )
        )

    drives = query.all()
    return jsonify([d.to_dict() for d in drives]), 200


@drives_bp.route("/<int:drive_id>", methods=["GET"])
@role_required("student", "admin")
def get_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    return jsonify(drive.to_dict()), 200
