from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id, timeout=300):
    """
    Сервисная функция для получения списка продуктов по категории с кэшированием.
    
    Args:
        category_id (int): ID категории
        timeout (int): Время жизни кэша в секундах (по умолчанию 5 минут)
    
    Returns:
        QuerySet: Список продуктов в указанной категории
    """
    # Создаем ключ кэша с учетом категории
    cache_key = f'products_category_{category_id}'
    
    # Пытаемся получить данные из кэша
    products = cache.get(cache_key)
    
    if products is None:
        # Если данных нет в кэше, получаем их из базы данных
        products = Product.objects.filter(
            category_id=category_id, 
            is_published=True
        ).select_related('category')
        
        # Сохраняем в кэш на указанное время
        cache.set(cache_key, products, timeout)
    
    return products


def invalidate_category_cache(category_id):
    """
    Функция для очистки кэша продуктов категории.
    Используется при изменении продуктов в категории.
    
    Args:
        category_id (int): ID категории
    """
    cache_key = f'products_category_{category_id}'
    cache.delete(cache_key)
