from django.shortcuts import render


def home(request):
    return render(request, 'main/home.html')

def about_view(request):
    return render(request, "main/about.html")


