from django.shortcuts import render, get_object_or_404

from .forms import SearchForm
from .models import Post, Category
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger


def post_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    object_list = Post.published.all()
    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug)
        object_list = object_list.filter(category=category)
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'category': category,
                   'categories': categories,
                   })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['q']
            results = Post.published.filter(title__icontains=query)
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
