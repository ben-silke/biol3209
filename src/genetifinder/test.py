
from parsers import faa_parser

directory = 'testing/data/'
location = 'output/prodigal/'
id = 'NC000913'

mrna_ext = '.mrna.faa'
gbk_ext = '.coords.gbk'

mrna_file = directory+location+id+'/'+id+mrna_ext

with open(mrna_file) as file:
    parser = faa_parser(file)
    parser.run()