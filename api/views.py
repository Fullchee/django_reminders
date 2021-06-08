from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from rest_framework.renderers import JSONRenderer
import sqlalchemy as sql
from sqlalchemy.dialects import postgresql
import psycopg2.sql


class JsonResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)


def sql_text(text):
    assert(connection.vendor == "postgresql")
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


def random_link(request):
    return JsonResponse({})


def get_all_links(request):
    with connection.cursor() as cursor:
        cursor.execute(sql_text('''SELECT * FROM api_link'''))
        result = fetchall_as_dict(cursor)
        return JsonResponse(result)


def keywords(request):
    return JsonResponse({})


def link(request):
    return JsonResponse({})


def search(request):
    return JsonResponse({})


def add_link(request):
    return JsonResponse({})


def delete_link(request):
    return JsonResponse({})


def update_link(request):
    return JsonResponse({})
