from django import forms

from blog.models import Blog


class BlogForm(forms.ModelForm):
    """Класс формы для блога"""

    class Meta:
        model = Blog
        fields = ("title", "content", "image", "is_published")
