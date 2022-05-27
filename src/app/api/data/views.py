"""Views."""

import uuid
import datetime

from flask import Blueprint, request
from flask.views import MethodView
from sqlalchemy.sql import select, desc

from . import service as data_service
from . import schemas as data_schemas
from ...models import schema as base_schemas
from ...tools.flasgger_marshmallow import swagger_decorator
from ...session import session_scope


data_blueprint = Blueprint('Data', __name__)
blueprint_name = data_blueprint.name


class DataPage(MethodView):
    """Data page."""

    @swagger_decorator(query_schema=data_schemas.DataPageQuerySchema, response_schema={200: data_schemas.DataPageResponseSchema, 400: base_schemas.ErrorResponseSchema}, blueprint_name=blueprint_name)
    def get(self):
        """Получение страницы данных."""
        page_offset = request.query_schema['page_offset']
        page_limit = request.query_schema['page_limit']
        with session_scope() as session:
            page = data_service.get_page(session, page_offset, page_limit)
        return {"page_offset": page_offset, "page_limit": page_limit, "page_items": data_schemas.DataResponseSchema(many=True).dump(page)}


class DataGet(MethodView):
    """Data get."""

    @swagger_decorator(path_schema=data_schemas.DataGetQuerySchema, response_schema={200: data_schemas.DataResponseSchema, 400: base_schemas.ErrorResponseSchema}, blueprint_name=blueprint_name)
    def get(self, id: str):
        """Получение данных."""
        with session_scope() as session:
            item = data_service.get_item(session, id)
        result = data_schemas.DataResponseSchema().dump(item)
        return result


class DataCreate(MethodView):
    """Data create."""

    @swagger_decorator(json_schema=data_schemas.DataCreateCommandSchema, response_schema={200: base_schemas.SuccessResponseSchema, 400: base_schemas.ErrorResponseSchema}, blueprint_name=blueprint_name)
    def post(self):
        """Создание данных."""
        value = request.json_schema["value"]
        with session_scope() as session:
            id = data_service.create_item(session, value)
        return {"msg": "Данные созданы", "data": {"id": id}}


class DataUpdate(MethodView):
    """Data update."""

    @swagger_decorator(path_schema=data_schemas.DataUpdateQuerySchema, json_schema=data_schemas.DataUpdateCommandSchema, response_schema={200: base_schemas.SuccessResponseSchema, 400: base_schemas.ErrorResponseSchema}, blueprint_name=blueprint_name)
    def put(self, id: str):
        """Oбновление данных."""
        value = request.json_schema["value"]
        with session_scope() as session:
            data_service.update_item(session, id, value)
        return {"msg": "ok"}


class DataDelete(MethodView):
    """Data delete."""

    @swagger_decorator(path_schema=data_schemas.DataDeleteQuerySchema, response_schema={200: base_schemas.SuccessResponseSchema, 400: base_schemas.ErrorResponseSchema}, blueprint_name=blueprint_name)
    def delete(self, id: str):
        """Удаление данных."""
        with session_scope() as session:
            data_service.delete_item(session, id)
        return {"msg": "ok"}


data_blueprint.add_url_rule('/', view_func=DataPage.as_view("datapage_api"))
data_blueprint.add_url_rule('/<string:id>', view_func=DataGet.as_view("dataget_api"))
data_blueprint.add_url_rule('/', view_func=DataCreate.as_view("datacreate_api"))
data_blueprint.add_url_rule('/<string:id>', view_func=DataUpdate.as_view("dataupdate_api"))
data_blueprint.add_url_rule('/<string:id>', view_func=DataDelete.as_view("datadelete_api"))
