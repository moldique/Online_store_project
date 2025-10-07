# Фикстуры для каталога

Этот каталог содержит фикстуры (fixtures) для моделей `Category` и `Product`.

## Файлы фикстур

- `categories.json` - содержит 5 категорий товаров
- `products.json` - содержит 10 продуктов в различных категориях
- `catalog_data.json` - объединенный файл с категориями и продуктами

## Использование фикстур

### Загрузка всех данных (рекомендуется)
```bash
poetry run python manage.py loaddata catalog/fixtures/catalog_data.json
```

### Загрузка только категорий
```bash
poetry run python manage.py loaddata catalog/fixtures/categories.json
```

### Загрузка только продуктов
```bash
poetry run python manage.py loaddata catalog/fixtures/products.json
```

### Очистка базы данных перед загрузкой
```bash
poetry run python manage.py flush --noinput
poetry run python manage.py loaddata catalog/fixtures/catalog_data.json
```

## Содержимое фикстур

### Категории (5 шт.)
1. Электроника
2. Одежда
3. Книги
4. Спорт
5. Дом и сад

### Продукты (10 шт.)
- iPhone 15 Pro (Электроника)
- Samsung Galaxy S24 Ultra (Электроника)
- MacBook Air M3 (Электроника)
- Джинсы Levis 501 (Одежда)
- Куртка North Face (Одежда)
- Python для начинающих (Книги)
- Django 4 в действии (Книги)
- Беговые кроссовки Nike (Спорт)
- Йога-коврик (Спорт)
- Кофемашина Delonghi (Дом и сад)

## Проверка загрузки

После загрузки фикстур можно проверить данные в Django shell:

```python
from catalog.models import Category, Product

# Проверка количества
print(f"Категорий: {Category.objects.count()}")
print(f"Продуктов: {Product.objects.count()}")

# Просмотр всех категорий
for cat in Category.objects.all():
    print(f"- {cat.name}")

# Просмотр всех продуктов
for prod in Product.objects.all():
    print(f"- {prod.name} ({prod.category.name}) - ${prod.price}")
```
