from ..models.schema import SuccessResponseSchema, SuccessResponceToastSchema, ErrorResponseSchema


def responce(succes_schema=None, toast=None):
    if succes_schema is None:
        if toast is None:
            success = SuccessResponseSchema

        else:
            success = SuccessResponceToastSchema
        return {200: success, 400: ErrorResponseSchema}
    else:
        return {200: succes_schema, 400: ErrorResponseSchema}
