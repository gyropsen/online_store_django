from django.shortcuts import render
from catalog.models import User


def home(request):
    return render(request, "catalog/home.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        User(name=name, phone=phone, text=message).save()
    return render(request, 'catalog/contacts.html')
