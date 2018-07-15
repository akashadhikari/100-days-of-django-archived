from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from blog.models import Blog


def profile_page(request, username):
    user = get_object_or_404(User, username=username)
    blogs = Blog.objects.filter(author=user)
    full_name = user.first_name + " " + user.last_name
    last_login = user.last_login
    profile_pic = user.profile.profile_pic
    location = user.profile.location
    context = {
        'user': user,
        'blogs': blogs,
        'fullname': full_name,
        'username': username,
        'last_login': last_login,
        'profile_pic': profile_pic,
        'location': location

    }
    return render(request, "userprofile/profile_home.html", context)
