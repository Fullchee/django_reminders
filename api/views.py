import json
import sqlalchemy as sql

from django.core.serializers import serialize
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from sqlalchemy.dialects import postgresql

from .models import Link
from api.serializers import UserSerializer, UserSerializerWithToken


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
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)


def sql_text(text):
    assert (connection.vendor == "postgresql")
    statement = sql.text(text)
    result = str(statement.compile(dialect=postgresql.dialect()))
    return result


def fetchall_as_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# @api_view(['GET'])
def ping(request):
    return render(request, 'api/PingTemplate.html')


# @api_view(['GET'])
def get_all_links(request):
    # links = list(Link.objects.filter(user=request.user))
    # return HttpResponse(serialize('json', links), content_type='application/json')
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''SELECT * FROM api_link'''))
        result = fetchall_as_dict(cursor)
        return JsonResponse(result)


# @api_view(['GET'])
def get_random_link(request):
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''
            SELECT * FROM api_link
            ORDER BY RANDOM()
            LIMIT 1
        '''))
        result = fetchall_as_dict(cursor)
        return JsonResponse(result[0])


# @api_view(['GET'])
def get_keywords(request):
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''
            SELECT DISTINCT UNNEST(keywords) AS keyword
            FROM api_link
        '''))
        result = fetchall_as_dict(cursor)
        return JsonResponse(sorted(map(lambda obj: obj['keyword'], result)))


# @api_view(['GET'])
def get_link(request, link_id):
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''
            SELECT *
            FROM api_link
            WHERE id = :link_id
        '''), {
            'link_id': link_id
        })
        result = fetchall_as_dict(cursor)
        return JsonResponse(result[0])


# @api_view(['GET'])
def search(request):
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''
            SELECT * 
            FROM api_link
            WHERE (title LIKE '%' || :query || '%' OR notes LIKE '%' || :query || '%')
        '''), {
            'query': request.GET.get('q', '')
        })
        result = fetchall_as_dict(cursor)
        return JsonResponse(result)


@csrf_exempt
# @api_view(['POST', 'PUT'])
def add_link(request):
    # request.user.id
    body = json.loads(request.body)
    notes, title, url, keywords = itemgetter('notes', 'title', 'url', 'keywords')(body)

    keywords = [] if keywords == '' else keywords.split(',')

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(sql_text('''
                INSERT INTO api_link (id, notes, title, url, keywords, last_accessed, user_id)
                VALUES (nextval('api_link_id_seq'::regclass), :notes, :title, :url, :keywords, NOW(), 2)
                RETURNING id
            '''), {
                'notes': notes,
                'title': title,
                'url': url,
                'keywords': keywords,
            })
            result = fetchall_as_dict(cursor)
            return JsonResponse(result[0])


@csrf_exempt
# @api_view(['POST', 'PUT'])
def delete_link(request):
    body = json.loads(request.body)
    link_id = body['id']
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''
            DELETE FROM api_link
            WHERE id = :id
            RETURNING :id as id
        '''), {
            'id': link_id
        })
        result = fetchall_as_dict(cursor)
        return JsonResponse(result[0])


@csrf_exempt
# @api_view(['POST', 'PUT'])
def update_link(request):
    body = json.loads(request.body)
    link_id, notes, title, url, keywords = itemgetter('id', 'notes', 'title', 'url', 'keywords')(body)

    keywords = [] if keywords == '' else keywords.split(',')

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(sql_text('''
                UPDATE api_link
                SET keywords = :keywords, title = :title, url = :url, notes = :notes, last_accessed = NOW(), views = views + 1
                WHERE id = :id
            '''), {
                'id': link_id,
                'notes': notes,
                'title': title,
                'url': url,
                'keywords': keywords,
            })
            return JsonResponse({'status': "success", 'id': link_id, 'message': "Link updated"})
