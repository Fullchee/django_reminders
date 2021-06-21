from django.core import serializers
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views


urlpatterns = [
    path('', views.ping),
    path('links', views.get_all_links),
    path('random-link', views.get_random_link),
    path('keywords', views.get_keywords),
    path('link/<int:link_id>', views.get_link),
    path('search', views.search),
    path('add-link', views.add_link),
    path('update-link', views.update_link),
    path('delete-link', views.delete_link),

    path('token-auth/', obtain_jwt_token),
    path('current_user/', views.current_user),
    path('users/', views.UserList.as_view()),
]
