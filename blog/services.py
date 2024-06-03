from django.conf import settings
from django.core.cache import cache

from blog.models import Blog


def get_blog_cache():
    """Функция кеширования блога"""
    if settings.CACHE_ENABLED:
        key = "blog_list"
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Blog.objects.filter(is_published=True)
            cache.set(key, blog_list)
        else:
            blog_list = Blog.objects.filter(is_published=True)
            print(blog_list)
        return blog_list
