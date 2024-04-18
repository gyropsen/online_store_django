from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    image = models.ImageField(upload_to='catalog/', verbose_name='Превью')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.FloatField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    # manufactured_at = models.DateField(verbose_name='Дата производства продукта', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return (f"{self.name} {self.description} {self.image} {self.category} "
                f"{self.price} {self.created_at} {self.updated_at}")

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class User(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    phone = models.TextField(**NULLABLE)
    text = models.TextField(**NULLABLE)

    def __str__(self):
        return f'{self.name} {self.phone} {self.text}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ProductVersion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version = models.PositiveIntegerField(verbose_name='Версия продукта')
    name_version = models.CharField(max_length=128, verbose_name='Название версии')
    is_active = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return f"{self.product} ({self.version})"

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
