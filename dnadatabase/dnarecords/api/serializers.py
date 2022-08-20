from rest_framework import serializers

from .. import models


class SequenceSerializer(serializers.Serializer):
    class Meta:
        model = models.Sequence
        fields = ["__all__"]
