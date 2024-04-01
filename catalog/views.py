from django.shortcuts import render
from catalog.models import User, Product, Category
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView


class IndexTemplateView(ListView):
    model = Product
    extra_context = {'title': 'Главная'}
    template_name = 'catalog/index.html'


# def index(request):
#     context = {
#         'object_list': Product.objects.all(),
#         'title': 'Главная'
#     }
#     return render(request, 'catalog/index.html', context)

class ContactTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['link'] = 'https://t.me/liveinthis'
        return context


# def contacts(request):
#     context = {
#         'title': 'Контакты'
#     }
#
#     return render(request, 'catalog/contacts.html', context)


class WriteMessageCreateView(CreateView):
    model = User
    fields = ('name', 'phone', 'text')
    success_url = reverse_lazy('catalog:index')


# def write_message(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#         User(name=name, phone=phone, text=message).save()
#     context = {'title': 'Напишите нам'}
#
#     return render(request, 'catalog/user_form.html', context)


class CatalogListView(ListView):
    model = Category
    extra_context = {'title': 'Каталог'}


# def catalog(request):
#     context = {
#         'object_list': Category.objects.all(),
#         'title': 'Каталог'
#     }
#     return render(request, 'catalog/category_list.html', context)

class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=None, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk
        context_data['title'] = str(category_item.name)
        context_data['description'] = str(category_item.description)

        return context_data


# def products(request, pk):
#     category_item = Category.objects.get(pk=pk)
#     context = {
#         'object_list': Product.objects.filter(category_id=pk),
#         'title': str(category_item.name),
#         'description': str(category_item.description),
#     }
#     return render(request, 'catalog/product_list.html', context)
