from flask import Flask
from dotenv import load_dotenv
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE_URL="postgresql://oscar:@localhost:5432/booknook",
    )

    if test_config:
        app.config.update(test_config)

    # DB
    from . import db
    db.init_app(app)

    # Controllers
    from .controllers.book_controller import bp as book_bp
    from .controllers.auth_controller import bp as auth_bp

    app.register_blueprint(book_bp)
    app.register_blueprint(auth_bp)

    return app