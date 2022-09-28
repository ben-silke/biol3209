
# read two files;

# compare the cds sequences


# read the first file - the source of truth; create the necessary objects or assess against the data base?
# need to add a section to the database to record the location of the actual gene.

# read the second file; the output of prodigal or genemark and then see if any of the gene locations match up.

# Check location -> if this location is wrong this is most likely an error.
# Check translation for somewhat of a match


# what scores should be used? what assertion of success is there?

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")

os.chdir('../../')
import django

django.setup()
from parsers.faa_parser import ProdigalResultParser
from gene.models import Gene

print(os.listdir())
directory = 'testing/data/'
location = 'output/prodigal/'
id = 'NC_000913'

mrna_ext = '.mrna.faa'
gbk_ext = '.coords.gbk'

mrna_file = directory+location+id+'/'+id+mrna_ext
print(f'{mrna_file=}')
print('/home/ben/research/biol3209/testing/data/output/prodigal/NC_000913/NC_000913.mrna.faa')
with open(mrna_file) as file:
    parser = ProdigalResultParser(file)
    prodigal_genes = parser.run()
    annotated_genes = Gene.objects.filter(locus=id)
    for gene in prodigal_genes:
        print(gene)
    # Can either create database objects here or just lookup from here.
    # it is probably better to use the database which was created because this will allow multiple searches here
