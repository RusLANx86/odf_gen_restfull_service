"""Schemas."""

from marshmallow import fields, EXCLUDE
from flask_marshmallow import Schema


class UserResponseSchema(Schema):
    """Ответ с данными пользователя."""

    name = fields.String(doc='Наименование')

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE
