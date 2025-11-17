from django.urls import path
from .views import pass_range_parameters, show_game_results

urlpatterns = [
    path("game/", pass_range_parameters, name="pass_range_parameters"),
    path("results/", show_game_results, name="show_game_results"),
]