from django.shortcuts import render
from django.views.generic import ListView
from .models import Tip
# Create your views here.

class TipsList(ListView):
    queryset = Tip.objects.all()
    context_object_name = "tips"
    template_name = "tips.html"
