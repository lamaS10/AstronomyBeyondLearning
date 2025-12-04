from django.urls import path
from . import views 

app_name = "games"

urlpatterns = [
    path("", views.all_games, name="all_games"),
    path("true-false/", views.true_false_game, name="true_false"),
]