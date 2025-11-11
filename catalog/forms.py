from django import forms
from django.core.validators import MinValueValidator
from .models import Product, Category

class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования товаров"""
    
    # Явно объявляем поле price с валидацией
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,  # Запрещаем отрицательные значения
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'step': '0.01',
            'required': 'required'
        }),
        label='Цена (руб.)',
        error_messages={
            'required': 'Цена обязательна для заполнения',
            'min_value': 'Цена не может быть отрицательной',
            'invalid': 'Введите корректное число'
        }
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'category': 'Категория',
            'image': 'Изображение товара',
        }

    def clean_price(self):
        """Валидация цены на уровне формы"""
        price = self.cleaned_data.get('price')
        
        # Дополнительная проверка (хотя min_value=0 уже делает это)
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
            
        return price

    def clean_name(self):
        """Валидация названия товара"""
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise forms.ValidationError('Название товара обязательно для заполнения')
        return name.strip()


class CategoryForm(forms.ModelForm):
    """Форма для создания и редактирования категорий"""
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }
        labels = {
            'name': 'Название категории',
        }

    def clean_name(self):
        """Валидация названия категории"""
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise forms.ValidationError('Название категории обязательно для заполнения')
        return name.strip()


class ProductFilterForm(forms.Form):
    """Форма для фильтрации товаров с динамической отправкой"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Мин. цена',
            'step': '0.01',
            'onchange': 'this.form.submit()'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Макс. цена',
            'step': '0.01',
            'onchange': 'this.form.submit()'
        })
    )
    
    SORT_CHOICES = [
        ('name', 'Название (А-Я)'),
        ('-name', 'Название (Я-А)'),
        ('price', 'Цена (по возрастанию)'),
        ('-price', 'Цена (по убыванию)'),
        ('created_at', 'Дата (сначала старые)'),
        ('-created_at', 'Дата (сначала новые)'),
    ]
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )


class CategoryFilterForm(forms.Form):
    """Форма для фильтрации категорий"""
    SORT_CHOICES = [
        ('name', 'Название (А-Я)'),
        ('-name', 'Название (Я-А)'),
        ('product_count', 'Количество товаров (по возрастанию)'),
        ('-product_count', 'Количество товаров (по убыванию)'),
        ('created_at', 'Дата создания (сначала старые)'),
        ('-created_at', 'Дата создания (сначала новые)'),
    ]
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='name',
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit()'})
    )


class AnalyticsFilterForm(forms.Form):
    """Форма для фильтрации аналитики"""
    SORT_CHOICES = [
        ('name', 'Категория (А-Я)'),
        ('-name', 'Категория (Я-А)'),
        ('product_count', 'Количество товаров (по возрастанию)'),
        ('-product_count', 'Количество товаров (по убыванию)'),
        ('total_value', 'Общая стоимость (по возрастанию)'),
        ('-total_value', 'Общая стоимость (по убыванию)'),
    ]
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='name',
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit()'})
    )