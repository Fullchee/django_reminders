import logging
from typing import Optional

from django.db import connection
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Link
from api.responses import (
    JsonResponse,
    JsonResponseMethodNotAllowed,
    JsonResponseNotFound,
)
from api.services.link_services import (
    create_link,
    get_random_link,
    search_links,
    update_link,
)
from api.services.raw_sql import fetchall_as_dict, sql_text
from api.services.youtube import calculate_title, calculate_youtube_url

logger = logging.getLogger(__name__)


# @api_view(['GET'])
def redirect_to_frontend(request):
    return render(request, "redirect-to-frontend.html")


# @api_view(['GET'])
def get_keywords(request):
    with connection.cursor() as cursor:
        cursor.execute(
            sql_text(
                """
            SELECT DISTINCT UNNEST(keywords) AS keyword
            FROM api_link
        """
            )
        )
        result = fetchall_as_dict(cursor)
        return JsonResponse(sorted(map(lambda obj: obj["keyword"], result)))


class LinkView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        """TODO: use the typed dict as a type in the Add/Edit serializer"""

        class Meta:
            model = Link
            fields = (
                "id",
                "flag",
                "keywords",
                "last_accessed",
                "notes",
                "title",
                "url",
                "views",
                "start_time",
            )

    def get(self, request: Request, link_id: Optional[int]) -> Response:
        if link_id:
            try:
                link = Link.objects.get(id=link_id)
                return JsonResponse(self.OutputSerializer(link))
            except Link.DoesNotExist:
                return JsonResponseNotFound(
                    {"message": f"No link with provided link ID exists"}
                )
        if request.GET.get("random"):
            link = get_random_link()
            return JsonResponse(self.OutputSerializer(link))

        search_term = request.GET.get("q")
        if search_term:
            links = search_links(search_term)
            return JsonResponse(self.OutputSerializer(links, many=True))

        return JsonResponse(self.OutputSerializer(Link.objects.all(), many=True))

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        keywords = serializers.ArrayField()
        url = serializers.URLField()
        last_accessed = serializers.DateField()
        """TODO: do I need to do anything to get this to auto update?"""
        views = serializers.IntegerField()
        """ TODO: increment by 1"""
        flag = serializers.BooleanField()

        # do we intentionally not include this here
        # so that it doesn't create model instances?
        # class Meta:
        #     model = Link

        # TODO: how to set the url and title?

        def calculate_youtube_url(self, link: Link):
            return calculate_youtube_url(link)

        def calculate_title(self, link: Link):
            return calculate_title(link)

    class UpdateInputSerializer(InputSerializer):
        id = serializers.IntegerField()

    def put(self, request: Request, link_id: Optional[int]) -> Response:
        if link_id:
            serializer = self.UpdateInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            update_link(**serializer.validated_data)
        else:
            serializer = self.InputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            create_link(**serializer.validated_data)

    def delete(self, request: Request, link_id: int) -> Response:
        if not link_id:
            return JsonResponseMethodNotAllowed()
        return JsonResponse({"success": "Deleted link"})
