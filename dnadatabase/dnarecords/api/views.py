from rest_framework import viewsets

from dnarecords.models import Sequence
from dnarecords.api.serializers import SequenceSerializer


class SequenceViewSet(viewsets.ModelViewSet):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
