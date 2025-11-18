from django.urls import path
from .views import pass_range_parameters, show_game_results, load_solo, load_multi, load_join, load_host

urlpatterns = [
    path("game/", pass_range_parameters, name="pass_range_parameters"),
    path("results/", show_game_results, name="show_game_results"),

    path("game/solo/", load_solo, name="load_solo"),
    path("game/multi/", load_multi, name="load_multi"),

    path("game/join/", load_join, name="load_join"),
    path("game/host/", load_host, name="load_host"),
]