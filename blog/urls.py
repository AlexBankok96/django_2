# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blog_post_list'),
    path('post/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('create/', views.BlogPostCreateView.as_view(), name='blog_post_create'),
    path('update/<slug:slug>/', views.BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('delete/<slug:slug>/', views.BlogPostDeleteView.as_view(), name='blog_post_delete'),
]
