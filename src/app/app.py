"""App."""

from flask import Flask, render_template


def internal_server_error(e):
    return 'Server error', 500


def get_app(config) -> Flask:
    """Get flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    from flask_marshmallow import Marshmallow
    Marshmallow(app)

    from flasgger import Swagger
    Swagger(app)

    from .api import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint.obj, url_prefix = blueprint.url_prefix)

    app.register_error_handler(Exception, internal_server_error)


    from sqlalchemy import create_engine
    from .models.map import Base
    Base.metadata.create_all(create_engine(app.config.get('DB_URI', '')))

    return app
