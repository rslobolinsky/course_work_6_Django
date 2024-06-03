from django.db import models

NULLABLE = {"null": True, "blank": True}


class Blog(models.Model):
    """Модель блога"""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(upload_to="images", verbose_name="Изображение", **NULLABLE)
    views = models.IntegerField(verbose_name="Просмотры", default=0)
    data_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(verbose_name="Признак публикации", default=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
