#!/bin/bash

g++ -O3 -o e mergedEncoder.cpp
g++ -O3 -o d mergedDecoder.cpp


./test.sh g > res/g
echo g
./test.sh d > res/d
echo d
./test.sh o > res/o
echo o
./test.sh f > res/f
echo f