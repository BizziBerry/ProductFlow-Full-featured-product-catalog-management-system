from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum, Avg, Min, Max
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category
from .forms import ProductForm, CategoryForm, ProductFilterForm, CategoryFilterForm, AnalyticsFilterForm

from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Product, Category

def home_view(request):
    """Главная страница с общей статистикой"""
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_value = Product.objects.aggregate(total=Sum('price'))['total'] or 0
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_value': total_value,
    }
    return render(request, 'catalog/home.html', context)

# Product CRUD Views
class ProductListView(ListView):
    """Список товаров с фильтрацией и сортировкой"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.select_related('category').all()
        
        # Применяем фильтры
        form = ProductFilterForm(self.request.GET)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            sort_by = form.cleaned_data.get('sort_by') or '-created_at'

            if category:
                queryset = queryset.filter(category=category)
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            
            queryset = queryset.order_by(sort_by)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """Детальная информация о товаре"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """Создание нового товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно создан!')
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно обновлен!')
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    """Удаление товара с подтверждением"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    context_object_name = 'product'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Товар успешно удален!')
        return super().delete(request, *args, **kwargs)


# Category CRUD Views
class CategoryListView(ListView):
    """Список категорий"""
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(
            product_count=Count('products')
        ).order_by('name')


class CategoryCreateView(CreateView):
    """Создание новой категории"""
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно создана!')
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    """Редактирование категории"""
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно обновлена!')
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    """Удаление категории с подтверждением"""
    model = Category
    template_name = 'catalog/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    context_object_name = 'category'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Категория успешно удалена!')
        return super().delete(request, *args, **kwargs)


# Analytics Views
def analytics_view(request):
    """Страница аналитики с агрегатными данными"""
    # Общая статистика по всем товарам
    total_products = Product.objects.count()
    total_value = Product.objects.aggregate(total=Sum('price'))['total'] or 0
    avg_price = Product.objects.aggregate(avg=Avg('price'))['avg'] or 0
    min_price = Product.objects.aggregate(min=Min('price'))['min'] or 0
    max_price = Product.objects.aggregate(max=Max('price'))['max'] or 0

    # Статистика по категориям
    categories_stats = Category.objects.annotate(
        product_count=Count('products'),
        total_value=Sum('products__price'),
        avg_price=Avg('products__price'),
        min_price=Min('products__price'),
        max_price=Max('products__price')
    ).order_by('name')

    context = {
        'total_products': total_products,
        'total_value': total_value,
        'avg_price': avg_price,
        'min_price': min_price,
        'max_price': max_price,
        'categories_stats': categories_stats,
    }
    return render(request, 'catalog/analytics.html', context)


def category_products_view(request, pk):
    """Товары конкретной категории"""
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/category_products.html', context)

class CategoryListView(ListView):
    """Список категорий с фильтрацией и сортировкой"""
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """Аннотируем категории количеством товаров и применяем сортировку"""
        queryset = Category.objects.annotate(
            product_count=Count('products')
        )
        
        # Применяем фильтры из формы
        form = CategoryFilterForm(self.request.GET)
        if form.is_valid():
            sort_by = form.cleaned_data.get('sort_by') or 'name'
            queryset = queryset.order_by(sort_by)
        
        return queryset

    def get_context_data(self, **kwargs):
        """Добавляем форму фильтрации в контекст"""
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CategoryFilterForm(self.request.GET)
        return context


def analytics_view(request):
    """
    Страница аналитики с агрегатными данными и фильтрацией
    """
    # Общая статистика по всем товарам
    total_products = Product.objects.count()
    total_value = Product.objects.aggregate(total=Sum('price'))['total'] or 0
    avg_price = Product.objects.aggregate(avg=Avg('price'))['avg'] or 0
    min_price = Product.objects.aggregate(min=Min('price'))['min'] or 0
    max_price = Product.objects.aggregate(max=Max('price'))['max'] or 0

    # Статистика по категориям с использованием аннотаций
    categories_stats = Category.objects.annotate(
        product_count=Count('products'),
        total_value=Sum('products__price'),
        avg_price=Avg('products__price'),
        min_price=Min('products__price'),
        max_price=Max('products__price')
    )

    # Применяем сортировку
    form = AnalyticsFilterForm(request.GET)
    if form.is_valid():
        sort_by = form.cleaned_data.get('sort_by') or 'name'
        categories_stats = categories_stats.order_by(sort_by)

    context = {
        'total_products': total_products,
        'total_value': total_value,
        'avg_price': avg_price,
        'min_price': min_price,
        'max_price': max_price,
        'categories_stats': categories_stats,
        'filter_form': form,
    }
    return render(request, 'catalog/analytics.html', context)