from django.db import models
from django.contrib.auth.models import User

from tinymce import models as tinymce_models


# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=255)
    code_description = models.TextField(max_length=1000, null=True, blank=True)
    body = tinymce_models.HTMLField()
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    pass


class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.blog.title

    class Meta:
        unique_together = ('blog', 'user',)
