from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_blog_cache


class BlogCreateView(PermissionRequiredMixin, CreateView):
    """Класс создания статьи блога"""

    form_class = BlogForm
    template_name = "blog/blog_form.html"
    permission_required = "blog.add_blog"
    success_url = reverse_lazy("blog:list")


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    """Класс редактирования статьи блога"""

    form_class = BlogForm
    template_name = "blog/blog_form.html"
    permission_required = "blog.change_blog"

    def get_success_url(self):
        return reverse("blog:blogs", args=[self.kwargs.get("pk")])


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    """Класс удаления статьи блога"""

    permission_required = "blog.delete_blog"
    model = Blog
    success_url = reverse_lazy("blog:list")


class BlogListView(ListView):
    """Класс просмотра списка статей блога"""

    model = Blog

    def get_queryset(self, *args, **kwargs):
        return get_blog_cache()


class BlogDetailView(DetailView):
    """Класс просмотра статьи блога"""

    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object
