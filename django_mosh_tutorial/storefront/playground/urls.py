from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('hellohtml/', views.say_hello_html),
]