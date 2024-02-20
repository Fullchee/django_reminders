import gzip
from typing import NotRequired, Optional, TypedDict

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class ErrorObject(TypedDict):
    title: NotRequired[str]
    message: str


class JsonResponse(HttpResponse):
    """
    TODO: does DRF have built-in versions of these responses?
    """

    def __init__(self, data, *, use_gzip=False, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        if use_gzip:
            content = gzip.compress(content)

        super().__init__(content, **kwargs)

        if use_gzip:
            self["Content-Encoding"] = "gzip"


class JsonResponseBadRequest(JsonResponse):
    """JSON 400 error"""

    def __init__(self, data: Optional[ErrorObject] = None, **kwargs):
        if data is None:
            data = {}
        data.setdefault("message", "Bad request")
        super().__init__({"error": data}, status=400, **kwargs)


class JsonResponseForbidden(JsonResponse):
    """JSON 403 error"""

    def __init__(self, data: Optional[ErrorObject] = None, **kwargs):
        if data is None:
            data = {}
        data.setdefault("message", "Forbidden")
        super().__init__({"error": data}, status=403, **kwargs)


class JsonResponseNotFound(JsonResponse):
    """JSON 404 error"""

    def __init__(self, data: Optional[ErrorObject] = None, **kwargs):
        if data is None:
            data = {}
        data.setdefault("message", "Not found")
        super().__init__({"error": data}, status=404, **kwargs)


class JsonResponseServerError(JsonResponse):
    """Generic 500 error"""

    def __init__(self, data: Optional[ErrorObject] = None, **kwargs):
        if data is None:
            data = {}
        data.setdefault("message", "Internal server error")
        super().__init__({"error": data}, status=500, **kwargs)
