
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


import django


django.setup()
# src/genetifinder/parsers
import csv

import gff3_parser

from gene.models import Gene


os.chdir('../')
print(os.listdir())
directory = 'testing/data/'
location = 'output/genemark/'
id = 'NC_000913'

gff_ext = '.genemark.txt'

gff_file = directory+location+id+'/'+id+gff_ext
print(f'{gff_file=}')
# with open(gff_file) as file:
genes = gff3_parser.parse_gff3(gff_file, verbose=True, parse_attributes=True)

print(genes)
annotated_genes = Gene.objects.filter(locus=id)
total = len(prodigal_genes) - 1
rows=[]
correct = 0
    # rows.append(['Gene name (prodigal)', 'Annotated Gene Name', 'Start', 'End', 'Equal', 'Raw Location'])
    # for i, gene in enumerate(prodigal_genes):
    #     row = [gene.get('name')]
    #     # print(gene)
    #     first = int(gene.get('start'))
    #     print(type(first))
    #     last = int(gene.get('end'))
    #     sequence = gene.get('sequence')
    #     print(f'Parsing {gene.get("name")}- {i}/{total}: {first}..{last}')
    #     matches = annotated_genes.filter(first_base=first)
    #     correct_match = False
    #     for match in matches:
    #         row.append(match.name)
    #         if match.first_base == first and match.last_base == last:
    #             correct_match = True
    #         row.extend([
    #             first,
    #             last,
    #             correct_match,
    #             match.raw_location,
    #             ])
    #     if not matches:
    #         row.extend([
    #             first,
    #             last,
    #             "failure",
    #             'No match found'
    #         ])

    #     if correct_match:
    #         correct += 1
    #     rows.append(row)

print(f'{correct=}')
with open('testing/results/prodigal_test.csv','w') as f:
    writer = csv.writer(f)
    writer.writerows(rows)


    # Can either create database objects here or just lookup from here.
    # it is probably better to use the database which was created because this will allow multiple searches here
