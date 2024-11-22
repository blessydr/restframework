
from django.contrib import admin
from django.urls import path,include
from Blog.views import RegistrationView

urlpatterns = [
    path('blog',include('Blog.urls'))
]
