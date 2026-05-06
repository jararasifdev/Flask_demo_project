from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.database import db
from app.schemas.schemas import ma
from app.core.config import Config
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp
from app.routes.tags import tags_bp
from app.routes.notes import notes_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    JWTManager(app)
    CORS(app)


    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(tags_bp, url_prefix='/tags')
    app.register_blueprint(notes_bp, url_prefix='/tasks')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    with app.app_context():
        db.create_all()

    return app
