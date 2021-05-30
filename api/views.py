from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def ping(request):
    return render(request, 'api/PingTemplate.html')


def random_link(request):
    return JsonResponse({})


def all_links(request):
    return JsonResponse({})


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
