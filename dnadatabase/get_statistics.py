import datetime
import os


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


if __name__ == "__main__":
    main()
