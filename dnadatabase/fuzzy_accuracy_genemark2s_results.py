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

import click
from gene.utils import GffParser
from gene.models import Gene
from django.db.models import Q
import csv
import django
import os

import numpy as np



# django.setup()
# src/genetifinder/parsers


os.chdir("../../")
print(os.listdir())


def run_file(id, iteration, all_file_count):
    file_name = id.split('.')[0]

    mrna_file = 'testing/results/genemark/'+file_name+'_genemark_test.csv'

    print(mrna_file)
    success = 0
    total = 0
    if "." in id:
        # locus is not stored with the decimal point
        id = id.split(".")[0]

    annotated_genes = Gene.objects.filter(locus=id).order_by('first_base')
    gene_count = annotated_genes.count()
    ls = [int(number[0])
          for number in annotated_genes.values_list('first_base')]
    starts = np.array(ls)
    results = []

    # total = len(genes) - 1
    with open(mrna_file) as file:
        rows = csv.reader(file)
        correct = 0


        for row in rows:
            print(row)
            if (len(row)) > 4:
                if row[4] == 'True':
                    print(row[4])
                    total += 1
                    five_prime = 0
                    three_prime = 0
                    ratio = 0
                    sum = 0
                    result_row = [
                        row[0],
                        row[1],
                        'match=True',
                        [five_prime, three_prime],
                        ratio,
                        sum
                    ]
                    correct += 1
                    results.append(result_row)
                    print(result_row)

                elif row[4] == "False":
                    start = int(row[2])
                    end = int(row[3])
                    matches = []
                    print(f'finding {start} {end}')

                    if potential_gene := annotated_genes.filter(first_base=start):
                        matches = potential_gene
                    elif potential_gene := annotated_genes.filter(last_base=end):
                        matches = potential_gene
                    else:
                        closest = get_closest(starts, start)
                        matches = annotated_genes.filter(first_base=closest)
                        print(f'working {closest}')

                    for match in matches:
                        # row.append(match.name)

                        five_prime = match.first_base - start
                        three_prime = end - match.last_base
                        ratio = five_prime/three_prime if three_prime > 0 else 0
                        sum = five_prime + three_prime
                        result_row = [
                            row[0],
                            row[1],
                            'match=True',
                            [five_prime, three_prime],
                            ratio,
                            sum
                        ]

                        correct += 1
                        results.append(result_row)

                    if not matches:
                        row.extend([start, end, "failure", "No match found"])

    all_rows = []

    all_rows.append(['correct', correct, 'total', total, 'gene_count', gene_count])
    all_rows.extend(results)
    # rows = all_rows

    print(f"{correct=}/{total=}")

    with open(f"testing/results/fuzzy/genemark_fuzzy/{id}_genemark_test.csv", "w") as f:
        writer = csv.writer(f)
        print(f'{type(all_rows)=}')
        writer.writerows(all_rows)

    return id, correct, total, gene_count

    # Can either create database objects here or just lookup from here.
    # it is probably better to use the database which was created because this will allow multiple searches here


def get_closest(array, start):
    # array = np.asarray(arr)
    idx = (np.abs(array-start)).argmin()
    return array[idx]


@click.command()
@click.option('--files', '--f')
def run(files):
    if not type(files) == list:
        files = [files]

    all_file_count = len(files)
    print(files)

    output = []
    output.append(["id", "correct", "total", "gene_count"])
    for iteration, file in enumerate(files):
        # try:
        id, correct, total, gene_count = run_file(
            file, iteration, all_file_count)
        output.append([id, correct, total, gene_count])
        print(output)
        # except Exception as e?:
        # output.append(["FAIL", file, e])

    with open("testing/results/genemark_overall.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(output)


if __name__ == '__main__':
    run()


"""

python3 compare_genemark2s_results.py --f

"""
