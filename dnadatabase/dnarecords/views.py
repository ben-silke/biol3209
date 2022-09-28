from ast import Dict
from multiprocessing import get_context
from pipes import Template
from typing import Any

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView, TemplateView

from . import models


def index(request):
    return HttpResponse("Hello, world. You're at the dnarecords index.")


class SequenceListView(ListView):
    template_name = "sequence_list.html"
    model = models.Sequence


class SequenceView(DetailView):
    template_name: str = "sequence.html"
    model = models.Sequence


class SequenceStatisticView(TemplateView):
    template_name = "dnarecords/summary_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "database_count": models.Database.objects.all().count(),
                "sequence_count": models.Sequence.objects.all().count(),
            }
        )

        return context


class DatabaseListView(ListView):
    template_name = "dnarecords/database_list.html"
    model = models.Database


class TaxonomyListView(ListView):
    template_name = "dnarecords/taxonomy_list.html"
    model = models.Taxonomy


class EnvironmentListView(ListView):
    template_name = "dnarecords/environment_list.html"
    model = models.Environment
