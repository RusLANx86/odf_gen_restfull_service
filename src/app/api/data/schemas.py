"""Schemas."""

from marshmallow import fields, EXCLUDE
from flask_marshmallow import Schema


class DataResponseSchema(Schema):
    """Ответ с данными."""

    id = fields.String(doc='Идентификатор')
    created_utc = fields.String(doc='Дата и время создания')
    updated_utc = fields.String(doc='Дата и время обновления')
    value = fields.String(doc='Значение')

    class Meta:
        """Meta."""

        strict = True


class DataPageResponseSchema(Schema):
    """Ответ со страницей данных."""

    page_items = fields.Nested(DataResponseSchema, many=True, doc='Страница данных')
    page_offset = fields.Integer(required=True, default=1, doc='Номер страницы')
    page_limit = fields.Integer(required=True, default=10, doc='Размер страницы')

    class Meta:
        """Meta."""

        strict = True


class DataPageQuerySchema(Schema):
    """Запрос страницы данных."""

    page_offset = fields.Int(required=False, default=1, doc='Номер страницы')
    page_limit = fields.Int(required=False, default=10, doc='Размер страницы')

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE


class DataGetQuerySchema(Schema):
    """Запрос получения данных."""

    id = fields.String(required=True, doc='Идентификатор')

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE 


class DataCreateCommandSchema(Schema):
    """Команда создания данных."""

    value = fields.String(required=True, doc='Значение')

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE


class DataUpdateQuerySchema(Schema):
    """Запрос обновления данных."""

    id = fields.String(required=True, doc='Идентификатор')

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE 


class DataUpdateCommandSchema(Schema):
    """Команда обновления данных."""

    value = fields.String(required=True, doc='Значение')

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE


class DataDeleteQuerySchema(Schema):
    """Запрос удаления данных."""

    id = fields.String(required=True, doc='Идентификатор')

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE
