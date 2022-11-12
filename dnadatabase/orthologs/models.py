from django.db import models

# Create your models here.
from gene.models import Gene
from dnarecords.models import DatabaseReference


class OrthologReference(DatabaseReference):
    # database = models.ForeignKey(
    #     Database, on_delete=models.CASCADE, null=True)
    # db_xref = models.CharField(null=True, max_length=50)
    # text = models.CharField(
    #     null=True, max_length=50, help_text="Original text of the reference"
    # )

    def get_orthologs(self):
        return QuestGene.objects.filter(reference=self)


    @property
    def orthologs(self):
        return QuestGene.objects.filter(reference=self).count()


class QuestGene(Gene):
    uniprot_accession = models.CharField(max_length=256)
    reference = models.ManyToManyField(OrthologReference)
    # reference = models.ForeignKey(OrthologReference, on_delete=models.CASCADE)
    reference_text = models.CharField(max_length=256)
    file_name = models.CharField(max_length=256)

    oma_reference_id = models.CharField(max_length=256, null=True)



