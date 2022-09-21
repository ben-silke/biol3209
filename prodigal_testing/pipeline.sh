#!/bin/bash

ids=(NC_000964.3)
echo ${ids[@]}

for id in "${ids[@]}"
do
    echo $id
    a="$(efetch -db nuccore -id $id -format fasta)"
    echo $a >> data/input/$id.fasta

    prodigal -i data/input/$id.fasta -o data/output/$id.coords.gbk -d data/output/$id.mrna.faa
    # python3 /Users/bensilke/gavins-lab/notJustOrthologs/JustOrthologs-master/justOrthologs.py -q data/output/$id.mrna.faa -s data/output/$id.mrna.faa -o output -c -t 16

done
