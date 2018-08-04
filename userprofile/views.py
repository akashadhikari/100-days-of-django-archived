from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User

from .models import FollowUser
from .forms import ProfileEditForm
from userprofile.models import Profile
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
    view_blog = Blog.objects.filter(author=user).annotate(count_views=Count('blog_views'))
    final_views_count = 0
    for i in range(blogs_count):
        final_views_count += view_blog[i].count_views

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
        'page_title': user.first_name + '\'s Profile',
        'fullname': full_name,
        'username': username,
        'last_login': last_login,
        'likes_count': likes_count,
        'final_views_count': final_views_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'follow_status': follow_status

    }
    return render(request, "userprofile/profile_home.html", context)


def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user.id)
    full_name = user.first_name + " " + user.last_name
    edit_profile_form = ProfileEditForm(request.POST or None, initial={'first_name': user.first_name,
                                                                       'last_name': user.last_name,
                                                                       'address': profile.location
                                                                       })

    context = {
        'page_title': 'Edit profile',
        'user': user,
        'fullname': full_name,
        'edit_profile_form': edit_profile_form
    }
    if edit_profile_form.is_valid():
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile.location = request.POST.get('address')
        profile.save()
        User.objects.filter(username=username).update(first_name=first_name, last_name=last_name)

    if request.method == 'POST':
        return redirect(reverse('profile:profile', kwargs={'username': username}))
    return render(request, "userprofile/profile_edit.html", context)


def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    FollowUser.objects.create(following=user, followed_by=request.user, is_following=True)
    return redirect(reverse('profile:profile', kwargs={'username': username}))


def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    FollowUser.objects.filter(following=user).filter(followed_by=request.user).first().delete()
    return redirect(reverse('profile:profile', kwargs={'username': username}))
