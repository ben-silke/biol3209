import datetime
import os

from readline import get_endidx


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django


django.setup()

from cogent3.parse.genbank import MinimalGenbankParser
from dnarecords.models import (
    Database,
    DatabaseFeatureReference,
    DatabaseSequenceReference,
    Environment,
    Feature,
    Sequence,
    Taxonomy,
)


def main():
    print("Running get_statistics.py")

    # get_references('InterPro')
    # get_references('UniProtKB/Swiss-Prot')

def get_references(db_name):
    print(f'Getting reference data for {db_name=}')
    database = Database.objects.get(name=db_name)
    references = DatabaseFeatureReference.objects.filter(database=database)

    unique_db_xrefs = {reference.db_xref for reference in references}
    counts = {
        db_xref: references.filter(db_xref=db_xref).count()
        for db_xref in unique_db_xrefs
    }
    high_counts = {
        key: value
        for key, value in counts.items() if value > 1
    }
    print(f'HIGH COUNTS__________{len(high_counts)}')

    # print(f'{high_counts=}')

    accs = []
    for i, ref in enumerate(high_counts.keys()):
        references = (DatabaseFeatureReference.objects.filter(db_xref=ref))
        accession = [reference.feature.sequence.accession for reference in references]
        acc = set(accession)
        for a in acc:
            if not 'NC_000964' in a:
                accs.append(a)
                print(f'{i} -- {a=}')
        print(f'{i} -- {accs=}')

    raise ValueError(accs)
    for ref in high_counts.keys():
        get_sequence(ref)

def get_sequence(db_xref):
    print(f'_______________{db_xref=}________________________')
    references = DatabaseFeatureReference.objects.filter(db_xref=db_xref)

    for reference in references:
        feature = reference.feature
        print(f'{feature.other_data=}')
        sequence = feature.sequence
        print(sequence)


def query_swiss_prot(db_xref):
    # https://www.uniprot.org/uniprotkb/P12345
    # https://rest.uniprot.org/uniprotkb/P12345.fasta

    references = DatabaseFeatureReference.objects.filter(db_xref=db_xref)
    for reference in references:
        # reference.
        pass


if __name__ == "__main__":
    main()
