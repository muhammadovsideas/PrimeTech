from django.urls import path
from main.views import *

urlpatterns = [
    # HTML pages
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product-detail'),

    # API Endpoints
    path('api/category/', CategoryListAPIView.as_view(), name='api-category-list'),
    path('api/products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('api/category/<int:pk>/', CategoryDetailAPIView.as_view(), name='api-category-detail'),
    path('api/product/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
]
