from django.db import models


class blog(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)