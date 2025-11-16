from django.urls import path
from .views import pass_range_parameters

urlpatterns = [
    path("game/", pass_range_parameters, name="pass_range_parameters")
]