
import django
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")


django.setup()


from gene.models import CDS, CdsDatabaseReference, Gene, GeneDatabaseReference
from orthologs.models import QuestGene, OrthologReference
from dnarecords.models import Database
from cogent3.parse.genbank import MinimalGenbankParser
import click
import csv
import pandas


from django.db.models import Count, Q


# data = list(QuestGene.objects.annotate(total=Count('oma_reference_id')).values('total', 'oma_reference_id'))

# for d in data:
# for d in data:
    # if d['total'] != 0:
        # print(d)

# print(data)


# AYIGYNH
# print(QuestGene.objects.filter(oma_reference_id='AYIGYNH'))


# for qg in QuestGene.objects.all():
    # print(qg.oma_reference_id)

orthologs = OrthologReference.objects.all()

orthologs = orthologs.filter(database__name='OMA')

data = {}
for d in orthologs:
    if d.orthologs > 1:
        print(d.orthologs)
        if d.database.name == 'OMA':
            row = [d.database.name]
            for orth in d.get_orthologs():
                row.append(orth.uniprot_accession)
            data[d.db_xref] = row

print (data)
