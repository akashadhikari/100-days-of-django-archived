import datetime
from django.db import models
from django.contrib.auth.models import User

from tinymce import models as tinymce_models


# Create your models here.


class Blog(models.Model):
    visibility = models.BooleanField(default=True) # True visibility means Public
    title = models.CharField(max_length=255, default="Untitled")
    code_description = models.TextField(max_length=1000, null=True, blank=True, default="No description provided.")
    body = tinymce_models.HTMLField()
    author = models.ForeignKey(User, null=True, blank=True, related_name='author', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BlogView(models.Model):
    blog = models.ForeignKey(Blog, related_name='blog_views', on_delete=models.CASCADE)
    ip = models.CharField(max_length=40, null=True, blank=True)
    session = models.CharField(max_length=40, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog.title


class Comment(models.Model):
    parent_blog = models.ForeignKey(Blog, related_name='comment_on', on_delete=models.CASCADE)
    # comment = models.TextField(max_length=1000, null=True, blank=True)
    comment = tinymce_models.HTMLField()
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.blog.title

    class Meta:
        unique_together = ('blog', 'user',)
