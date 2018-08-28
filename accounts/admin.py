from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ArticleAdmin(admin.ModelAdmin):
    pass
