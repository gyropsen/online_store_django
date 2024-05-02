from django.contrib import admin
from catalog.models import Product, Category, User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone', 'text')
