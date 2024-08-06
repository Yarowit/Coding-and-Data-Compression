from sys import argv
from numpy import log2
from os import stat


Occurance = [0]*256
def entropy(name):
    with open(name, "rb") as f:
        while rawbyte := f.read(1):
            byte = int.from_bytes(rawbyte,"big")
            Occurance[byte] += 1
            
    if sum(Occurance) == 0:
        print("Plik pusty")
        exit()

    Probability = [Occurance[i] / sum(Occurance) for i in range(256)]

    H = sum(Probability[x] * (-1)*log2(Probability[x]) if Probability[x] != 0 else 0  for x in range(256))
    return H
    print("Entropia",name,":",H)

o = stat(argv[1]).st_size
k = stat(argv[2]).st_size
print("Rozmiar oryginalny:   ",o)
print("Rozmiar skompresowany:",k)
print("Entropia oryginalna:   ",entropy(argv[1]))
print("Entropia skompresowana:",entropy(argv[2]))
print("Kompresja:",k/o)