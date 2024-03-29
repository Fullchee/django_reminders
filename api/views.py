import json
import logging
from operator import itemgetter
from urllib.error import HTTPError

import sqlalchemy as sql
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status

# from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from sqlalchemy.dialects import postgresql

# from .models import Link
from api.serializers import UserSerializer, UserSerializerWithToken
from .helper import parse_keywords, extract_youtube_info, generate_youtube_title
from .responses import JsonResponseServerError, JsonResponseForbidden

logger = logging.getLogger(__name__)


# @api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JsonResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super().__init__(content, **kwargs)


def sql_text(text):
    assert connection.vendor == "postgresql"
    statement = sql.text(text)
    result = str(statement.compile(dialect=postgresql.dialect()))
    return result


def fetchall_as_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# @api_view(['GET'])
def ping(request):
    return render(request, "api/PingTemplate.html")


# @api_view(['GET'])
def get_all_links(request):
    # links = list(Link.objects.filter(user=request.user))
    # return HttpResponse(serialize('json', links), content_type='application/json')
    with connection.cursor() as cursor:
        cursor.execute(sql_text("""SELECT * FROM api_link"""))
        result = fetchall_as_dict(cursor)
        return JsonResponse(result)


# @api_view(['GET'])
def get_random_link(request):
    """
from random import choice

pks = A.objects.values_list('pk', flat=True)
random_pk = choice(pks)
random_obj = A.objects.get(pk=random_pk)

`MyModel.objects.order_by('?').first()` can be very slow
    """
    with connection.cursor() as cursor:
        cursor.execute(
            sql_text(
                """
            SELECT * FROM api_link
            ORDER BY RANDOM()
            LIMIT 1
        """
            )
        )
        result = fetchall_as_dict(cursor)
        return JsonResponse(result[0])


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


# @api_view(['GET'])
def get_link(request, link_id):
    with connection.cursor() as cursor:
        cursor.execute(
            sql_text(
                """
            SELECT *
            FROM api_link
            WHERE id = :link_id
        """
            ),
            {"link_id": link_id},
        )
        result = fetchall_as_dict(cursor)[0]
        if "youtu.be" in result["url"]:
            result["url"] += f"?t={result['start_time'] or 0}"
        result["startTime"] = result["start_time"]
        return JsonResponse(result)


# @api_view(['GET'])
def search(request):
    with connection.cursor() as cursor:
        cursor.execute(
            sql_text(
                """
            SELECT * 
            FROM api_link
            WHERE (
              title ILIKE '%' || :query || '%'
              OR
              notes ILIKE '%' || :query || '%'
              OR
              :query = ANY(keywords)
              )
        """
            ),
            {"query": request.GET.get("q", "")},
        )
        result = fetchall_as_dict(cursor)
        return JsonResponse(result)


def add_or_update(request, action: str, query: str) -> HttpResponse:
    """
    :param request:
    :param action: 'add' or 'update'
    :param query: insert or update query
    """
    body = json.loads(request.body)
    notes, title, url, keywords = itemgetter(
        "notes",
        "title",
        "url",
        "keywords",
    )(body)

    link_id = flag = start_time = None
    if action == "update":
        link_id, flag, start_time = itemgetter("id", "flag", "start_time")(body)

    keywords = parse_keywords(keywords)
    url, youtube_start_time = extract_youtube_info(url)
    try:
        title = title or generate_youtube_title(url)
    except HTTPError as e:
        logger.error(repr(e))
        if e.code == 401:
            error_message = "The YouTube video's author may have disabled playback outside of YouTube"
            logger.error(error_message)
            return JsonResponseForbidden({"message": error_message})
        # return JsonResponseServerError(e)
    except Exception as e:
        return JsonResponseServerError(e)

    # prioritize the form start time over the YouTube URL (which might be outdated)
    start_time = (start_time and int(start_time)) or youtube_start_time or 0

    with connection.cursor() as cursor:
        cursor.execute(
            sql_text(query),
            {
                "id": link_id,
                "notes": notes,
                "title": title,
                "url": url,
                "keywords": keywords,
                "flag": flag,
                "start_time": start_time,
            },
        )
        result = fetchall_as_dict(cursor)[0]
        if "youtu.be" in result["url"]:
            result["url"] += f"?t={result['start_time'] or 0}"
        result["startTime"] = result["start_time"]
        return JsonResponse(result)


@csrf_exempt
# @api_view(['POST', 'PUT'])
def add_link(request):
    # TODO: auth with request.user.id

    # temp measure, the @api_view decorator will do this in the future
    if request.method != "POST" and request.method != "PUT":
        return HttpResponse(status=405)

    INSERT_QUERY = """
        INSERT INTO api_link (id, notes, title, url, keywords, last_accessed, user_id, flag, start_time)
        VALUES (nextval('api_link_id_seq'::regclass), :notes, :title, :url, :keywords, NOW(), 2, FALSE, :start_time)
        ON CONFLICT (url) DO UPDATE SET url = :url
        RETURNING *
    """
    return add_or_update(request, "add", query=INSERT_QUERY)


@csrf_exempt
# @api_view(['POST', 'PUT'])
def update_link(request) -> HttpResponse:
    # TODO: auth with request.user.id

    # temp measure, the @api_view decorator will do this in the future
    if request.method != "POST" and request.method != "PUT":
        return HttpResponse(status=405)
    UPDATE_QUERY = """
        UPDATE api_link
        SET keywords = :keywords,
          title = :title,
          url = :url,
          notes = :notes,
          flag = :flag,
          last_accessed = NOW(),
          start_time = :start_time,
          views =
            CASE last_accessed = CURRENT_DATE
              WHEN TRUE THEN views
              WHEN FALSE THEN views + 1
            END
        WHERE id = :id
        RETURNING *
    """
    return add_or_update(request, "update", query=UPDATE_QUERY)


@csrf_exempt
# @api_view(['POST', 'PUT'])
def delete_link(request) -> HttpResponse:
    if request.method != "POST" and request.method != "PUT":
        return HttpResponse(status=405)
    body = json.loads(request.body)
    link_id = body["id"]
    with connection.cursor() as cursor:
        cursor.execute(
            sql_text(
                """
            DELETE FROM api_link
            WHERE id = :id
            RETURNING :id as id
        """
            ),
            {"id": link_id},
        )
        result = fetchall_as_dict(cursor)
        return JsonResponse(result[0])
