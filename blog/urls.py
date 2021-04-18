from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    # post views
    path('blog/feed/', LatestPostsFeed(), name='post_feed'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('blog/search/', views.post_search, name='post-search'),
    path('blog/add/', views.CreateArticle.as_view(), name='post-article'),
    path('blog/<str:category_slug>/', views.PostListView.as_view(), name='post_list_by_category'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),



]
