from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User

from .models import FollowUser
from blog.models import Blog


def profile_page(request, username):
    user = get_object_or_404(User, username=username)
    blogs = Blog.objects.filter(author=user)
    full_name = user.first_name + " " + user.last_name
    last_login = user.last_login
    profile_pic = user.profile.profile_pic
    location = user.profile.location
    followers_count = FollowUser.objects.filter(following=user).count()
    qs = FollowUser.objects.filter(following=user).filter(followed_by=request.user)
    if qs.count() == 1:
        follow_status = qs.first().is_following
    else:
        follow_status = False

    context = {
        'user': user,
        'blogs': blogs,
        'fullname': full_name,
        'username': username,
        'last_login': last_login,
        'profile_pic': profile_pic,
        'location': location,
        'followers_count': followers_count,
        'follow_status': follow_status,

    }
    return render(request, "userprofile/profile_home.html", context)


def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    FollowUser.objects.create(following=user, followed_by=request.user, is_following=True)
    return redirect(reverse('profile:profile', kwargs={'username': username}))
