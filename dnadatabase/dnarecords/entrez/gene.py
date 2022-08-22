import requests
from dnarecords.models import Sequence
from utils import SequenceCreator




class GeneSequenceCreator(SequenceCreator):
    """
    Class to use the entrez utilities to get and analyze gene sequences.
    """


# GET archive/id/:id	Uses the given identifier to return its latest version
# GET homology/id/:id	Retrieves homology information (orthologs) by Ensembl gene id
# GET xrefs/id/:id	Perform lookups of Ensembl Identifiers and retrieve their external references in other databases
