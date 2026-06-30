from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    CORS(app)

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.company import company_bp
    from routes.student import student_bp
    from routes.drives import drives_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(company_bp, url_prefix="/api/company")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(drives_bp, url_prefix="/api/drives")

    with app.app_context():
        db.create_all()
        seed_admin()

    return app


def seed_admin():
    """Pre-create the single admin user programmatically, as required."""
    if not User.query.filter_by(role="admin").first():
        admin = User(email="admin@ppa.com", role="admin", is_active=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Seeded admin user: admin@ppa.com / admin123")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
