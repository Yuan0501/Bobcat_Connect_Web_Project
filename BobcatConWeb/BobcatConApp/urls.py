from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('search_people', views.search_people, name='search_people'),
    path('search_roommates', views.search_roommates, name='search_roommates')
]