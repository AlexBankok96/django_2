from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog_post_list.html'
    context_object_name = 'blog_posts'


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post_detail.html'
    context_object_name = 'blog_post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog_post_form.html'
    fields = ['title', 'content', 'preview_image']
    success_url = reverse_lazy('blog:blog_post_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog_post_form.html'
    fields = ['title', 'content', 'preview_image']
    success_url = reverse_lazy('blog:blog_post_list')


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog_post_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_post_list')
