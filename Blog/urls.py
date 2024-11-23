from django.urls import path
from django.urls import re_path
from . import views
from .views import RegistrationView,BlogListCreateView,LoginView



urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),
    path('blog/<int:pk>/', views.blog_edit_delete, name='blog_edit_delete'),
    path("register/",RegistrationView.as_view()),
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),

]
