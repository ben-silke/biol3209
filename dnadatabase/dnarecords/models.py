from uuid import uuid4
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

    @property
    def db_features(self):
        return DatabaseFeatureReference.objects.filter(database=self)

    @property
    def db_sequences(self):
        return DatabaseSequenceReference.objects.filter(database=self)


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
    mol_type = models.CharField(null=True, max_length=50)
    # sequence = models.TextField(null=True, help_text="The nt's of the sequence")
    organism = models.CharField(null=True, max_length=50)
    length = models.IntegerField(null=True)
    definition = models.TextField(null=True)
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

    def __str__(self) -> str:
        references = [f'{reference.database.name}:{reference.db_xref}' for reference in self.database_reference]
        return f'ACC: {self.accession}. Ref:{references}. Features Count: {self.feature_set.count()}.'


class Feature(concept):
    type = models.CharField(null=True, max_length=50)
    raw_location = models.CharField(max_length=50, null=True)

    start_location = models.IntegerField(null=True)
    end_location = models.IntegerField(null=True)
    # if you delete a sequence the features will all be deleted
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)

    other_data = models.JSONField(
        null=True,
        help_text="Other information about the feature. Information which does not fit into the above categories. properties of features may not be consistent across features so this area will contain the general information.",
    )

    @property
    def database_reference_set(self):
        return DatabaseFeatureReference.objects.filter(feature=self)


class DatabaseReference(concept):
    database = models.ForeignKey(Database, on_delete=models.CASCADE, null=True)
    db_xref = models.CharField(null=True, max_length=50)
    text = models.CharField(
        null=True, max_length=50, help_text="Original text of the reference"
    )


class DatabaseFeatureReference(DatabaseReference):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)


class DatabaseSequenceReference(DatabaseReference):
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, null=True)


class SequenceHomology(models.Model):
    uuid = models.UUIDField(default=uuid4())
    id = models.AutoField(primary_key=True)

    description = models.TextField(null=True)
    type = models.CharField(null=True, max_length=50)

    base_sequence = models.OneToOneField(
        Sequence, related_name="base_sequence", on_delete=models.CASCADE
    )
    relation_sequence = models.ForeignKey(
        Sequence, related_name="related_sequences", on_delete=models.CASCADE
    )

class FeatureHomology(models.Model):
    id = models.AutoField(primary_key=True)

    description = models.TextField(null=True)

    base_feature = models.OneToOneField(
        Feature, related_name="base_feature", on_delete=models.CASCADE
    )
    relation_feature = models.ForeignKey(
        Feature, related_name="related_feature", on_delete=models.CASCADE
    )


class GenbankRecord(Sequence):
    pass


class EnsemblRecord(Sequence):
    pass
