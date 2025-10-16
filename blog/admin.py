from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'created_at', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')

