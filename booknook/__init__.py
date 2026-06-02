from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="booknook.sqlite",
    )

    if test_config:
        app.config.update(test_config)

    # DB setup
    from . import db
    db.init_app(app)

    # Blueprints
    from . import auth, books
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)

    return app