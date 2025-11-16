from django.shortcuts import render
from game.forms import PassRangeParameters

# Create your views here.
def load_index(request):
    form = PassRangeParameters()
    return render(request, "index.html", {"form": form})