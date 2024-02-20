from random import choice

from django.db.models import Q

from api.models import Link


def get_random_link() -> Link:
    """
    Guaranteed to not throw, the first migration will create the sample data
    `Link.objects.order_by('?').first()` can be very slow
    """
    pks = Link.objects.values_list("pk", flat=True)
    random_pk = choice(pks)
    return Link.objects.get(pk=random_pk)


def search_links(search_term: str) -> "QuerySet[Link]":
    """
    TODO: add django-stubs
    poetry install django-stubs --group dev
    TODO: postgres search
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
    return Link.objects.filter(
        Q(question__startswith="Who") | Q(question__startswith="What")
    )


def update_link(link):
    """

    TODO: create a type for link Partial<dict version of Link>

    TODO: can I use the output serializer return value?

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
    pass
