import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django
django.setup()

from dnarecords.models import Database
from gene.models import CdsDatabaseReference, Gene, GeneDatabaseReference, CDS

import click

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
    "--environment",
    "--e",
    is_flag=True,
    help="Flag to prompt the inclusion of an environment.",
)
def main(d, create=False, test=False, fail_file=None, environment=None):
    files = [
        os.path.join(d, f)
        for f in os.listdir(d)
        if os.path.isfile(os.path.join(d, f))
    ]
    fails = run(files)

    return fails


def parse_file(file):
    genes = []
    try:
        print(f'Parsing {file}')
        with open(file) as f:
            parser = MinimalGenbankParser(f)
            for p in parser:
                genes.append(p)
        # print(f'{genes=}')
        print(type(genes))

        return genes
    except Exception as e:
        print(f'Failed to parse {file} because {e}')
        return None

    return genes

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
    return fails


def create_objects(genes):
    fails = []
    gene = None
    # print(f'{len(genes)}')
    gene = genes[0]
    # for gene in genes:
    print(f'{type(gene["features"])=}')
    if features := gene.get('features', None):
        for feature in features:

            if 'gene' in feature['type']:
                print(feature)
                gene = feature
                references = gene.pop('db_xref', [])

                gene = Gene.objects.create(name=gene.get('gene'))
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
# {'type': 'gene', 'raw_location': ['190..255'], 'location': [<cogent3.parse.genbank.Location object at 0x1048ddc40>], 'gene': ['thrL'], 'locus_tag': ['b0001'], 'gene_synonym': ['ECK0001'], 'db_xref': ['ASAP:ABE-0000006', 'ECOCYC:EG11277', 'GeneID:944742']}
            elif 'CDS' in feature['type']:
                print(feature)
                # create feature
                cds = feature
                references = cds.pop('db_xref', [])

                cds = CDS.objects.create(name=cds.get('gene'))

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
