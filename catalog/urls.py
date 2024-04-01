from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import IndexTemplateView, ContactTemplateView, ProductListView, WriteMessageCreateView, CatalogListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexTemplateView.as_view(), name="index"),
    path('contacts/', ContactTemplateView.as_view(), name="contacts"),
    path('write/', WriteMessageCreateView.as_view(), name='write_message'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('products/<int:pk>/', ProductListView.as_view(), name="products"),
]
