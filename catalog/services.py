from config.settings import CACHE_ENABLED
from django.core.cache import cache


def model_objects_all(model):
    """
    Функция предоставляет возможность получение от любой модели только всех данных
    :return: Queryset
    """
    if not CACHE_ENABLED:
        return model.objects.all()

    key = f"{model.__name__}_list"
    categories_in_cache = cache.get(key)

    # Проверяем, есть ли в кэше данные по ключу categories_list
    if categories_in_cache:
        # Возвращаем данные в кэше
        return categories_in_cache
    else:
        # Записываем данные в кэш, и возвращаем
        categories = model.objects.all()
        cache.set(key, categories)
        return categories
