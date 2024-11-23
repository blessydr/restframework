from django.db import models
from django.contrib.auth.models import User
# blog/models.py

from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="blogs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Approved')
    def __str__(self):
        return self.title
