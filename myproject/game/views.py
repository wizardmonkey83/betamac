from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .forms import PassRangeParameters, PassHostParameters, Joinlobby
import redis
import random
import json


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

            # bandaid
            duration = request.POST.get('duration_selector')
            print(f"DURATION: {duration}")

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

                "duration": duration,
                "distractions": distractions_enabled,

                "allowed_operations": allowed_operations,
            }

            return render(request, "game/game.html", context)
    else:
        form = PassRangeParameters()
    return render(request, "index.html", {"form": form})


def host_game(request):
    if request.method == "POST":
        form = PassHostParameters(request.POST)
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

            duration = request.POST.get('duration_selector')

            lobby_code = form.cleaned_data["lobby_code"]

            allowed_operations = []
            if addition_enabled:
                allowed_operations.append('+')
            if subtraction_enabled:
                allowed_operations.append('-')
            if multiplication_enabled:
                allowed_operations.append('*')
            if division_enabled:
                allowed_operations.append('/')

            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
            exists = r.exists(f"game:{lobby_code}:config")

            if not exists:
                # send all parameters to the unique lobby
                r.hset(f"game:{lobby_code}:config", mapping={
                    "addition_left_min": addition_left_min,
                    "addition_left_max": addition_left_max,
                    "addition_right_min": addition_right_min,
                    "addition_right_max": addition_right_max,

                    "multiplication_left_min": multiplication_left_min,
                    "multiplication_left_max": multiplication_left_max,
                    "multiplication_right_min": multiplication_right_min,
                    "multiplication_right_max": multiplication_right_max,

                    "duration": duration,
                    "distractions": distractions_enabled,

                    "allowed_operations": json.dumps(allowed_operations),
                })
                # seconds
                r.expire(f"game:{lobby_code}:config", 630)
                return HttpResponseRedirect(reverse("start_game", args=[lobby_code]))
            else:
                lobby_code = ""
                characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                i = 0
                while i < 6:
                    random_index = random.randint(0, len(characters) - 1)
                    lobby_code += characters[random_index]
                    i += 1
                second_exists = r.exists(f"game:{lobby_code}:config")
                if not second_exists:
                    r.hset(f"game:{lobby_code}:config", mapping={
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

                    "allowed_operations": json.dumps(allowed_operations),
                    })
                    # seconds
                    r.expire(f"game:{lobby_code}:config", 630)
                    return HttpResponseRedirect(reverse("start_game", args=[lobby_code]))
                else:
                    # ur cooked pal
                    return None

def start_game(request, lobby_code):
    return render(request, "game/multi/multi_game.html", {"lobby_code": lobby_code})

def join_game(request):
    if request.method == "POST":
        form = Joinlobby(request.POST)
        if form.is_valid():
            lobby_code = form.cleaned_data["lobby_code"]
            # port subject to change
            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
            exists = r.exists(f"game:{lobby_code}:config")

            if exists:
                return HttpResponseRedirect(reverse("start_game", args=[lobby_code]))
            else:
                form.add_error(None, "Invalid login code.")
        
    else:
        form = Joinlobby()
    return render(request, "game/multi/join_fragment.html", {"form": form})



# routing -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def show_game_results(request):
    return render(request, "game/solo/solo_results_fragment.html")

def load_solo(request):
    form = PassRangeParameters()
    return render(request, "game/solo/solo_fragment.html", {"form": form})

def load_multi(request):
    form = Joinlobby()
    return render(request, "game/multi/multi_fragment.html", {"form": form})

def load_join(request):
    form = Joinlobby()
    return render(request, "game/multi/join_fragment.html", {"form": form})

def load_host(request):
    parameter_form = PassRangeParameters()
    return render(request, "game/multi/host_fragment.html", {"parameter_form": parameter_form})

def load_rules(request):
    return render(request, "rules.html")