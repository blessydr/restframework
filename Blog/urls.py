from django.urls import path
from django.urls import re_path
from . import views



urlpatterns = [
    path('',views.getData),
    path('add/',views.add_blog),
    path ('hi',views.example_view),
    re_path('login',views.login),
    re_path('signup',views.signup),
    re_path('test',views.test_token),
]
