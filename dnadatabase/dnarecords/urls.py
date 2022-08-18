from django.urls import include, path

from dnarecords import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sequences/", views.SequenceListView.as_view(), name="sequence_list"),
    path("sequence/", views.SequenceView.as_view(), name="sequence"),
    path("api/", include("dnarecords.api.urls")),
]
