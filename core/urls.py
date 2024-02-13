from django.urls import path
from core.views import Register, Login, main

urlpatterns = [
    path('public/u/register', Register, name="Register"),
    path('public/u/login', Login, name="Login"),
    path('u/apps', main, name="App")
]
