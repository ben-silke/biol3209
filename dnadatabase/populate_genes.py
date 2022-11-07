import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django


django.setup()

import csv

import click

from cogent3.parse.genbank import MinimalGenbankParser
from dnarecords.models import Database
from gene.models import CDS, CdsDatabaseReference, Gene, GeneDatabaseReference


@click.command()
@click.option("--d", help="Directory of genbank files", default=None)
@click.option(
    "--test",
    "--t",
    help="Test mode enabled to query a single entry.",
    default=False,
    is_flag=True,
)
@click.option(
    "--create",
    "--c",
    help="Create mode enabled to create new entries.",
    default=False,
    is_flag=True,
)
@click.option(
    "--fail_file",
    "--ff",
    help="File to write failed entries to.",
)
@click.option(
    "--output",
    "--o",
    help="Flag to prompt the inclusion of an environment.",
)
def main(d, create=False, test=False, fail_file=None, output=""):
    files = [
        os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))
    ]
    fails = run(files)
    print("________________FAILS________________________")
    print(fails)
    file = output + "gene_population_failures.csv"
    with open(file) as f:
        writer = csv.writer()

        writer.writerow(["file-name", "failure reason"])

        for k, v in fails:
            writer.writerow([k, v])

    return fails


def parse_file(file):
    genes = []
    errors = []
    try:
        print(f"Parsing {file}")
        with open(file) as f:
            parser = MinimalGenbankParser(f)
            for p in parser:
                genes.append(p)
        # print(f'{genes=}')

        return genes
    except Exception as e:
        error = f"Failed to parse {file} because {e}"
        print(error)
        errors.append(error)
        return errors


def run(files):
    fails = {}
    total = len(files)
    for i, file in enumerate(files):
        ls = file.split('/')
        locus = ls[len(ls)-1]
        locus = locus.split('.')[0]
        with open(f'/home/ben/research/biol3209/data/fails/{locus}_{i}.csv', 'w') as output_file:
            writer = csv.writer(output_file)
            print(f"attemping to parse {i}/{total} -::- {file}")
            try:
                genes = parse_file(file)
                if genes:
                    f, rows = create_objects(genes)
                    writer.writerows(rows)
                    fails[str(file)] = f
            except Exception as e:
                print(f"failed to parse {file} __ {e}")
                fails[file] = f"failed to parse {file} __ {e}"

    return fails


def create_objects(sequences):
    fails = []
    gene = None
    # print(f'{len(genes)}')
    file = sequences[0]
    locus = file.get("locus", None)
    # for gene in genes:
    rows = []
    if features := file.get("features", None):
        for feature in features:
            row = [locus]
            if "gene" in feature["type"]:
                gene = feature
                row.append(gene)
                references = feature.get("db_xref", [])
                name = feature.get("gene", None)
                raw_location = feature.get("raw_location", None)
                location = feature.get("location", None)
                if name or raw_location or location:
                    gene = Gene.objects.create(name=name)
                    if locus:
                        gene.locus = locus
                    if raw_location:
                        gene.raw_location = raw_location

                    if location:
                        try:
                            gene.first_base = location.first()
                            gene.last_base = location.last()
                        except:
                            row.append(f'failed to get first and last base for {gene.name}')
                            print(f"failed to get first and last base for {gene.name}")
                    gene.save()

                    for reference in references:
                        db_reference = reference.split(":")
                        ref = db_reference[0]
                        location = db_reference[1]

                        db_obj = Database.objects.get_or_create(name=ref)[0]
                        db_ref = GeneDatabaseReference.objects.create(
                            gene=gene, database=db_obj, db_xref=location, text=reference
                        )
                    print(gene)
                    if gene:
                        row.extend([gene, gene.id])
            elif "CDS" in feature["type"]:
                cds = feature
                references = feature.pop("db_xref", [])
                product = feature.get("product", None)
                name = feature.get("gene", None)
                row.append(name)
                translation = feature.get("translation", None)
                id = feature.get("protein_id", None)
                product = feature.get("product", None)
                raw_location = feature.get("raw_location", None)
                location = feature.get("location", None)
                if name or product or id or location or raw_location or translation:
                    cds = CDS.objects.create(name=name)
                    if product:
                        cds.product = product
                    if id:
                        cds.protein_id = id
                    if translation :
                        cds.translation = translation
                    if locus:
                        cds.locus = locus
                    if raw_location:
                        cds.raw_location = raw_location

                    if location:
                        try:
                            cds.first_base = location.first()
                            cds.last_base = location.last()
                        except:
                            print(f"failed to get first and last base for {cds.name}")
                    cds.save()

                    for reference in references:
                        db_reference = reference.split(":")
                        ref = db_reference[0]
                        location = db_reference[1]

                        db_obj = Database.objects.get_or_create(name=ref)[0]
                        db_ref = CdsDatabaseReference.objects.create(
                            cds=cds, database=db_obj, db_xref=location, text=reference
                        )

                    if gene.name == cds.name:
                        cds.gene = gene
                        cds.save()

                    if cds:
                        row.extend([cds, cds.id])
                    else:
                        row.append('fail')

            rows.append(row)
    return fails, rows


if __name__ == "__main__":
    main()
