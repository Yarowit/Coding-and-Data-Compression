#!/usr/bin/bash

set -x

g++ -O3 -o d decoder.cpp
g++ -O3 -o e encoder.cpp
set +x

for file in $(ls testy1)
do
    echo \n\n
    f=testy1/$file
    echo %%%%%%%%%% $file %%%%%%%%%%

    echo kompresja:
    time ./e testy1/$file > temp

    echo -n Rozmiar oryginalny    : 
    wc -c $f | cut -d' ' -f1
    echo -n Rozmiar skompresowany : 
    wc -c temp | cut -d' ' -f1

    echo dekompresja:
    time ./d < temp > out

    cmp $f out

    echo pipe:
    time ./e testy1/$file | ./d > out

    cmp $f out
done