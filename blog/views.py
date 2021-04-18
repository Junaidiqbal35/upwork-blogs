from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView

from .forms import SearchForm, PostForm
from .models import Post, Category
import feedparser


class CreateArticle(CreateView):
    model = Post
    template_name = 'blog/post/add_article.html'
    form_class = PostForm

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        return super(CreateArticle, self).form_valid(form)


# def post_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     object_list = Post.published.all()
#     if category_slug:
#         category = get_object_or_404(Category, category_slug=category_slug)
#         object_list = object_list.filter(category=category)
#     paginator = Paginator(object_list, 3)  # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/post/list.html',
#                   {'page': page,
#                    'posts': posts,
#                    'category': category,
#                    'categories': categories,
#                    })


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):

        category_slug = self.kwargs.get('category_slug')
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        if category_slug:
            category = get_object_or_404(Category, category_name__icontains=self.kwargs['category_slug'])
            context['category'] = self.model.objects.filter(category=category)

        else:
            context['object_list'] = self.model.objects.all()
            context['feed'] = feedparser.parse("https://www.cert.ssi.gouv.fr/feed/")

        return context


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
