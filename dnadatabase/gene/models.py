from django.db import models
from dnarecords.utils import get_interpro_info
from dnarecords.models import DatabaseReference
from dnarecords.model_utils import concept


# Create your models here.

class Gene(concept):
    name = models.CharField(default="", max_length=256)
    interpro_id = models.CharField(default="", max_length=256)

    odb_cluster_id = models.CharField(null=True, max_length=256)

    other_data = models.JSONField(null=True)

    @property
    def database_set(self):
        return GeneDatabaseReference.objects.filter(gene=self)

    @property
    def cds(self):
        return CDS.objects.filter(gene=self).first()


class GeneDatabaseReference(DatabaseReference):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)



class CDS(concept):
    name = models.CharField(default="", max_length=256)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE, null=True)
    other_data = models.JSONField(null=True)

    @property
    def database_set(self):
        return CdsDatabaseReference.objects.filter(cds=self)


class CdsDatabaseReference(DatabaseReference):
    cds = models.ForeignKey(CDS, on_delete=models.CASCADE)
