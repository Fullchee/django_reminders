from django.db import connection
from sqlalchemy.dialects import postgresql


def sql_text(text):
    assert connection.vendor == "postgresql"
    statement = sql.text(text)
    result = str(statement.compile(dialect=postgresql.dialect()))
    return result


def fetchall_as_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
