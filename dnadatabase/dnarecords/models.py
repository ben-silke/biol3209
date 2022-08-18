from django.db import models

from .model_utils import concept

class Database(concept):
    name = models.CharField(null=True, max_length=255)
    description = models.TextField(
        null=True,
    )
    url = models.URLField(
        null=True,
    )


class Sequence(concept):
    sequence = models.TextField(
        null=True,
    )
    accession = models.CharField(null=True, max_length=50)
    organism = models.CharField(null=True, max_length=50)
    description = models.CharField(null=True, max_length=50)
    gene = models.CharField(null=True, max_length=50)

    relations = models.JSONField(
        null=True,
    )

    @property
    def feature_set(self):
        return Feature.objects.filter(sequence=self)


class Feature(concept):
    type = models.CharField(null=True, max_length=50)
    location = models.CharField(max_length=50, null=True)
    # if you delete a sequence the features will all be deleted
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)

    @property
    def database_reference_set(self):
        return DatabaseReference.objects.filter(feature=self)


class DatabaseReference(concept):
    database = models.ManyToManyField(Database)
    db_xref = models.CharField(null=True, max_length=50)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)


class GenbankRecord(Sequence):
    pass


class EnsemblRecord(Sequence):
    pass
