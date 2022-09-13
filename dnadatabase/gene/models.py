from django.db import models
from dnarecords.utils import get_interpro_info
from dnarecords.models import DatabaseReference
from dnarecords.model_utils import concept
import requests
BASE_KEGG = 'https://rest.kegg.jp/'
# Create your models here.
GET = 'get/'
CONVERT = 'conv/genes/'


class KeggConnectionMixin:

    def kegg_link(self):
        response = None
        if gene_id := self.database_set.filter(database__name='GeneID').first():
            print(f'{gene_id=} ; {gene_id.db_xref=} ; {gene_id.database.name=}')
            url = BASE_KEGG+CONVERT+'ncbi-geneid:'+gene_id.db_xref
            print(url)
            try:
                response = requests.get(url)
            except:
                response = None
        if response.text == '\n':
            response = None
            if uniprot := self.database_set.filter(database__name='UniProtKB/Swiss-Prot').first():
                print(f'{uniprot=} ; {uniprot.db_xref=} ; {uniprot.database.name=}')

                print(f'{uniprot=}')
                try:
                    response = requests.get(BASE_KEGG+CONVERT+'uniprot:'+uniprot.db_xref)
                except:
                    response = None
        print(f'{response.text=}')
        if response and response.status_code == 200:
            try:
                kegg_id = response.text.split('\n')[0].split('\t')[1]
                self.kegg_id = kegg_id
                self.save()

                response = requests.get(BASE_KEGG+GET+kegg_id)
                if response.status_code == 200:
                    return response.text
            except Exception as e:
                print(f'Exception {e} resulted in failure. {response.text=}')

class Gene(concept, KeggConnectionMixin):
    name = models.CharField(default="", max_length=256)
    interpro_id = models.CharField(default="", max_length=256)

    odb_cluster_id = models.CharField(null=True, max_length=256)

    other_data = models.JSONField(null=True)
    kegg_id = models.CharField(null=True, max_length=64)


    @property
    def database_set(self):
        return GeneDatabaseReference.objects.filter(gene=self)

    @property
    def cds(self):
        return CDS.objects.filter(gene=self).first()

    def get_kegg_id(self):
        if self.kegg_id:
            return self.kegg_id

        else:
            self.kegg_link()
            if not self.kegg_id:
                raise ValueError(f'Database reference does not have an associated link in kegg db.')
            return self.kegg_id


class GeneDatabaseReference(DatabaseReference):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)


class CDS(concept, KeggConnectionMixin):
    name = models.CharField(default="", max_length=256)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE, null=True)

    other_data = models.JSONField(null=True)
    product = models.CharField(null=True, max_length=256)
    protein_id = models.CharField(null=True, max_length=64)
    translation = models.TextField(null=True, max_length=500)
    kegg_id = models.CharField(null=True, max_length=64)


    @property
    def database_set(self):
        return CdsDatabaseReference.objects.filter(cds=self)


class CdsDatabaseReference(DatabaseReference):
    cds = models.ForeignKey(CDS, on_delete=models.CASCADE)
