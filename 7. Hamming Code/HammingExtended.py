from random import sample, randrange, random

# generuje plik w postaci $size 4-bitowych znaków (liczb)
def generateRandomFile(size):
    return [toBits(randrange(0,16)) for i in range(size)]

# zaszumia każdy bit z prawdopodobieństwem p
def noise(messages,p):
    stat = 0
    for i in range(len(messages)):
        for j in range(len(messages[i])):
            if random() < p:
                messages[i][j] ^= 1
                stat += 1
    print(p,stat)
    return messages

# liczba na tablicę bitów
def toBits(n):
    res = []
    for i in range(4):
        bit = n % 2
        res.append(bit)
        n //= 2
    return res

# flip n bitów
def flipBits(mat,n):
    for bit in sample(range(0,8),n):
        mat[bit] ^= 1
    return mat

# kodowanie tablicy bitów
def encode(m):
    # macierz wygenerowana przez h = x^7-1 / x^3+x+1
    G =  [
        [ 1, 0, 0, 0],
        [ 1, 1, 0, 0],
        [ 0, 1, 1, 0],
        [ 1, 0, 1, 1],
        [ 0, 1, 0, 1],
        [ 0, 0, 1, 0],
        [ 0, 0, 0, 1],
        [ 1, 1, 1, 1] # bit parzystości
    ]

    message = []
    
    for row in G:
        val = 0
        for i in range(len(row)):
            val ^= row[i] * m[i]
        message.append(val)
    
    return message

def encodeFile(file):
    res = []

    for byte in file:
        res.append(encode(byte))

    return res

def decodeFile(file):
    res = []
    errors = [0,0,0]
    for byte in file:
        decoded, error = decode(byte)
        errors[error] += 1
        res.append(decoded)


    return res, errors

def compare(original, decoded):
    different = 0

    for line in range(len(original)):
        if original[line] != decoded[line]:
            different += 1
    
    return different

def compareHowManyBitsWrong(original, decoded):
    different = 0
    different = [0,0,0,0,0]
    for line in range(len(original)):
        diff = 0
        for i in range(4):
            if original[line][i] != decoded[line][i]:
                diff += 1
        different[diff] += 1

    
    return different[1:5]
            
# odkodowanie tablicy bitów
def decode(message):
    H = [
        [ 0, 0, 1, 0, 1, 1, 1],
        [ 0, 1, 0, 1, 1, 1, 0],
        [ 1, 0, 1, 1, 1, 0, 0],
    ]

    res = []

    for row in H:
        val = 0
        
        for i in range(len(row)):
            val ^= row[i] * message[i]
        res.append(val)
    
    # print(message,res, checkParityBit(encoded[0]))

    # naprawa
    errors = 0
    if(sum(res) > 0):
        errors = 1
        for i in range(7):
            if H[0][i] == res[0] and H[1][i] == res[1] and  H[2][i] == res[2]:
                message[i] ^= 1
                break
    
    if checkParityBit(message) == 1 and errors == 1:
        errors = 2
    
    

    # dedukujemy wartości z macierzy
    return [message[0], message[1]^message[0],message[5],message[6]], errors

# zwraca 1 jeśli są różne
def checkParityBit(message):
    H = [
        [ 1, 1, 1, 1, 1, 1, 1]
    ]
    acc = message[-1]
    for bit in message[0:-1]:
        acc ^= bit
    
    return acc

import matplotlib.pyplot as plt
def statistics():
    
    fileSize = 1000
    # xax = range(100,5,-5)
    xax = range(5,100,5)
    yax1 = []
    yax2 = []
    yax3 = []

    yaxd1 = []
    yaxd2 = []
    yaxd3 = []
    diffor = []
    for prob in xax:

        noiseProbability = 1/prob
        noiseProbability = prob/100

    # print("Długość pliku:",fileSize)
    # print("...")

        file = generateRandomFile(fileSize)
        encoded = encodeFile(file)

        encoded = noise(encoded, noiseProbability)
        decoded, errors = decodeFile(encoded)
        differences = compare(file, decoded)
        diffAll = compareHowManyBitsWrong(file,decoded)

        noisedOriginal = noise(file,noiseProbability)
        differencesOriginal = compare(file, decoded)
        diffor.append(differencesOriginal)
        yax1.append(differences)
        yax2.append(errors[1])
        yax3.append(errors[2])
        yaxd1.append(diffAll[1])
        yaxd2.append(diffAll[2])
        yaxd3.append(diffAll[3])
    
    xax = range(5,100,5)
    plt.plot(xax,yax1,label="niezgodne 4-bitowe")
    # plt.plot(xax,yax2,label="pojedyncze")
    plt.plot(xax,yax3,label="podwójne")
    plt.plot(xax,diffor,label="szum orygialnego")
    # plt.plot(xax,yaxd1,label="ile 4-bitowych ma 1 błąd")
    # plt.plot(xax,yaxd2,label="ile 4-bitowych ma 2 błąd")
    # plt.plot(xax,yaxd3,label="ile 4-bitowych ma 3 błąd")
    plt.legend()
    plt.show()
    # print("Niezgodne bloki 4-bitowe:",differences)
    # print("\nWykryte błędy:")
    # print("    Pojedncze -",errors[1])
    # print("    Podwójne  -",errors[2])

    # print(differences,errors)

statistics()
exit(0)
# PROGRAM
    
fileSize = 1000
noiseProbability = 0.01

print("Długość pliku:",fileSize)
print("...")

file = generateRandomFile(fileSize)
encoded = encodeFile(file)

encoded = noise(encoded, noiseProbability)
decoded, errors = decodeFile(encoded)
differences = compare(file, decoded)

print("Niezgodne bloki 4-bitowe:",differences)
print("\nWykryte błędy:")
print("    Pojedncze -",errors[1])
print("    Podwójne  -",errors[2])
# print(differences,errors)

# wynik ma sens, bo jeśli błąd nie dotyczy bitów 0,1,5 lub 6 to dostaniemy poprawną wiadomość