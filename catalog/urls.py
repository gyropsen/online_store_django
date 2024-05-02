from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import IndexTemplateView, ContactTemplateView, ProductListView, WriteMessageCreateView, \
    CatalogListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from django.views.decorators.cache import cache_page, never_cache

app_name = CatalogConfig.name

urlpatterns = [
    path('', never_cache(IndexTemplateView.as_view()), name="index"),
    path('contacts/', never_cache(ContactTemplateView.as_view()), name="contacts"),
    path('write/', cache_page(60)(WriteMessageCreateView.as_view()), name='write_message'),
    path('catalog/', never_cache(CatalogListView.as_view()), name='catalog'),
    path('products/<int:pk>/', never_cache(ProductListView.as_view()), name="products"),
    path('detail/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name="product_detail"),
    path('create/', cache_page(60)(ProductCreateView.as_view()), name="product_create"),
    path('update/<int:pk>', cache_page(60)(ProductUpdateView.as_view()), name="product_update"),
    path('delete/<int:pk>', never_cache(ProductDeleteView.as_view()), name="product_delete"),
]
