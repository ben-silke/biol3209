import os


os.chdir("../../")
from parsers.faa_parser import ProdigalResultParser


print(os.listdir())
directory = "testing/data/"
location = "output/prodigal/"
id = "NC_000913"

mrna_ext = ".mrna.faa"
gbk_ext = ".coords.gbk"

mrna_file = directory + location + id + "/" + id + mrna_ext
print(f"{mrna_file=} | ")
print(
    "/home/ben/research/biol3209/testing/data/output/prodigal/NC_000913/NC_000913.mrna.faa"
)
with open(mrna_file) as file:
    parser = ProdigalResultParser(file)
    genes = parser.run()

    # Can either create database objects here
