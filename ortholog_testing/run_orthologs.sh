


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

    # python3 justOrthologs.py -q data/output/nc_000913.3-mrna.faa -s /Users/bensilke/gavins-lab/biol3209/prodigal/data/output/nc_000963.1-mrna.faa -o output -c -t 16

    strace -o data/trace_data/$id.txt -c -tt ____command_goes_here____

    # python script to compare the sequences.
done
# THis needs to recursively loop
# Can use trace to track how long the processes take
# ben@ben-amd:~/research/biol3209/prodigal_testing$ strace -o trace -c -Ttt ./pipeline.sh
