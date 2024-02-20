import json
from operator import itemgetter
from urllib.error import HTTPError

from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.responses import JsonResponse, JsonResponseForbidden, JsonResponseServerError
from api.services.raw_sql import fetchall_as_dict, sql_text
from api.services.youtube import extract_youtube_info, generate_youtube_title


# @api_view(['GET'])
def get_all_links(request):
    # links = list(Link.objects.filter(user=request.user))
    # return HttpResponse(serialize('json', links), content_type='application/json')
    with connection.cursor() as cursor:
        cursor.execute(sql_text("""SELECT * FROM api_link"""))
        result = fetchall_as_dict(cursor)
        return JsonResponse(result)


# @api_view(['GET'])
def get_random_link_sql(request):
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
    return add_or_update(json.loads(request.body), "add", query=INSERT_QUERY)


@csrf_exempt
# @api_view(['POST', 'PUT'])
def update_link_sql(request) -> HttpResponse:
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
    return add_or_update(json.loads(request.body), "update", query=UPDATE_QUERY)


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


def add_or_update(body, action: str, query: str) -> HttpResponse:
    """
    :param body:
    :param action: 'add' or 'update'
    :param query: insert or update query
    """
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
        logger.error(e)
        return JsonResponseServerError()

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


def parse_keywords(keywords):
    """
    TODO: the backend will deal with arrays of keywords, the frontend component will transform the data

    >>> parse_keywords([{"value": "keyword1"}, {"value": "keyword2"}])
    ["keyword1", "keyword2"]
    """
    return list(map(lambda keyword: keyword["value"], keywords))
