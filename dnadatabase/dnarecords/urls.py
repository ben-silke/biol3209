from django.urls import include, path
from dnarecords import views


urlpatterns = [
    path("", views.index, name="index"),
    path("sequences/", views.SequenceListView.as_view(), name="sequence_list"),
    path("sequence/<str:uuid>/", views.SequenceView.as_view(), name="sequence"),
    path("api/", include("dnarecords.api.urls")),
    path("stats/", views.SequenceStatisticView.as_view(), name="summary_stats"),
    path("databases/", views.DatabaseListView.as_view(), name="database_list"),
    path("taxonomys/", views.TaxonomyListView.as_view(), name="taxonomy_list"),
    path('environments/', views.EnvironmentListView.as_view(), name='environment_list')
]
