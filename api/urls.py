from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.redirect_to_frontend),
    path("keywords", views.get_keywords),
    path("v1/links/<int:link_id>", views.LinkView.as_view(), name="link"),
    path("v1/links", views.LinkView.as_view(), name="links"),

    # TODO: deprecate these v0 link endpoints
    path("links", views.get_all_links),
    path("links/<int:link_id>", views.get_link),
    path("link/<int:link_id>", views.get_link),
    path("random-link", views.get_random_link_sql),
    path("search", views.search),
    path("add-link", views.add_link),
    path("update-link", views.update_link),
    path("delete-link", views.delete_link),
    # end of deprecated link endpoints
]
