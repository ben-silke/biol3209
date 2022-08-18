from django.urls import include, path
from rest_framework import routers
from dnarecords import views

router = routers.DefaultRouter()
router.register(r'sequence', views.SequenceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api', include(router.urls)),
]
