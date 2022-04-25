from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import admin


class Blog(models.Model):
    title = models.CharField(max_length = 80, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое описание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.ImageField(upload_to='images/', default = 'images.jpg', verbose_name = "Путь к картинке")
    
    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return f'/{self.id}'

    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title
        class Meta:
            db_table = "Блог"
            ordering = ["-posted"]
            verbose_name = "статья блога"
            verbose_name_plural = "статьи блога"

admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(max_length=500)
    posted = models.DateTimeField(default=datetime.now(), verbose_name="Time published")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/{self.id}'

    def __str__(self):
        return self.text