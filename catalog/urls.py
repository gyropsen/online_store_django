from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import index, contacts, products, write_message, catalog

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name="index"),
    path('contacts/', contacts, name="contacts"),
    path('write/', write_message, name='write_message'),
    path('catalog/', catalog, name='catalog'),
    path('products/<int:pk>/', products, name="products"),
]
# <int:pk>/
