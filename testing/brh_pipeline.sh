


#!/bin/bash
# NC_015733
echo ${ids[@]}


files=(UP000002524_243230 UP000000577_243231 UP000000429_85962 UP000000557_251221 UP000000718_289376 UP000000431_272561 UP000001408_189518 UP000000798_224324 UP000007719_515635 UP000001570_224308 UP000001425_1111708 UP000002526_224911 UP000002438_208964 UP000000425_122586 UP000001414_226186 UP000001025_243090 UP000000625_83333 UP000008183_243274 UP000000807_243273 UP000001973_100226 UP000002008_324602 UP000002521_190304 UP000001584_83332)

# change this depending on the input
folder=data/quest4orthologs/Bacteria

ext=_DNA.fasta
cd ../
eval ls
mkdir testing/data/output/rbhs
mkdir testing/data/output/rbh_intermediate

for file in "${files[@]}"
do
    echo $file
    for file_two in "${files[@]}"
    do
    echo $file_two
    if [[ "$file" == "$file_two" ]]; then
    # double chekc these labels
        echo "files are equal"
    else
        echo $file.$file_two
        # eval ls

        exec "run_blast.sh $folder/$file$ext $folder/$file_two$ext testing/data/output/rbh_intermediate/$file.$file_two"
        exec "find_rbh_blast.sh testing/data/output/rbh_intermediate/$file.$file_two testing/data/output/rbhs/$file.$file_two"
        break
    fi
    done
    break
    # strace -o data/justorthologs/trace_data/$id.txt -c -tt ____command_goes_here____
    # python script to compare the sequences.
done
# this needs to recursively loop
# Can use trace to track how long the processes take
# ben@ben-amd:~/research/biol3209/prodigal_testing$ strace -o trace -c -Ttt ./pipeline.sh
