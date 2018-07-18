from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Blog, Like
from .forms import BlogForm

# Create your views here.


def blogs_list(request):
    blogs = Blog.objects.all().order_by('-id')
    context = {
        "page_title": "TheShelve",
        "blogs": blogs,
    }
    return render(request, "blog/list.html", context)


def blog_create(request):
    blog_form = BlogForm(request.POST or None)

    context = {
        "page_title": "New Showpiece - TheShelve",
        "form": blog_form,
    }
    if blog_form.is_valid():
        title = request.POST.get('title')
        body = request.POST.get('content')
        new_blog = Blog.objects.create(title=title, body=body)
        new_blog.author = request.user
        new_blog.save()
    if request.method == 'POST':
        return redirect(reverse('blog:detail', kwargs={'pk': Blog.objects.last().id}))
    return render(request, "blog/create.html", context)


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    page_title = blog.title + '- TheShelve'
    if blog.author:
        author = blog.author.first_name + " " + blog.author.last_name
        blog_author = True
    else:
        author = "A user"
        blog_author = False
    if request.user.is_authenticated:
        like = Like.objects.filter(blog=pk).filter(user=request.user).first()
        like_count = Like.objects.filter(blog=pk).count()
        likers = Like.objects.values_list('user__username', flat=True).filter(blog=pk)

    else:
        like = ''
        like_count = ''
        likers = ''
    context = {
        'blog': blog,
        'page_title': page_title,
        'author': author,
        'like': like,
        'like_count': like_count,
        'likers': likers,
        'blog_author': blog_author
    }

    return render(request, "blog/detail.html", context)


def blog_edit(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    edit_form = BlogForm(request.POST or None, initial={'title': blog.title, 'content': blog.body})
    context = {
        'form': edit_form,
        'page_title': 'Edit Showpiece - TheShelve'
    }
    if edit_form.is_valid():
        title = request.POST.get('title')
        body = request.POST.get('content')
        Blog.objects.filter(id=pk).update(title=title, body=body)
    if request.method == 'POST':
        return redirect(reverse('blog:detail', kwargs={'pk': blog.id}))

    return render(request, 'blog/edit.html', context)


def blog_delete(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    blog.delete()
    return redirect(reverse('blog:list'))


def like_trigger(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    Like.objects.create(blog=blog, user=request.user, like=True)
    return redirect(reverse('blog:detail', kwargs={'pk': blog.id}))


def unlike_trigger(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    like = Like.objects.filter(blog=pk).filter(user=request.user).first()
    like.delete()
    return redirect(reverse('blog:detail', kwargs={'pk': blog.id}))