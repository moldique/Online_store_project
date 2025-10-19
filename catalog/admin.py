from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_published', 'owner', 'created_at')
    list_filter = ('category', 'is_available', 'is_published', 'created_at')
    search_fields = ('name', 'description', 'owner__username')
    ordering = ('-created_at',)
