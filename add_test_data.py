import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalog_project.settings')
django.setup()

from catalog.models import Category, Product

def create_test_data():
    # Создаем категории
    categories = [
        "Электроника",
        "Одежда", 
        "Книги",
        "Спорт",
        "Дом и сад"
    ]
    
    created_categories = []
    for cat_name in categories:
        category, created = Category.objects.get_or_create(name=cat_name)
        created_categories.append(category)
        print(f"Создана категория: {cat_name}")
    
    # Создаем товары
    products_data = [
        {"name": "Смартфон Samsung", "price": 29999.99, "category": "Электроника", "description": "Современный смартфон с отличной камерой"},
        {"name": "Ноутбук HP", "price": 54999.50, "category": "Электроника", "description": "Мощный ноутбук для работы и игр"},
        {"name": "Футболка хлопковая", "price": 1499.99, "category": "Одежда", "description": "Удобная футболка из натурального хлопка"},
        {"name": "Джинсы", "price": 3999.00, "category": "Одежда", "description": "Стильные джинсы классического кроя"},
        {"name": "Python для начинающих", "price": 1299.00, "category": "Книги", "description": "Лучшая книга для изучения Python"},
        {"name": "Война и мир", "price": 899.00, "category": "Книги", "description": "Классика русской литературы"},
        {"name": "Футбольный мяч", "price": 2499.00, "category": "Спорт", "description": "Профессиональный футбольный мяч"},
        {"name": "Гантели 5кг", "price": 1999.00, "category": "Спорт", "description": "Набор гантелей для домашних тренировок"},
        {"name": "Цветочный горшок", "price": 499.00, "category": "Дом и сад", "description": "Керамический горшок для цветов"},
        {"name": "Набор инструментов", "price": 3599.00, "category": "Дом и сад", "description": "Необходимые инструменты для дома"},
    ]
    
    for product_data in products_data:
        category = Category.objects.get(name=product_data["category"])
        product, created = Product.objects.get_or_create(
            name=product_data["name"],
            defaults={
                'price': product_data["price"],
                'category': category,
                'description': product_data["description"]
            }
        )
        if created:
            print(f"Создан товар: {product_data['name']} - {product_data['price']} руб.")
        else:
            print(f"Товар уже существует: {product_data['name']}")
    
    print("\nТестовые данные успешно добавлены!")

if __name__ == "__main__":
    create_test_data()