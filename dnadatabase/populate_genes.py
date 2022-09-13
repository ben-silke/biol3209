import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django
django.setup()

from dnarecords.models import Database
from gene.models import CdsDatabaseReference, Gene, GeneDatabaseReference, CDS

import click
import csv

from cogent3.parse.genbank import MinimalGenbankParser


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
def main(d, create=False, test=False, fail_file=None, output=None):
    files = [
        os.path.join(d, f)
        for f in os.listdir(d)
        if os.path.isfile(os.path.join(d, f))
    ]
    fails = run(files)

    file = output+'gene_population_failures.csv'
    with open(file) as f:
        writer = csv.writer()

        writer.writerow(['file-name', 'failure reason'])

        for k, v in fails:
            writer.writerow([k,v])

    return fails


def parse_file(file):
    genes = []
    errors = []
    try:
        print(f'Parsing {file}')
        with open(file) as f:
            parser = MinimalGenbankParser(f)
            for p in parser:
                genes.append(p)
        # print(f'{genes=}')

        return genes
    except Exception as e:
        error = f'Failed to parse {file} because {e}'
        print(error)
        errors.append(error)
        return errors

def run(files):
    fails = {}
    for file in files:
        try:
            genes = parse_file(file)
            print(f'{type(genes[0])=}')
            print(f'{genes[0].keys()}')
            if genes:
                fails[str(file)] = create_objects(genes)
        except Exception as e:
            print(f'failed to parse {file} __ {e}')
            fails[file] = f'failed to parse {file} __ {e}'
    return fails


def create_objects(sequences):
    fails = []
    gene = None
    # print(f'{len(genes)}')
    file = sequences[0]
    # for gene in genes:
    if features := file.get('features', None):
        for feature in features:

            if 'gene' in feature['type']:
                gene = feature
                references = gene.pop('db_xref', [])
                if name := feature.get('gene', None):
                    gene = Gene.objects.create(name=name)
                    for reference in references:
                        db_reference = reference.split(':')
                        ref = db_reference[0]
                        location = db_reference[1]

                        db_obj = Database.objects.get_or_create(name=ref)[0]
                        db_ref = GeneDatabaseReference.objects.create(
                            gene=gene,
                            database=db_obj,
                            db_xref=location,
                            text=reference
                        )
            elif 'CDS' in feature['type']:
                cds = feature
                references = feature.pop('db_xref', [])
                if name := feature.get('gene', None):
                    cds = CDS.objects.create(name=name)
                    if product := feature.get('product', None):
                        cds.product = product
                    if id := feature.get('protein_id', None):
                        cds.protein_id = id
                    if translation := feature.get('translation', None):
                        cds.translation = translation
                    cds.save()

                    for reference in references:
                        db_reference = reference.split(':')
                        ref = db_reference[0]
                        location = db_reference[1]

                        db_obj = Database.objects.get_or_create(name=ref)[0]
                        db_ref = CdsDatabaseReference.objects.create(
                            cds=cds,
                            database=db_obj,
                            db_xref=location,
                            text=reference
                        )

                    if gene.name == cds.name:
                        cds.gene = gene
                        cds.save()

    return fails

if __name__ == "__main__":
    main()
