This file contains the testing scripts, input and output data for the testing of the JustOrtholog pipeline.

JustOrthologs requires two files as input and it then computes orthology between the two sequences.

python3 justOrthologs.py -q /Users/bensilke/gavins-lab/biol3209/prodigal/data/output/nc_000913.3-mrna.faa -s /Users/bensilke/gavins-lab/biol3209/prodigal/data/output/nc_000963.1-mrna.faa -o output -c -t 16


Might be necessary to write a wrapper; or just begin by comparing two sequences with orthologs.
