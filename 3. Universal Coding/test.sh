#!/usr/bin/bash

# set -x

# g++ -O3 -o e mergedEncoder.cpp
# g++ -O3 -o d mergedDecoder.cpp
# set +x

folder="testy2"

for file in $(ls $folder)
do
    f=$folder/$file
    echo \$ $file

    ./e $folder/$file $1 > temp

    python3 entropia.py $folder/$file temp

    ./d temp $1 > out

    echo cmp:
    cmp $f out

done