
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
import csv

from gene.models import Gene
# src/genetifinder/parsers
from gene.utils import ProdigalResultParser


os.chdir('../')
print(os.listdir())


def run_file(id):
    directory = 'testing/data/'
    location = 'output/prodigal/'

    mrna_ext = '.mrna.faa'
    gbk_ext = '.coords.gbk'

    mrna_file = directory+location+id+'/'+id+mrna_ext
    print(f'{mrna_file=}')
    with open(mrna_file) as file:
        parser = ProdigalResultParser(file)
        prodigal_genes = parser.run()
        if '.' in id:
            # locus is not stored with the decimal point
            id = id.split('.')[0]
        annotated_genes = Gene.objects.filter(locus=id)
        gene_count = annotated_genes.count()
        total = len(prodigal_genes) - 1
        rows=[]
        correct = 0
        rows.append(['Gene name (prodigal)', 'Annotated Gene Name', 'Start', 'End', 'Equal', 'Raw Location'])
        for i, gene in enumerate(prodigal_genes):
            row = [gene.get('name')]
            # print(gene)
            first = int(gene.get('start'))
            print(type(first))
            last = int(gene.get('end'))
            sequence = gene.get('sequence')
            print(f'Parsing {gene.get("name")}- {i}/{total}: {first}..{last}')
            matches = annotated_genes.filter(first_base=first)
            correct_match = False
            for match in matches:
                row.append(match.name)
                if match.first_base == first and match.last_base == last:
                    correct_match = True
                row.extend([
                    first,
                    last,
                    correct_match,
                    match.raw_location,
                    ])
            if not matches:
                row.extend([
                    first,
                    last,
                    "failure",
                    'No match found'
                ])

            if correct_match:
                correct += 1
            rows.append(row)

    print(f'{correct=}/{total}')

    with open(f'testing/results/prodigal/{id}_prodigal_test.csv','w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return id, correct, total, gene_count

    # Can either create database objects here or just lookup from here.
    # it is probably better to use the database which was created because this will allow multiple searches here

def run_files(directory):
    files = [
        file.replace('.gb', '').split('.')[0] for file in os.listdir(directory)
    ]
    print(files)

    output = []
    output.append(['id', 'correct', 'total', 'gene_count'])
    for file in files:
        try:
            id, correct, total, gene_count = run_file(file)
            output.append([id,correct,total,gene_count])
        except:
            output.append(['FAIL',file])

        with open('testing/results/genemark_overall.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(output)
