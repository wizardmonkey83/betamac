from django.urls import path
from .views import pass_range_parameters, show_game_results, load_solo, load_multi, load_join, load_host, host_game, start_game, join_game, load_rules

urlpatterns = [
    path("game/", pass_range_parameters, name="pass_range_parameters"),
    path("results/", show_game_results, name="show_game_results"),

    path("game/solo/", load_solo, name="load_solo"),
    path("game/multi/", load_multi, name="load_multi"),

    path("game/load/join/", load_join, name="load_join"),
    path("game/load/host/", load_host, name="load_host"),

    path("game/host/", host_game, name="host_game"),
    path("game/join/", join_game, name="join_game"),
    path("game/lobby/<str:lobby_code>/", start_game, name="start_game"),

    path("rules/", load_rules, name="load_rules"),
]