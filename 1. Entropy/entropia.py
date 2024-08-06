from sys import argv
from numpy import log2


Occurance = [0]*256
InOrderOccurance = [ [0]*256 for i in range(256)]

with open(argv[1], "rb") as f:
    prevbyte = 0
    while rawbyte := f.read(1):
        byte = int.from_bytes(rawbyte,"big")
        Occurance[byte] += 1
        InOrderOccurance[prevbyte][byte] += 1
        prevbyte = byte
        
if sum(Occurance) == 0:
    print("Plik pusty")
    exit()

Probability = [Occurance[i] / sum(Occurance) for i in range(256)]
ConditionalProbability = [[[0] for i in range(256)] for j in range(256)]
for i in range(256):
    for j in range(256): # i | j
        if Occurance[j] == 0:
            ConditionalProbability[i][j] = 0
        else:
            ConditionalProbability[i][j] = InOrderOccurance[j][i] / Occurance[j]
# ConditionalProbability = [[0 if Occurance[j] == 0 else InOrderOccurance[j][i] / Occurance[j] for i in range(256)] for j in range(256)]

H = sum(Probability[x] * (-1)*log2(Probability[x]) if Probability[x] != 0 else 0  for x in range(256))
HCond = sum(Probability[x] * sum(ConditionalProbability[y][x] * (-1)*log2(ConditionalProbability[y][x])  if ConditionalProbability[y][x] != 0 else 0 for y in range(256)) for x in range(256))

print("Entropia:",H)
print("Entropia warunkowa:",HCond)
print("Różnica:",H - HCond)