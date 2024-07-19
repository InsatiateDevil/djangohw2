from django.urls import path, include
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactsListView, ProductDetailView, \
    ProductCreateView, BlogListView, BlogDetailView, BlogCreateView, \
    BlogUpdateView, BlogDeleteView, ProductUpdateView, ProductDeleteView, \
    CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactsListView.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', cache_page(60)(ProductDetailView.as_view()),
         name='product_detail'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(),
         name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(),
         name='product_delete'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
