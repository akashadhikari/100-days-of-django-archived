from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
