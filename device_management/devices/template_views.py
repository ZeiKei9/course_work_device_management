from django.shortcuts import render


def home_view(request):
    return render(request, "home.html")


def device_catalog_view(request):
    return render(request, "device_catalog.html")
