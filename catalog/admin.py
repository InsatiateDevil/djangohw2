from django.contrib import admin
from catalog.models import Product, Category, Contact, Version, Blog


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('product_name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('category_name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'inn', 'address')
    search_fields = ('country', 'address',)
    list_filter = ('country',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'version_number', 'version_name', 'is_active')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'is_published')
