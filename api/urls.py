from django.urls import path
from . import views

urlpatterns = [
    path('', views.ping),
    path('links', views.get_all_links),
]