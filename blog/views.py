from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Blog
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
        Blog.objects.create(title=title, body=body)
    if request.method == 'POST':
        return redirect(reverse('blog:detail', kwargs={'pk': Blog.objects.last().id}))
    return render(request, "blog/create.html", context)


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    page_title = blog.title + '- TheShevle'
    context = {
        'blog': blog,
        'page_title': page_title
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
