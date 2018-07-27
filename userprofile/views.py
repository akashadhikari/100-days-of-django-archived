from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User

from .models import FollowUser
from blog.models import Blog, Like


def profile_page(request, username):
    user = get_object_or_404(User, username=username)
    blogs = Blog.objects.filter(author=user).order_by('-created_at')
    blogs_count = blogs.count()
    full_name = user.first_name + " " + user.last_name
    last_login = user.last_login
    likes_count = Like.objects.filter(user=user).count()
    followers_count = FollowUser.objects.filter(following=user).count()
    following_count = FollowUser.objects.filter(followed_by=user).count()
    if request.user.is_authenticated:
        qs = FollowUser.objects.filter(following=user).filter(followed_by=request.user)
        if qs.count() == 1:
            follow_status = qs.first().is_following
        else:
            follow_status = False
    else:
        qs, follow_status = None, False

    context = {
        'user': user,
        'blogs': blogs,
        'blogs_count': blogs_count,
        'fullname': full_name,
        'username': username,
        'last_login': last_login,
        'likes_count': likes_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'follow_status': follow_status,

    }
    return render(request, "userprofile/profile_home.html", context)


def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    FollowUser.objects.create(following=user, followed_by=request.user, is_following=True)
    return redirect(reverse('profile:profile', kwargs={'username': username}))


def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    FollowUser.objects.filter(following=user).filter(followed_by=request.user).first().delete()
    return redirect(reverse('profile:profile', kwargs={'username': username}))
