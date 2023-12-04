import requests


# ortholog finder
ORTHO_DB_ENDPOINT = url = "https://www.orthodb.org/"

# search?query=3433707"
def get_orthoDB_id(query):
    query = f"?query={query}"

    response = requests.get(f"{ORTHO_DB_ENDPOINT}search{query}")
    return response.json()["data"]


# "https://www.orthodb.org/orthologs?id={ids[2]}"
def get_orthologs_from_orthoDB(id):
    """
    Returns the orthologs from OrthoDB using the OrthoDB id.
    id = OrthoDB cluster id
    """
    query = f"?id={id}"

    response = requests.get(f"{ORTHO_DB_ENDPOINT}orthologs{query}")
    if response.json()["data"]:
        return response.json()["data"][0]["genes"]


def get_interpro_info(query, id):
    base = "https://www.ebi.ac.uk/interpro/api/"

    response = requests.get(base + query + id)
    assert response.status_code == 200
    if results := response.json().get("results", None):
        return response.json()["results"]
    else:
        return response.json()
