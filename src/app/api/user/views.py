"""Views."""

from flask import Blueprint
from flask.views import MethodView
from sqlalchemy.sql import func, select

from . import schemas as user_schemas
from ...models import schema as base_schemas
from ...tools.flasgger_marshmallow import swagger_decorator
from ...session import session_scope


user_blueprint = Blueprint('User', __name__)
blueprint_name = user_blueprint.name

class UserCurrentGet(MethodView):
    """Get user current."""

    @swagger_decorator(response_schema={200: user_schemas.UserResponseSchema, 400: base_schemas.ErrorResponseSchema}, blueprint_name=blueprint_name)
    def get(self):
        """Получение информации о текущем пользователе."""
        with session_scope() as session:
            name = session.execute(select([func.current_user()])).fetchone()[0]
        return {"name": name}


user_blueprint.add_url_rule('/current', view_func=UserCurrentGet.as_view("user_current_api"))
