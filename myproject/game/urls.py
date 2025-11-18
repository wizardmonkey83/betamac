from django.urls import path
from .views import pass_range_parameters, show_game_results, load_solo, load_multi

urlpatterns = [
    path("game/", pass_range_parameters, name="pass_range_parameters"),
    path("results/", show_game_results, name="show_game_results"),

    path("game/solo/", load_solo, name="load_solo"),
    path("game/multi/", load_multi, name="load_multi"),
]