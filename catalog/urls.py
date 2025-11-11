from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home_view, name='home'),

    # Product URLs
    path('', views.ProductListView.as_view(), name='product_list'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/<int:pk>/products/', views.category_products_view, name='category_products'),
    
    # Analytics URLs
    path('analytics/', views.analytics_view, name='analytics'),
]