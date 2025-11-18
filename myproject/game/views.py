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

            addition_enabled = form.cleaned_data["addition_enabled"]
            subtraction_enabled = form.cleaned_data["subtraction_enabled"]
            multiplication_enabled = form.cleaned_data["multiplication_enabled"]
            division_enabled = form.cleaned_data["division_enabled"]

            distractions_enabled = form.cleaned_data["distractions_enabled"]
            print(f"DISTRACTIONS ENABLED: {distractions_enabled}" )

            duration_selector = form.cleaned_data["duration_selector"]

            allowed_operations = []
            if addition_enabled:
                allowed_operations.append('+')
            if subtraction_enabled:
                allowed_operations.append('-')
            if multiplication_enabled:
                allowed_operations.append('*')
            if division_enabled:
                allowed_operations.append('/')

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
                "distractions": distractions_enabled,

                "allowed_operations": allowed_operations,
            }

            return render(request, "game/game.html", context)
    else:
        form = PassRangeParameters()
    return render(request, "index.html", {"form": form})

def show_game_results(request):
    return render(request, "game/solo_results_fragment.html")