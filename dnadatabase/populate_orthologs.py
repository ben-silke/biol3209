
import django
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")


django.setup()


from gene.models import CDS, CdsDatabaseReference, Gene, GeneDatabaseReference
from dnarecords.models import Database
from cogent3.parse.genbank import MinimalGenbankParser
import click
import csv
import pandas

from orthologs.models import OrthologReference, QuestGene
os.chdir('../')


def run():
    print(os.listdir())

    files = [f for f in os.listdir('data/quest4orthologs/Bacteria') if '.idmapping' in f]

    with open('populate_orthologs_output.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(
            [
                'file',
                'gene',
                'ortholog_ids',
            ]
        )
        for i, name in enumerate(files):
            print(f'running {i}/{len(files)} _____ {name}  ')
            file = f'data/quest4orthologs/Bacteria/{name}'
            ortholog_ids = []
            # errors = []
            with open(file) as file:
                idmapping = csv.reader(file, delimiter="\t")
                gene_id = ''
                gene = None
                ids = []

                for id in idmapping:
                    # print(id)
                    # ['P47624', 'EMBL', 'L43967']

                    if not gene_id == id[0]:
                        if gene:
                            writer.writerow([
                                name,
                                gene.uniprot_accession,
                                ids,
                                ])
                        print(name,gene,ids)
                        gene_id = id[0]
                        gene = QuestGene.objects.create(uniprot_accession=gene_id, file_name=name)
                        ids = []

                    database = Database.objects.get_or_create(name=id[1])[0]
                    ortholog_id = id[2]
                    ids.append(f'{database.name}__{ortholog_id}')

                    try:
                        ortholog_reference = OrthologReference.objects.get(db_xref=ortholog_id)
                    except:
                        ortholog_reference = OrthologReference.objects.create(database=database, db_xref=ortholog_id)

                    gene.reference.add(ortholog_reference)

                    if id[1] == "OMA":
                        gene.oma_reference_id = ortholog_id










def main():
    run()

if __name__ == "__main__":
    main()
