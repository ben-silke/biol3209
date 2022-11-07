import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django
django.setup()



from gene.utils import ProdigalResultParser
from gene.models import Gene
import csv


# src/genetifinder/parsers
os.chdir("../")
print(os.listdir())
import numpy as np

def run_file(id, iteration, all_file_count):
    directory = "testing/data/"
    location = "output/prodigal/"

    mrna_ext = ".mrna.faa"
    gbk_ext = ".coords.gbk"

    mrna_file = directory + location + id + "/" + id + mrna_ext
    print(f"{mrna_file=}")
    with open(mrna_file) as file:
        parser = ProdigalResultParser(file)
        prodigal_genes = parser.run()
        if "." in id:
            # locus is not stored with the decimal point
            id = id.split(".")[0]

        annotated_genes = Gene.objects.filter(locus=id).order_by('start')
        starts = np.array([int(number) for number in annotated_genes.values_list('start')])
        total = len(prodigal_genes) - 1
        rows = []
        correct = 0
        for i, gene in enumerate(prodigal_genes):
            row = [gene.get('name')]
            first = int(gene.get('start'))
            last = int(gene.get('end'))
            closest = get_closest(starts, first)

            matches = annotated_genes.filter(first_base=closest)
            print(
                f'Parsing {gene.get("name")} - {iteration}//{all_file_count}.{i}/{total}: {first}..{last}')

            for match in matches:
                row.append(match.name)

                five_prime = match.first_base - first
                three_prime = last - match.last_base

                row.extend(
                    'p5,p3,a5,a3',
                    [first,last,match.first_base, match.last_base],
                    five_prime,
                    three_prime,
                    five_prime+three_prime,
                    five_prime/three_prime
                )

                correct += 1
                rows.append(row)
            if not matches:
                row.extend([first, last, "failure", "No match found"])
    all_rows = []

    titles = [
        "Gene name (prodigal)",
        "Annotated Gene Name",
        "Start",
        "End",
        "Equal",
        "Raw Location",
    ]
    all_rows.append(titles)
    all_rows.append(['correct', correct, 'total', total, 'gene_count', gene_count])
    all_rows.extend(rows)

    with open(f"testing/results/prodigal/fuzzy/{id}_prodigal_test.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)

    return id, correct, total, gene_count

def get_closest(array, start):
    # array = np.asarray(arr)
    idx = (np.abs(array-start)).argmin()
    return array[idx]



def run_files(directory):
    files = [file.replace(".gb", "") for file in os.listdir(directory)]
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
            id, correct, total, gene_count = run_file(file, iteration, all_file_count)
            output.append([id, correct, total, gene_count])
        except Exception as e:
            print('________________________________________________failure______________________________')
            print(file, e)
            output.append(["FAIL", file, e])

    with open("testing/results/prodigal_overall.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(output)

run_files('data/soil/soil_reference_genomes')
