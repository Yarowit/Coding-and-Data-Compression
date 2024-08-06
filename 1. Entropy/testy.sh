#!/usr/bin/bash
# set -x
for file in $(ls testy1)
do
    echo \# testowanie $file
    python3 entropia.py testy1/$file
    echo
done
# set +x