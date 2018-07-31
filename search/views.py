from django.db.models import Q
from django.shortcuts import render

from blog.models import Blog


# Create your views here.


def search_list(request):
    query = request.GET.get('q')
    if query is not '':
        lookups = Q(title__icontains=query) | \
                  Q(code_description__icontains=query) | \
                  Q(body__icontains=query)
        blogs = Blog.objects.filter(lookups).order_by('-id')
    else:
        blogs = Blog.objects.none()
    context = {
        "page_title": "Snippcode",
        "blogs": blogs,
    }
    return render(request, "search/list.html", context)
