from sys import argv
from numpy import log2
from os import stat

name = argv[1]
# name = "L4/testy/example1.tga"

def wholeEntropy():
    n = int(256**3)
    Occurance = [0]*n
    f = open(name, "rb")
    
    f.read(12)
    X = int.from_bytes(f.read(2),"little")
    Y = int.from_bytes(f.read(2),"little")
    f.read(2)
    
    for y in range(Y):
        for x in range(X):
            v = int.from_bytes(f.read(3),"little")
            Occurance[v] += 1
            
    f.close()

    return entropy(Occurance)
    print("Entropia RGB : ",entropy(Occurance))

def rgbEntropy():
    Occurance = {
        "r": [0]*256,
        "g": [0]*256,
        "b": [0]*256
    }
    f = open(name, "rb")
    
    f.read(12)
    X = int.from_bytes(f.read(2),"little")
    Y = int.from_bytes(f.read(2),"little")
    f.read(2)
    
    for y in range(Y):
        for x in range(X):
            b = int.from_bytes(f.read(1),"little")
            g = int.from_bytes(f.read(1),"little")
            r = int.from_bytes(f.read(1),"little")
            Occurance["b"][b] += 1
            Occurance["g"][g] += 1
            Occurance["r"][r] += 1
            
    f.close()
    
    # print("Entropia R   : ",entropy(Occurance["r"]))
    # print("Entropia  G  : ",entropy(Occurance["g"]))
    # print("Entropia   B : ",entropy(Occurance["b"]))
    return [
        entropy(Occurance["r"]),
        entropy(Occurance["g"]),
        entropy(Occurance["b"])
    ]

def predictor(n,w,nw, i):
    match i:
        case 0:
            return w
        case 1:
            return n
        case 2:
            return nw
        case 3:
            return n+w-nw
        case 4:
            return n+(w-nw)//2
        case 5:
            return w+(n-nw)//2
        case 6:
            return (n+w)//2
        case 7:
            if nw >= max(w,n):
                return max(w,n)
            elif nw <= min(w,n):
                return min(w,n)
            else:
                return w+n-nw

def wholeEncoding():
    n = int(256**3)
    Occurance = [[0]*256 for i in range(8)]
    
    f = open(name, "rb")
    # f = open("L4/testy/example0.tga", "rb")
    
    f.read(12)
    X = int.from_bytes(f.read(2),"little")
    Y = int.from_bytes(f.read(2),"little")
    f.read(2)
    
    upperRow = [0]*(X+1)

    for y in range(Y):
        prevVal = 0
        newUpperRow = [0]*(X+1)
        for x in range(X):
            v = int.from_bytes(f.read(3),"little")
            for i in range(8):
                Occurance[i][(v - predictor(upperRow[x+1],prevVal,upperRow[x],i))%256] += 1
            newUpperRow[x+1] = v
            prevVal = v
        upperRow = newUpperRow
        

    f.close()
    
    return [entropy(Occurance[i]) for i in range(8)]

    for i in range(8):
        print("Predyktor",i,":")
        print("    Entropia RGB : ",entropy(Occurance[i]))
    

def rgbEncoding():
    Occurance = [{
        "r": [0]*256,
        "g": [0]*256,
        "b": [0]*256
    } for i in range(8)]
    # Occurance = [[0]*256 for i in range(8)]
    
    f = open(name, "rb")
    # f = open("L4/testy/example0.tga", "rb")
    
    f.read(12)
    X = int.from_bytes(f.read(2),"little")
    Y = int.from_bytes(f.read(2),"little")
    f.read(2)
    
    upperRow = {
        "r": [0]*(X+1),
        "g": [0]*(X+1),
        "b": [0]*(X+1)
    }

    for y in range(Y):
        prevVal = {
            "r": 0,
            "g": 0,
            "b": 0
        }
        newUpperRow = {
            "r": [0]*(X+1),
            "g": [0]*(X+1),
            "b": [0]*(X+1)
        }
        for x in range(X):
            b = int.from_bytes(f.read(1),"little")
            g = int.from_bytes(f.read(1),"little")
            r = int.from_bytes(f.read(1),"little")
            for i in range(8):
                Occurance[i]["b"][(b - predictor(upperRow["b"][x+1],prevVal["b"],upperRow["b"][x],i))%256] += 1
                Occurance[i]["g"][(g - predictor(upperRow["g"][x+1],prevVal["g"],upperRow["g"][x],i))%256] += 1
                Occurance[i]["r"][(r - predictor(upperRow["r"][x+1],prevVal["r"],upperRow["r"][x],i))%256] += 1
            newUpperRow["b"][x+1] = b
            newUpperRow["g"][x+1] = g
            newUpperRow["r"][x+1] = r
            prevVal["b"] = b
            prevVal["g"] = g
            prevVal["r"] = r
        upperRow = newUpperRow
        

    f.close()

    return {
        "r": [entropy(Occurance[i]["r"]) for i in range(8)],
        "g": [entropy(Occurance[i]["g"]) for i in range(8)],
        "b": [entropy(Occurance[i]["b"]) for i in range(8)]
    } 

    for i in range(8):
        print("Predyktor",i,":")
        print("    Entropia R   : ",entropy(Occurance[i]["r"]))
        print("    Entropia  G  : ",entropy(Occurance[i]["g"]))
        print("    Entropia   B : ",entropy(Occurance[i]["b"]))


def entropy(Occurance):
    s = sum(Occurance)
    H = 0
    for x in range(len(Occurance)):
        p = Occurance[x] / s
        if p != 0:
            H += p * (-1)*log2(p) 
    return H


def results():
    print("$$$ Predyktory $$$")
    whole = wholeEncoding()
    rgb = rgbEncoding()

    for i in range(8):
            print("Predyktor",i,":")
            print("    Entropia RGB : ",whole[i])
            print("    Entropia R   : ",rgb["r"][i])
            print("    Entropia  G  : ",rgb["g"][i])
            print("    Entropia   B : ",rgb["b"][i])

    print("$$$ Najlepsze $$$")
    i = whole.index(min(whole))
    print(" RGB : Predyktor",i)
    print("    Entropia:",whole[i])

    r = rgb["r"].index(min(rgb["r"]))
    print(" R   : Predyktor",r)
    print("    Entropia:",rgb["r"][r])

    g = rgb["g"].index(min(rgb["g"]))
    print("  G  : Predyktor",g)
    print("    Entropia:",rgb["g"][g])

    b = rgb["b"].index(min(rgb["b"]))
    print("  B  : Predyktor",b)
    print("    Entropia:",rgb["b"][b])

    print("$$$ Oryginał $$$")

    print("Entropia oryginalna RGB : ",wholeEntropy())
    e = rgbEntropy()
    print("Entropia oryginalna R   : ",e[0])
    print("Entropia oryginalna  G  : ",e[1])
    print("Entropia oryginalna   B : ",e[2])

results()