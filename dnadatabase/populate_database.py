import django

django.setup()
import os
import csv
import click

from cogent3.parse.genbank import MinimalGenbankParser
from dnarecords.model_utils import concept
from dnarecords.models import (
    Database,
    DatabaseFeatureReference,
    DatabaseSequenceReference,
    Environment,
    Feature,
    Sequence,
    Taxonomy,
)


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
    '--ff',
    help="File to write failed entries to.",
)

def main(d, create=False, test=False, fail_file=None):
    import django

    django.setup()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")

    if d:

        files = [
            os.path.join(d, f)
            for f in os.listdir(d)
            if os.path.isfile(os.path.join(d, f))
        ]
        print(files)

    else:
        print(
            "Please provide a directory of genbank files. Test mode will run a single entry."
        )
        test = True

    if test:
        # change this
        os.chdir("/Users/bensilke/gavins-lab/biol3209/")
        files = ["data/soil_reference_genomes/NC_000913.3.gb"]

    failures = {}
    if create:
        genes = run(files)
        failures = create_database_objects(genes)

    print(f"There are {Database.objects.count()} databases.")
    print(
        f"There are {DatabaseFeatureReference.objects.count()} database feature references."
    )
    print(
        f"There are {DatabaseSequenceReference.objects.count()} database sequence references."
    )
    print(f"There are {Feature.objects.count()} features.")
    print(f"There are {Sequence.objects.count()} sequences.")

    if failures:
        if not fail_file:
            print(failures)
        else:
            with open(fail_file, "w") as f:
                writer = csv.DictWriter(f, fieldnames=["accession", "failures"])
                writer.writeheader()
                writer.writerows(failures)


def run(files):
    genes = []
    for file in files:
        with open(file) as f:
            parser = MinimalGenbankParser(f)
            for p in parser:
                genes.append(p)
    print(type(genes))
    print(type(genes[0]))
    return genes


def create_database_objects(genes):
    environment = Environment.objects.create(
        name="Soil",
        description="Soil Microbiome: https://pubmed.ncbi.nlm.nih.gov/27935589/",
    )

    failures = {}

    for i, gene in enumerate(genes):
        accession = gene['accession']
        failures[accession] = []
        print(f'{i=} and {gene["accession"]=}')
        # For feature creation
        features = gene.pop("features", [])

        # Database creations
        db = gene.pop("dblink", [])

        # Many to many
        taxonomy = gene.pop("taxonomy", [])

        # Data Transformation
        length = int(gene.pop("length", []))

        # other data
        references = gene.pop("references", [])
        topology = gene.pop("topology", None)
        comment = gene.pop("comment", None)

        data = {
            "length": length,
            "accession": gene.pop("accession", None),
            "version": gene.pop("version", None),
            "mol_type": gene.pop("mol_type", None),
            "sequence": gene.pop("sequence", None),
            "organism": gene.pop("organism", None),
            "definition": gene.pop("definition", None),
            "gene": gene.pop("gene", None),
            "other": {
                "topology": topology,
                "comment": comment,
                "references": references,
            },
        }

        # print(f'{data=}')

        # Create Sequence
        try:
            sequence = Sequence.objects.create(**data)
            sequence.save()
        except:
            failures[accession].append('Sequence creation failed.')
            print(f'Sequence creation failed for {gene["accession"]}')
            continue

        try:
            # Create database
            print(f"{db=}")
            db = db.replace("DBLINK", "").strip()
            db_string = db.split(" ")
            databases = []
            i = 0
            while i < len(db_string):
                database = db_string[i]
                location = db_string[i + 1]
                i += 2
                databases.append(
                    {
                        "database": database,
                        "location": location,
                        "text": f"{database}:{location}",
                    }
                )

            for database in databases:
                db_obj = Database.objects.get_or_create(name=database["database"])[0]
                db_reference = DatabaseSequenceReference.objects.create(
                    sequence=sequence,
                    database=db_obj,
                    db_xref=database["location"],
                    text=database["text"],
                )
        except:
            print(f'Database creation failed for {gene["accession"]}')
            failures[accession].append('Database creation failed.')
            continue

        # Create features
        for feature in features:
            try:
                 # Create database references (need to create database)
                # Remove location because it is a cogent3 object and I dont want to deal with it
                feature.pop("location", None)

                feature_type = feature.pop("type", None)
                raw_location = feature.pop("raw_location", None)

                db_xrefs = feature.pop("db_xref", [])
                data = {
                    "type": feature_type,
                    "raw_location": raw_location,
                    "other_data": feature,
                }
                if raw_location:
                    try:
                        raw_location = raw_location[0]
                        if "complement" in raw_location:
                            raw_location = raw_location.replace("complement(", "").replace(
                                ")", ""
                            )
                        locations = raw_location.split("..")
                        start_location = int(locations[0])
                        end_location = int(locations[1])
                        data.update(
                            {
                                "start_location": start_location,
                                "end_location": end_location,
                            }
                        )
                    except Exception as e:
                        print(f"No location added. {e}. Error found with {raw_location}")

                feature_object = Feature.objects.create(sequence=sequence, **data)
                for db_ref in db_xrefs:
                    db_reference = db_ref.split(":")
                    ref = db_reference[0]
                    location = db_reference[1]

                    db_obj = Database.objects.get_or_create(name=ref)[0]
                    db_reference = DatabaseFeatureReference.objects.create(
                        feature=feature_object,
                        database=db_obj,
                        db_xref=location,
                        text=db_ref,
                    )
            except Exception as e:
                failures[accession].append(f'Feature {data} creation failed.')
                continue

        # create and add taxonomy
        for tax in taxonomy:
            try:
                print(tax)
                list = Taxonomy.objects.filter(name=tax)
                if list:
                    taxonomy_object = list[0]
                else:
                    taxonomy_object = Taxonomy.objects.create(name=tax)
                sequence.taxonomy.add(taxonomy_object)
            except:
                failures[accession].append(f'Taxonomy {tax} creation failed.')
                print(f'Taxonomy {tax} creation failed.')
                continue

        # Create environment
        try:
            sequence.environment.add(environment)
            sequence.save()
        except:
            failures[accession].append('Environment creation failed.')
            print(f'Environment creation failed for {gene["accession"]}')
            continue

    return failures

if __name__ == "__main__":
    main()
