#!/bin/bash
#Script to filter reciprocal blast results for best hits
#Usage: bash findRBH.sh PATH/TO/QUERY/BLAST/RESULTS PATH/TO/DB/BLAST/RESULTS
#Usage ex: bash findRBH.sh blast.outfmt6 blast_reciprocal.outfmt6
#Input query blast results file
queryPath="$1"
#Input DB reciprocal blast results file
dbPath="$2"


#Final output files
outFileRBH="blast_RBH.txt"
outFileSummary="blast_RBH_summary.txt"
#Add headers to output RBH files
echo "queryHit,dbHit" > $outFileRBH
echo "queryHits,dbHits,bestHits" > $outFileSummary
#Output start status message
echo "Recording RBH..."
#Loop over query blast results
while IFS=$'\t' read -r f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12
do
#Determine RBH to DB blast results
if grep -q "$f2"$'\t'"$f1"$'\t' $dbPath; then #RBH
echo "$f1,$f2" >> $outFileRBH
fi
done < $queryPath
#Output summary of RBH
queryHits=$(wc -l "$queryPath" | cut -d ' ' -f 1)
dbHits=$(wc -l "$dbPath" | cut -d ' ' -f 1)
bestHits=$(($(wc -l "$outFileRBH" | cut -d ' ' -f 1)-1))
echo "$queryHits","$dbHits","$bestHits" >> $outFileSummary
#Output end status message
echo "Finished recording RBH!"
