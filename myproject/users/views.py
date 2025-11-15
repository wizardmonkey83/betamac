from django.shortcuts import render

# Create your views here.
def load_index(request):
    return render(request, "index.html")