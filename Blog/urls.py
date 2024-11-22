from django.urls import path
from django.urls import re_path
from . import views
from .views import RegistrationView,BlogListCreateView,LoginView



urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),

    path("register/",RegistrationView.as_view()),
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),

]
