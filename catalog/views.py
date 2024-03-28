from django.shortcuts import render
from catalog.models import User
from catalog.models import Product
from catalog.models import Category


def index(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Главная'
    }
    return render(request, 'catalog/index.html', context)


def contacts(request):
    context = {
        'title': 'Контакты'
    }

    return render(request, 'catalog/contacts.html', context)


def write_message(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        User(name=name, phone=phone, text=message).save()
    context = {'title': 'Напишите нам'}

    return render(request, 'catalog/write_mess.html', context)


def catalog(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Каталог'
    }
    return render(request, 'catalog/catalog.html', context)


def products(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': str(category_item.name),
        'description': str(category_item.description),
    }
    return render(request, 'catalog/product.html', context)
