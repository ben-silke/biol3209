from django.db import models

from .model_utils import concept


class Database(concept):
    name = models.CharField(null=True, max_length=255)
    description = models.TextField(
        null=True,
        help_text="A description of the database. More information if no url can be provided.",
    )
    url = models.URLField(
        null=True,
    )


class Environment(concept):
    name = models.CharField(null=True, max_length=255)
    description = models.TextField(
        null=True, help_text="A description of the environment or type of environment."
    )

    @property
    def community(self):
        return Sequence.objects.filter(environment=self)


class Taxonomy(concept):
    name = models.CharField(null=True, max_length=255)
    description = models.TextField(
        null=True,
        help_text="A description of the taxonomy. More information if no url can be provided.",
    )

    @property
    def sequence_set(self):
        return Sequence.objects.filter(taxonomy=self)


class Sequence(concept):
    locus = models.TextField(null=True)
    accession = models.CharField(null=True, max_length=50)
    version = models.CharField(null=True, max_length=50)
    mol_type = models.Choices(("DNA"), ("RNA"))
    sequence = models.TextField(null=True, help_text="The nt's of the sequence")
    organism = models.CharField(null=True, max_length=50)

    description = models.TextField(null=True)
    gene = models.CharField(null=True, max_length=50)

    other = models.JSONField(
        null=True,
        help_text="Other information about the sequence. Information which does not fit into the above categories.",
    )

    taxonomy = models.ManyToManyField(Taxonomy)
    environment = models.ManyToManyField(Environment)

    @property
    def feature_set(self):
        return Feature.objects.filter(sequence=self)

    @property
    def database_reference(self):
        return DatabaseSequenceReference.objects.filter(sequence=self)

    @property
    def homology_relation_set(self):
        return SequenceHomology.objects.filter(base_sequence=self)


class Feature(concept):
    type = models.CharField(null=True, max_length=50)
    location = models.CharField(max_length=50, null=True)
    # if you delete a sequence the features will all be deleted
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)

    @property
    def database_reference_set(self):
        return DatabaseFeatureReference.objects.filter(feature=self)


class DatabaseReference(concept):
    database = models.ManyToManyField(Database)
    db_xref = models.CharField(null=True, max_length=50)


class DatabaseFeatureReference(DatabaseReference):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)


class DatabaseSequenceReference(DatabaseReference):
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, null=True)


class SequenceHomology(models.Model):
    id = models.UUIDField(primary_key=True)
    description = models.CharField(null=True, max_length=50)
    type = models.CharField(null=True, max_length=50)

    base_sequence = models.OneToOneField(
        Sequence, related_name="base_sequence", on_delete=models.CASCADE
    )
    relation_sequence = models.ForeignKey(
        Sequence, related_name="related_sequences", on_delete=models.CASCADE
    )


class GenbankRecord(Sequence):
    pass


class EnsemblRecord(Sequence):
    pass
