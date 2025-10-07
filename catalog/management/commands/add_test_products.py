"""
Кастомная Django команда для добавления тестовых продуктов
Удаляет все существующие данные и добавляет новые тестовые данные
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет все существующие данные и добавляет тестовые продукты'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Количество продуктов для создания (по умолчанию 10)'
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='Количество категорий для создания (по умолчанию 5)'
        )

    def handle(self, *args, **options):
        count = options['count']
        categories_count = options['categories']
        
        self.stdout.write(
            self.style.SUCCESS('Начинаем создание тестовых данных...')
        )
        
        try:
            with transaction.atomic():
                # 1. Удаляем все существующие данные
                self.stdout.write('Удаляем существующие данные...')
                
                deleted_products = Product.objects.count()
                deleted_categories = Category.objects.count()
                
                Product.objects.all().delete()
                Category.objects.all().delete()
                
                self.stdout.write(
                    self.style.WARNING(
                        f'Удалено {deleted_products} продуктов и {deleted_categories} категорий'
                    )
                )
                
                # 2. Создаем новые категории
                self.stdout.write('Создаем категории...')
                categories = self.create_categories(categories_count)
                
                # 3. Создаем новые продукты
                self.stdout.write('Создаем продукты...')
                products = self.create_products(count, categories)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Успешно создано {len(categories)} категорий и {len(products)} продуктов!'
                    )
                )
                
                # 4. Выводим статистику
                self.print_statistics(categories, products)
                
        except Exception as e:
            raise CommandError(f'Ошибка при создании тестовых данных: {e}')

    def create_categories(self, count):
        """Создает тестовые категории"""
        categories_data = [
            ('Электроника', 'Техника и электронные устройства'),
            ('Одежда', 'Мужская и женская одежда'),
            ('Книги', 'Художественная и техническая литература'),
            ('Спорт', 'Спортивные товары и аксессуары'),
            ('Дом и сад', 'Товары для дома и сада'),
            ('Красота', 'Косметика и средства по уходу'),
            ('Авто', 'Автомобильные товары'),
            ('Игрушки', 'Детские игрушки и игры'),
        ]
        
        categories = []
        for i in range(min(count, len(categories_data))):
            name, description = categories_data[i]
            category = Category.objects.create(
                name=name,
                description=description
            )
            categories.append(category)
            self.stdout.write(f'  Создана категория: {category.name}')
            
        return categories

    def create_products(self, count, categories):
        """Создает тестовые продукты"""
        products_data = [
            # Электроника
            ('iPhone 15 Pro', 'Новейший смартфон от Apple', 'Электроника', 999.99),
            ('Samsung Galaxy S24', 'Флагманский смартфон Samsung', 'Электроника', 899.99),
            ('MacBook Air M3', 'Легкий ноутбук от Apple', 'Электроника', 1299.99),
            ('iPad Pro', 'Планшет для профессионалов', 'Электроника', 799.99),
            ('AirPods Pro', 'Беспроводные наушники', 'Электроника', 249.99),
            
            # Одежда
            ('Джинсы Levis 501', 'Классические мужские джинсы', 'Одежда', 89.99),
            ('Куртка North Face', 'Теплая зимняя куртка', 'Одежда', 199.99),
            ('Футболка Nike', 'Спортивная футболка', 'Одежда', 29.99),
            ('Кроссовки Adidas', 'Беговые кроссовки', 'Одежда', 129.99),
            
            # Книги
            ('Python для начинающих', 'Руководство по изучению Python', 'Книги', 29.99),
            ('Django 4 в действии', 'Практическое руководство по Django', 'Книги', 39.99),
            ('Искусство программирования', 'Классическая книга по алгоритмам', 'Книги', 79.99),
            
            # Спорт
            ('Гантели 20кг', 'Набор разборных гантелей', 'Спорт', 149.99),
            ('Йога-коврик', 'Нескользящий коврик для йоги', 'Спорт', 24.99),
            ('Велосипед горный', 'Горный велосипед для активного отдыха', 'Спорт', 599.99),
            
            # Дом и сад
            ('Кофемашина Delonghi', 'Автоматическая кофемашина', 'Дом и сад', 599.99),
            ('Пылесос Dyson', 'Беспроводной пылесос', 'Дом и сад', 399.99),
            ('Семена томатов', 'Семена для выращивания томатов', 'Дом и сад', 4.99),
        ]
        
        products = []
        for i in range(min(count, len(products_data))):
            name, description, category_name, price = products_data[i]
            
            # Находим категорию по имени
            category = next((cat for cat in categories if cat.name == category_name), categories[0])
            
            product = Product.objects.create(
                name=name,
                description=description,
                category=category,
                price=price,
                is_available=True
            )
            products.append(product)
            self.stdout.write(f'  Создан продукт: {product.name} - ${product.price}')
            
        return products

    def print_statistics(self, categories, products):
        """Выводит статистику созданных данных"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('СТАТИСТИКА СОЗДАННЫХ ДАННЫХ'))
        self.stdout.write('='*50)
        
        # Статистика по категориям
        self.stdout.write('\nКатегории:')
        for category in categories:
            category_products_count = sum(1 for p in products if p.category == category)
            self.stdout.write(f'  {category.name}: {category_products_count} продуктов')
        
        # Общая статистика
        self.stdout.write(f'\nОбщая статистика:')
        self.stdout.write(f'  Всего категорий: {Category.objects.count()}')
        self.stdout.write(f'  Всего продуктов: {Product.objects.count()}')
        
        # Топ-3 самых дорогих продукта
        expensive_products = Product.objects.order_by('-price')[:3]
        self.stdout.write('\nТоп-3 самых дорогих продукта:')
        for i, product in enumerate(expensive_products, 1):
            self.stdout.write(f'  {i}. {product.name} - ${product.price}')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно!'))
        self.stdout.write('='*50)
