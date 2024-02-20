from django.urls import include, path

from . import views, views_sql

urlpatterns = [
    path("", views.redirect_to_frontend),
    path("keywords", views.get_keywords),
    path("v1/links/<int:link_id>", views.LinkView.as_view(), name="link"),
    path("v1/links", views.LinkView.as_view(), name="links"),
    path("tinymce/", include("tinymce.urls")),
    # TODO: deprecate these v0 link endpoints
    path("links", views_sql.get_all_links),
    path("links/<int:link_id>", views_sql.get_link),
    path("link/<int:link_id>", views_sql.get_link),
    path("random-link", views_sql.get_random_link_sql),
    path("search", views_sql.search),
    path("add-link", views_sql.add_link),
    path("update-link", views_sql.update_link_sql),
    path("delete-link", views_sql.delete_link),
    # end of deprecated link endpoints
]
