from django.shortcuts import render

# Create your views here.
# kenji2
# kenji.konno@soliton-advisors.com
# Def6392a / Melbourn65

# Create your views here.
from django.contrib.auth.decorators import login_required
@login_required()
def home(request):
    return render(request, 'setting/home.html')