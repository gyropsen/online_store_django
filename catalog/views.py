from catalog.forms import ProductForm, ProductVersionForm
from catalog.models import User, Product, Category, ProductVersion
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexTemplateView(ListView):
    model = Product
    extra_context = {'title': 'Главная'}
    template_name = 'catalog/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=None, **kwargs)
        # Получаем все продукты
        products = Product.objects.all()

        # Перебор продуктов
        for product in products:

            # Получение всех версии продуктов
            versions = ProductVersion.objects.filter(product=product)
            if versions:

                # Получение активной версии из версий
                active_version = versions.filter(is_active=True)
                if active_version:

                    # Присваивание версии
                    product.version_num = active_version[0].version
                    product.version_name = active_version[0].name_version
                else:
                    product.version = None
            else:
                product.version = None
        context_data['object_list'] = products
        return context_data


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

class ProductDetailView(DetailView):
    model = Product
    extra_context = {'title': 'Детальный просмотр продукта'}


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:register')
    redirect_field_name = ""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        product = form.save()
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:register')
    redirect_field_name = ""
    model = Product
    form_class = ProductForm
    extra_context = {'title': 'Редактирование продукта'}

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductVersionFormset = inlineformset_factory(Product, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            formset = ProductVersionFormset(self.request.POST, instance=self.object)
        else:
            formset = ProductVersionFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        object_ = form.save()

        if formset.is_valid():
            formset.instance = object_
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('users:register')
    redirect_field_name = ""
    model = Product
    extra_context = {'title': 'Удаление продукта'}

    def get_success_url(self):
        return reverse('catalog:products', args=[Product.objects.get(pk=self.kwargs.get('pk')).category.pk])
