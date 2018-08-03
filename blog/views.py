from datetime import datetime, timedelta

from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Blog, Like, BlogView, Comment
from userprofile.models import FollowUser
from .forms import BlogForm, CommentForm

# Create your views here.


def home(request):
    init = """<pre class="language-python"><code>

</code></pre>"""
    is_auth = request.user.is_authenticated
    blogs = Blog.objects.filter(visibility=True).order_by('-created_at')[:5]
    blog_form = BlogForm(request.POST or None, initial={'content': init, 'visibility': is_auth})

    all_views = Blog.objects.all().annotate(count_views=Count('blog_views'))
    start_date = timezone.now()

    trending_list = all_views.order_by('-count_views').filter(created_at__gte=start_date-timedelta(days=6))[:5]

    context = {
        "page_title": "Snippcode",
        "blogs": blogs,
        "blog_form": blog_form,
        "trending_list": trending_list
    }
    if blog_form.is_valid():
        title = request.POST.get('title')
        code_description = request.POST.get('code_description')
        body = request.POST.get('content')
        visibility = request.POST.get('visibility')
        new_blog = Blog.objects.create(title=title, visibility=visibility, code_description=code_description, body=body)
        if request.user.is_authenticated:
            new_blog.author = request.user
        new_blog.save()
        if request.method == 'POST':
            return redirect(reverse('blog:detail', kwargs={'pk': Blog.objects.last().id}))
    return render(request, "blog/list.html", context)


def blogs_following_list(request):
    if request.user.is_authenticated:
        blogs_following = Blog.objects.filter(visibility=True).order_by('-created_at')
        context = {
            'blogs_following': blogs_following,
            'page_title': 'Following Feed'
        }
        # Blog.objects.filter(author=FollowUser.objects.filter(followed_by=request.user))
        return render(request, "blog/following_list.html", context)
    else:
        return redirect(reverse('userauth:login'))


def blog_create(request):
    init = """<pre class="language-python"><code>

</code></pre>"""
    is_auth = request.user.is_authenticated
    blog_form = BlogForm(request.POST or None, initial={'content':init, 'visibility': is_auth})

    context = {
        "page_title": "New Snippcode",
        "form": blog_form,
    }
    if blog_form.is_valid():
        title = request.POST.get('title')
        code_description = request.POST.get('code_description')
        body = request.POST.get('content')
        visibility = request.POST.get('visibility')
        new_blog = Blog.objects.create(title=title, visibility=visibility, code_description=code_description, body=body)
        if request.user.is_authenticated:
            new_blog.author = request.user
        new_blog.save()
        if request.method == 'POST':
            return redirect(reverse('blog:detail', kwargs={'pk': Blog.objects.last().id}))
    return render(request, "blog/create.html", context)


def blog_detail(request, pk):

    blog_all = get_object_or_404(Blog, id=pk)
    if request.user == blog_all.author:
        blog = get_object_or_404(Blog, id=pk)
    else:
        blog = get_object_or_404(Blog.objects.filter(visibility=True), id=pk)

    page_title = blog.title + '- Snippcode'

    if blog.author:
        author = blog.author.first_name + " " + blog.author.last_name
        blog_author = True

    else:
        author, blog_author = "A man has no name.", False

    if request.user.is_authenticated:
        like = Like.objects.filter(blog=pk).filter(user=request.user).first()
        like_count = Like.objects.filter(blog=pk).count()
        likers = Like.objects.values_list('user__username', flat=True).filter(blog=pk)

    else:
        like, like_count, likers = ''

    # Count views

    # if not ORM filter (blog, session)

    view = BlogView(blog=blog,
                    ip=request.META['REMOTE_ADDR'],
                    created=datetime.now(),
                    session=request.session.session_key)
    view.save()

    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        comment = request.POST.get('comment')
        author = request.user
        Comment.objects.create(parent_blog=blog, comment=comment, author=author)
        if request.method == 'POST':
            return redirect(reverse('blog:detail', kwargs={'pk': pk}))
    comments = Comment.objects.filter(parent_blog=blog).order_by('-created_at')

    context = {
        'blog': blog,
        'view_count': BlogView.objects.filter(blog=blog).count(),
        'page_title': page_title,
        'author': author,
        'like': like,
        'like_count': like_count,
        'likers': likers,
        'blog_author': blog_author,
        'comment_form': comment_form,
        'comments': comments
    }

    return render(request, "blog/detail.html", context)


def blog_edit(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    edit_form = BlogForm(request.POST or None, initial={'title': blog.title,
                                                        'code_description':blog.code_description,
                                                        'content': blog.body,
                                                        'visibility': blog.visibility})
    context = {
        'form': edit_form,
        'page_title': 'Edit Snippcode - Snippcode'
    }
    if edit_form.is_valid():
        title = request.POST.get('title')
        code_description = request.POST.get('code_description')
        body = request.POST.get('content')
        visibility = request.POST.get('visibility')
        Blog.objects.filter(id=pk).update(title=title, visibility=visibility, code_description=code_description, body=body)
    if request.method == 'POST':
        return redirect(reverse('blog:detail', kwargs={'pk': blog.id}))

    return render(request, 'blog/edit.html', context)


def blog_delete(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    if request.user.is_authenticated and request.user == blog.author:
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
