from django.shortcuts import render , redirect
from django.contrib import messages
from .models import Planet
from .forms import PlanetForm
from django.core.paginator import Paginator


# Create your views here.


def planets_add_view(request):

    if not request.user:
        messages.warning(request, "Only staff can add planets", "alert-warning")
        return redirect("main:home")

    if request.method == "POST":
        form = PlanetForm(request.POST, request.FILES)

        if form.is_valid():
            planet = form.save()
            messages.success(request, "Planet added successfully", "alert-success")
            return redirect("main:home")

    else:
        form = PlanetForm()

    return render(request, "planets/add_planet.html", {
        "form": form,
    })




def planets_list_view(request):
    planets = Planet.objects.all()
    return render(request, "planets/all_planets.html", {"planets": planets})

def planet_detail_view(request, planet_id):

    try:
        planet = Planet.objects.get(id=planet_id)
    except Planet.DoesNotExist:
        messages.error(request, "Planet does not exist", "alert-danger")
        return redirect("planets:planets_list")

    # paginator بيسوي صفحتين: 1 = overview , 2 = details
    pages = ["overview", "details"]

    paginator = Paginator(pages, 1)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "planets/planet_detail.html",
        {"planet": planet, "page_obj": page_obj}
    )