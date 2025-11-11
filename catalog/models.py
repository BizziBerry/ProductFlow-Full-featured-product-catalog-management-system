from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name="Категория"
    )
    image = models.ImageField(
        upload_to='products/', 
        blank=True, 
        null=True,
        verbose_name="Изображение товара"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    # def clean(self):
    #     """Валидация цены"""
    #     from django.core.exceptions import ValidationError
    #     if self.price < 0:
    #         raise ValidationError({'price': 'Цена не может быть отрицательной'})
