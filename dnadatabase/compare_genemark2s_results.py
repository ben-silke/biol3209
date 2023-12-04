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

from django.db.models import Q
from gene.models import Gene
from gene.utils import GffParser
import click

os.chdir("../../")
print(os.listdir())


def run_file(id, iteration, all_file_count):
    location = "output/genemark/"

    gff_ext = ".genemark.txt"

    gff_file = f"testing/data/{location}{id}/{id}{gff_ext}"
    print(f"{gff_file=}")
    # with open(gff_file) as file:

    with open(gff_file, "r") as f:
        parser = GffParser(f)
        genes = parser.run()
        metadata = parser.metadata

    rows = [
        [
            "Gene name (genemark)",
            "Annotated Gene Name/ locus",
            "Start",
            "End",
            "correct match",
            "Raw Location/ failure",
            "first_base",
            "last_base",
        ]
    ]
    success = 0
    total = len(genes)
    for i, gene in enumerate(genes):
        print(f'{iteration}/{all_file_count}.{i}/{total} - {gene.get("gene_id")}')
        if "." in id:
            # locus is not stored with the decimal point
            id = id.split(".")[0]
        annotated_genes = Gene.objects.filter(locus=id)
        gene_count = annotated_genes.count()
        has_match = False
        row = [gene.get("gene_id")]
        first = gene.get("start")
        last = gene.get("end")
        locus = gene.get("locus")

        if m := annotated_genes.filter(
            Q(first_base=first) | Q(last_base=last)
        ):
            for match in m:
                row.append(match.name)

                if match.first_base == first and match.last_base == last:
                    has_match = True

                row.extend(
                    [
                        first,
                        last,
                        has_match,
                        match.raw_location,
                        match.first_base,
                        match.last_base,
                    ]
                )
        else:
            row.extend([locus, first, last, has_match, "Failure"])

        if has_match:
            success += 1

        rows.append(row)

    all_rows = [['correct', success, 'total', total], *rows]
    # rows = all_rows

    print(f"{success=}/{total=}")

    with open(f"testing/results/genemark/{id}_genemark_test.csv", "w") as f:
        writer = csv.writer(f)
        print(f'{type(all_rows)=}')
        writer.writerows(all_rows)

    return id, success, total, gene_count

    # Can either create database objects here or just lookup from here.
    # it is probably better to use the database which was created because this will allow multiple searches here


directory = "data/soil/soil_reference_genomes"


def run_files(directory):
    files = [file.replace(".gb", "") for file in os.listdir(directory)]
    files = [
        # 'NC_000913.3',
        'NC_014623.1'
    ]
    all_file_count = len(files)
    print(files)

    output = [["id", "correct", "total", "gene_count"]]
    for iteration, file in enumerate(files):
        # try:
        id, correct, total, gene_count = run_file(file, iteration, all_file_count)
        output.append([id, correct, total, gene_count])
        # except Exception as e?:
            # output.append(["FAIL", file, e])

    with open("testing/results/genemark_overall.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(output)


# run_files('data/soil/soil_reference_genomes')


@click.command()
@click.option('--files', '--f')
def run(files):
    if type(files) != list:
        files = [files]

    all_file_count = len(files)
    print(files)

    output = [["id", "correct", "total", "gene_count"]]
    for iteration, file in enumerate(files):
        # try:
        id, correct, total, gene_count = run_file(file, iteration, all_file_count)
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
