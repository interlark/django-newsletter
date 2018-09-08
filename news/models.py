from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from unidecode import unidecode
from accounts.models import Profile
from . import utils
import re


class Article(models.Model):
    poster = models.ImageField(blank=True,
                               upload_to=utils.get_poster_path,
                               verbose_name='Изображение', max_length=512)
    title = models.CharField(max_length=80,
                             blank=False,
                             verbose_name='Заголовок')
    slug = models.SlugField(unique=True,
                            blank=True,
                            editable=False)
    content = models.TextField(verbose_name='Текст',
                               blank=False)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile,
                               null=False,
                               on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    message = models.TextField(verbose_name='Сообщение',
                               blank=False)
    article = models.ForeignKey(Article,
                                null=False,
                                on_delete=models.CASCADE)
    author = models.ForeignKey(Profile,
                               null=False,
                               on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


def reserved_slugs():
    from news.urls import urlpatterns as news_urlpatterns
    from newsletter.urls import urlpatterns as app_urlpatterns

    r = re.compile('^[\w\d_-]+/$')
    news_url_paths = [str(url_pattern.pattern) for url_pattern in news_urlpatterns]
    app_url_paths = [str(url_pattern.pattern) for url_pattern in app_urlpatterns]
    url_paths = news_url_paths + app_url_paths
    paths = list(filter(r.match, url_paths))
    slugs = [path[:-1] for path in paths]
    return slugs


def create_slug(instance, new_slug=None, counter=2):
    slug = slugify(unidecode(instance.title))
    if new_slug is not None:
        slug = new_slug
    articles = Article.objects.filter(slug=slug)
    if articles.exists() or slug in reserved_slugs():
        new_slug = '%s-%s' % (slug, counter)
        return create_slug(instance, new_slug, counter + 1)
    return slug


@receiver(pre_save, sender=Article)
def article_on_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:  # Запрещаем менять пулю опубликованной статьи
        instance.slug = create_slug(instance)
