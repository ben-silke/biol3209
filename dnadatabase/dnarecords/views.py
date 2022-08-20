from multiprocessing import get_context
from pipes import Template

from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView, TemplateView

from . import models


def index(request):
    return HttpResponse("Hello, world. You're at the dnarecords index.")


class SequenceListView(ListView):
    model = models.Sequence


class SequenceView(TemplateView):
    template_name: str = "sequence.html"
