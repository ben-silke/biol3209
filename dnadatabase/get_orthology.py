import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django
django.setup()

from gene.models import CdsDatabaseReference, Gene, GeneDatabaseReference, CDS
import requests
# some thing like

# for gene in gene names:
# (just the high ones)
genes =[('dnaA', 352),
 ('dnaN', 270),
 ('recF', 188),
 ('gyrB', 143),
 ('yaaA', 67),
 ('gyrA', 35),
 ('gnd', 24),
 ('thrA', 17),
 ('thrC', 17),
 ('thrB', 17),
 ('thrL', 16),
 ('mioC', 12),
 ('yidA', 11),
 ('ravA', 10),
 ('asnC', 10),
 ('viaA', 10),
 ('kup', 10)
]



def get_gene(name):
    genes = Gene.objects.filter(name=name)
    references = []
    for gene in genes:
        for ref in GeneDatabaseReference.objects.filter(gene=gene):
            references.append(ref)

        for ref in gene.cds.database_set:
            references.append(ref)

    return references
# get gene

# get db referecne
base = 'https://www.ebi.ac.uk/interpro/api/'

def get_interpro_info(query, id):

    response = requests.get(base+query+id)
    if not response.status_code == 200:
        return []
    if results := response.json().get('results', None):
        return results
    else:
        return response.json()

def get_ortho_db_set(id):
    base = "https://www.orthodb.org/search?"
    query = f"query={id}&"
    tags = "ncbi=1"
    response = requests.get(base+query+tags)
    if not response.status_code == 200:
        return []
    if results := response.json().get('data', []):
        return results
    else:
        return []

def check_endpoints(endpoints):
    results = {}
    for endpoint in endpoints:
        print(endpoint.database.name)
        print(endpoint.db_xref)
        if endpoint.database.name == 'InterPro':
            results[endpoint.text] = get_interpro_info('entry/interpro/', endpoint.db_xref)
        elif endpoint.database.name == 'UniProtKB/Swiss-Prot':
            results[endpoint.text] = get_interpro_info('entry/interpro/protein/uniprot/', endpoint.db_xref)
        elif endpoint.database.name == 'GeneID':
            results[endpoint.text] = get_ortho_db_set(endpoint.db_xref)

    return results


ls = [
 ('dnaN', 270),
 ('recF', 188),
 ('gyrB', 143),
 ('yaaA', 67),
 ('gyrA', 35),
 ('gnd', 24),
 ]


for l in ls:
    l = l[0]
    print(f'____________ Gene Name === {l} _______________________')
    endpoints = get_gene(l)
    results = check_endpoints(endpoints)
    print(results)
