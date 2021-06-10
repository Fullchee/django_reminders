from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from rest_framework.renderers import JSONRenderer
import sqlalchemy as sql
from sqlalchemy.dialects import postgresql
import psycopg2.sql
import json
from operator import itemgetter
from django.views.decorators.csrf import csrf_exempt
from .models import Link


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


def ping(request):
    return render(request, 'api/PingTemplate.html')


def get_random_link(request):
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''
            SELECT * FROM api_link
            ORDER BY RANDOM()
            LIMIT 1
        '''))
        result = fetchall_as_dict(cursor)
        return JsonResponse(result[0])


def get_all_links(request):
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''SELECT * FROM api_link'''))
        result = fetchall_as_dict(cursor)
        return JsonResponse(result)


def get_keywords(request):
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''
            SELECT DISTINCT UNNEST(keywords) AS keyword
            FROM api_link
        '''))
        result = fetchall_as_dict(cursor)
        return JsonResponse(sorted(map(lambda obj: obj['keyword'], result)))


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
def add_link(request):
    # request.user.id
    body = json.loads(request.body)
    notes, title, url, keywords = itemgetter('notes', 'title', 'url', 'keywords')(body)

    keywords = [] if keywords == '' else keywords.split(',')

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(sql_text('''
                INSERT INTO api_link (id, notes, title, url, keywords, last_accessed)
                VALUES (nextval('api_link_id_seq'::regclass), :notes, :title, :url, :keywords, NOW())
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
def delete_link(request):
    body = json.loads(request.body)
    link_id = body['id']
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(sql_text('''
                DELETE FROM api_link
                WHERE id = :id
            '''), {
                'id': link_id
            })
            result = fetchall_as_dict(cursor)
            return JsonResponse(result[0])


@csrf_exempt
def update_link(request):
    body = json.loads(request.body)
    link_id, notes, title, url, keywords = itemgetter('id', 'notes', 'title', 'url', 'keywords')(body)

    keywords = [] if keywords == '' else keywords.split(',')

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(sql_text('''
                UPDATE api_link
                SET keywords = :keywords, title = :title, url = :url, notes = :notes, last_accessed = NOW()
                WHERE id = :id
            '''), {
                'id': link_id,
                'notes': notes,
                'title': title,
                'url': url,
                'keywords': keywords,
            })
            result = fetchall_as_dict(cursor)
            return JsonResponse({'status': "success", id: id, 'message': "Link updated"})
