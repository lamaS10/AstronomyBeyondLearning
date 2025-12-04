from django.shortcuts import render , redirect
from django.contrib import messages
from .models import Planet,BookmarkPlanet
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
    
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = BookmarkPlanet.objects.filter(
            planet=planet,
            user=request.user
        ).exists()

   
    pages = ["overview", "details"]

    paginator = Paginator(pages, 1)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "planets/planet_detail.html",
        {"planet": planet, "page_obj": page_obj, "is_bookmarked": is_bookmarked}
    )


def planet_delete_view(request, planet_id):

    if not request.user.is_staff:
        messages.warning(request, "Only staff can delete planets", "alert-warning")
        return redirect("main:home_view")

    try:
        planet = Planet.objects.get(id=planet_id)
        planet.delete()
        messages.success(request, "Planet deleted successfully", "alert-success")
    except:
        messages.error(request, "Couldn't delete planet", "alert-danger")

    return redirect("planets:planets_list")


def planet_update_view(request, planet_id):

    if not request.user.is_staff:
        messages.warning(request, "Only staff can update planets", "alert-warning")
        return redirect("main:home")

    planet = Planet.objects.get(id=planet_id)

    if request.method == "POST":
        form = PlanetForm(request.POST, request.FILES, instance=planet)

        if form.is_valid():

            planet.name = request.POST.get("name")
            planet.description = request.POST.get("description")
            planet.category = request.POST.get("category")

            if "image" in request.FILES:
                planet.image = request.FILES["image"]

            planet.save()

            messages.success(request, "Planet updated successfully", "alert-success")
            return redirect("planets:planet_detail", planet_id=planet_id)

    else:
        form = PlanetForm(instance=planet)

    return render(request, "planets/planet_update.html", {
        "planet": planet,
        "form": form,
    })

def toggle_bookmark_view(request, planet_id):

    if not request.user.is_authenticated:
        messages.error(request, "Please log in to bookmark planets.")
        return redirect("accounts:sign_in")

    planet = Planet.objects.get(id=planet_id)

   
    existing = BookmarkPlanet.objects.filter(
        planet=planet,
        user=request.user
    )

    if existing.exists():
        existing.delete()
        messages.warning(request, "Bookmark removed.")
    else:
        BookmarkPlanet.objects.create(
            planet=planet,
            user=request.user
        )
        messages.success(request, "Planet bookmarked.")

    return redirect("planets:planet_detail", planet_id=planet_id)


