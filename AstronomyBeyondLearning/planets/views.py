from django.shortcuts import render , redirect
from .forms import PlanetForm



# Create your views here.

def add_planet(request):

    if request.method == "POST":
        form = PlanetForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('planets_list')  # بعدين تتفعل هذي الصفحة

    else:
        form = PlanetForm()

    return render(request, 'planets/add_planet.html', {"form": form})
