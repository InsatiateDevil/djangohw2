from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactsListView, ProductDetailView, \
    ProductCreateView, BlogListView, BlogDetailView, BlogCreateView, \
    BlogUpdateView, BlogDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactsListView.as_view(), name='contacts'),
    path('product_details/<int:pk>/', ProductDetailView.as_view(),
         name='product_details'),
    path('add_product/', ProductCreateView.as_view(), name='product_create'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
