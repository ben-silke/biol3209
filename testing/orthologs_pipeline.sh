


#!/bin/bash
# NC_015733
ids=(NC_015733)
echo ${ids[@]}

# change this depending on the input
folder=prodigal
just_ortho_dir=notJustOrthologs/justOrthologs/

for id in "${ids[@]}"
do
    for second in "${ids[@]}"
    do
    if ["$id" != "$second"]; then
    # double chekc these labels
        python3 $just_ortho_dir/justOrthologs.py -q data/output/$folder/$id/$id.mrna.faa -s data/output/$folder/$second/$second.mrna.faa -o data/output/justorthologs/orthologs.$id.$second.faa -c -t 16
    fi
    done
    # strace -o data/justorthologs/trace_data/$id.txt -c -tt ____command_goes_here____
    # python script to compare the sequences.
done
# this needs to recursively loop
# Can use trace to track how long the processes take
# ben@ben-amd:~/research/biol3209/prodigal_testing$ strace -o trace -c -Ttt ./pipeline.sh
