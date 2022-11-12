
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django
django.setup()
import click

from gene.utils import ProdigalResultParser
from gene.models import Gene
import csv

import os
# src/genetifinder/parsers
os.chdir("../../")
# print(os.listdir())
import numpy as np

def run_file(id, iteration, all_file_count):
    file_name = id.split('.')[0]

    mrna_file = 'testing/results/prodigal/'+file_name+'_prodigal_test.csv'
    print(mrna_file)
    # print(f"{mrna_file=}")
    with open(mrna_file) as file:
        # parser = ProdigalResultParser(file)
        # prodigal_genes = parser.run()

        if "." in id:
            # locus is not stored with the decimal point
            id = id.split(".")[0]
        annotated_genes = Gene.objects.filter(locus=id).order_by('first_base')
        gene_count = annotated_genes.count()
        ls = [int(number[0]) for number in annotated_genes.values_list('first_base')]
        print(ls)
        starts=np.array(ls)
        rows = csv.reader(file)
        total = 0
        correct = 0
        results = []

        for row in rows:
            if row[4] == 'True':
                total+= 1
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
                correct += True

                results.append(result_row)

            elif row[4] == "No match found":
                start = int(row[1])
                end = int(row[2])
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

    with open(f"testing/results/fuzzy/prodigal_fuzzy/{id}_prodigal_test.csv", "w") as f:
        writer = csv.writer(f)
        print(f'{type(all_rows)=}')
        writer.writerows(all_rows)

    return id, correct, total, gene_count

def get_closest(array, start):
    # array = np.asarray(arr)
    idx = (np.abs(array-start)).argmin()
    return array[idx]


@click.command()
@click.option('--files', '--f')
def run(files):
    if not type(files) == list:
        files = [files]
    # files = [file.replace(".gb", "") for file in os.listdir(directory)]
    print(files)
    # files = [
    #     'NC_000913.3'
    # ]

    output = []
    output.append(["id", "correct", "total", "gene_count"])
    all_file_count = len(files)
    print(all_file_count)
    for iteration, file in enumerate(files):
        try:
            id, correct, total, gene_count = run_file(
                file, iteration, all_file_count)
            output.append([id, correct, total, gene_count])
            print(output)
        except Exception as e:
            print(
                '________________________________________________failure______________________________')
            print(file, e)
            output.append(["FAIL", file, e])


if __name__ == '__main__':
    run()
