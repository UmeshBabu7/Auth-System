from django.urls import path, include

api_urls = [
    path('api/users/',include("users.urls")),
]
