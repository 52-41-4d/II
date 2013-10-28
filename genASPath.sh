#!/bin/bash

RBAFile=rba #location of rba file
INPUT=/scratch/SIGCOMM14/Input/ASPaths
OUTPUT=/scratch/SIGCOMM14/Output/ASPaths

for file in `ls $INPUT`
do
    fullSource=$INPUT/$file
    asFile=${file%.bz2}.txt
    bzcat $fullSource | $RBAFile | grep "ASPATH" | sed 's/ASPATH: //g' > $OUTPUT/$asFile
    echo "Completed processing AS file: $file"
done

# write logic here for Neo4j insert
