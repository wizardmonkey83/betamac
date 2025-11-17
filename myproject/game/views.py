from django.shortcuts import render
from .forms import PassRangeParameters

# Create your views here.
def pass_range_parameters(request):
    if request.method == "POST":
        form = PassRangeParameters(request.POST)
        if form.is_valid():
            addition_left_min = form.cleaned_data["addition_left_min"]
            addition_left_max = form.cleaned_data["addition_left_max"]
            addition_right_min = form.cleaned_data["addition_right_min"]
            addition_right_max = form.cleaned_data["addition_right_max"]

            multiplication_left_min = form.cleaned_data["multiplication_left_min"]
            multiplication_left_max = form.cleaned_data["multiplication_left_max"]
            multiplication_right_min = form.cleaned_data["multiplication_right_min"]
            multiplication_right_max = form.cleaned_data["multiplication_right_max"]

            duration_selector = form.cleaned_data["duration_selector"]

            context = {
                "addition_left_min": addition_left_min,
                "addition_left_max": addition_left_max,
                "addition_right_min": addition_right_min,
                "addition_right_max": addition_right_max,

                "multiplication_left_min": multiplication_left_min,
                "multiplication_left_max": multiplication_left_max,
                "multiplication_right_min": multiplication_right_min,
                "multiplication_right_max": multiplication_right_max,

                "duration": duration_selector,
            }

            return render(request, "game/game.html", context)
    else:
        form = PassRangeParameters()
    return render(request, "index.html", {"form": form})

def show_game_results(request):
    return render(request, "game/solo_results_fragment.html")