#!/bin/bash
# NC_015733
ids=(NC_015733)
echo ${ids[@]}

for id in "${ids[@]}"
do
    echo $id
    fetch_commmand="$(efetch -db nuccore -id $id -format fasta)"
    echo $fetch_command >> data/input/$id.fasta
    mkdir data/output/$id

    # prodigal_command="$(prodigal -i data/input/$id.fasta -o data/output/$id/$id.coords.gbk -d data/output/$id/$id.mrna.faa -a data/output/$id/$id.protein.faa)"
    strace -o data/trace_data/$id.txt -c -tt prodigal -i data/input/$id.fasta -o data/output/$id/$id.coords.gbk -d data/output/$id/$id.mrna.faa -a data/output/$id/$id.protein.faa

    # python script to compare the sequences.
done
# THis needs to recursively loop
# Can use trace to track how long the processes take
# ben@ben-amd:~/research/biol3209/prodigal_testing$ strace -o trace -c -Ttt ./pipeline.sh
