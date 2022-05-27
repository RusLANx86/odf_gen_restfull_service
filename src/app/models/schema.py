"""Schemas."""

#region imports

from marshmallow import fields
from flask_marshmallow import Schema
 
#endregion


class SuccessResponseSchema(Schema):
    """Ответ при успешном выполнении запроса."""

    class Meta:
        """Meta."""

        strict = True

    msg = fields.String(doc='Сообщение')
    data = fields.Dict(doc='Данные')


class SuccessResponceToastSchema(Schema):

    detail = fields.String(default='Успешно', doc='Развернутое описание ответа')
    summary = fields.String(default=' ', doc='Общий ответ')
    severity = fields.String(default='success', doc='Тип сообщения')
    content = fields.String(default='')
    life = fields.Integer(default=3)


class ErrorItemResponseSchema(Schema):
    """Ошибка запроса."""

    class Meta:
        """Meta."""

        strict = True

    id = fields.String(doc='Идентификатор')
    msg = fields.String(doc='Сообщение')
    detail = fields.String(doc='Описание')


class ErrorResponseSchema(Schema):
    """Ответ при неправильном выполнении запроса."""

    class Meta:
        """Meta."""

        strict = True

    msg = fields.String(doc='Сообщение')
    errors = fields.Nested(ErrorItemResponseSchema, many=True, doc='Ошибки')
