from sys import argv
from numpy import log2
from os import stat
import pyTGA
from numba import njit
import numba as nb
import numpy as np
import random
from math import trunc as t

def SpliceImageIntoColors(file):
    f = open(file, "rb")
    
    f.read(12)
    X = int.from_bytes(f.read(2),"little")
    Y = int.from_bytes(f.read(2),"little")
    f.read(2)

    r,g,b = ([],[],[])
    
    for y in range(Y):
        for x in range(X):
            b.append(int.from_bytes(f.read(1),"little"))
            g.append(int.from_bytes(f.read(1),"little"))
            r.append(int.from_bytes(f.read(1),"little"))
            
    f.close()
    return X, Y, r,g,b


def quantizeData(data, k):
    col = ["r","g","b"]
    result = {
        "r":[],
        "g":[],
        "b":[],
    }
    for c in col:
        # print(max(data[c]))
        N = len(data["r"])       
        
        mean = [0 for i in range(256)]
        devi = [0 for i in range(256)]

        # zliczamy częstość występowania wartości
        prevMean = 0
        for i in range(1,N,2):
            newMean = (data[c][i] + data[c][i-1])//2
            mean[prevMean-newMean] += 1
            prevMean = newMean
            # mean[(data[c][i] + data[c][i-1])//2] += 1
            # if t((data[c][i] - data[c][i-1])/2) >= 128:
            #     devi[128] += 1
            # elif t((data[c][i] - data[c][i-1])/2) <= -127:
            #     devi[-127] += 1
            # else:
                # devi[t((data[c][i] - data[c][i-1])/2)] += 1
            truncData = 0
            if t((data[c][i] - data[c][i-1])/2) >= 127:
                truncData = 127
            elif t((data[c][i] - data[c][i-1])/2) <= -128:
                truncData = -128
            else:
                truncData = t((data[c][i] - data[c][i-1])/2)

            devi[128 + truncData] += 1
            # devi[128 + t((data[c][i] - data[c][i-1])/2)] += 1
        
        # print(mean)
        # MEANS
        mbuckets = [(0,256)]
        while len(mbuckets) < 2**k:
            maxI = 0
            maxSum = 0

            # maksymalne wiadro
            for i in range(len(mbuckets)):
                a,b = mbuckets[i]
                if b-a > 1 and sum(mean[a:b]) > maxSum:
                    maxSum = sum(mean[a:b])
                    maxI = i
            
            if maxSum == 0:
                for i in range(len(mbuckets)):
                    a,b = mbuckets[i]
                    if b-a >= 2:
                        maxI = i
                        break

            a,b = mbuckets[maxI]
            half = sum(mean[a:b]) / 2
            halfj = b
            acc = 0
            # print(maxSum,maxI)
            # znajdywanie połowy
            for j in range(a,b):
                acc += mean[j]
                if acc >= half:
                    halfj = j+1
                    break
            if halfj == b:
                acc = 0
                for j in range(b-1,a,-1):
                    acc += mean[j]
                    if acc >= half:
                        halfj = j
                        break

            mbuckets.pop(maxI)
            mbuckets.insert(maxI,(halfj,b))
            mbuckets.insert(maxI,(a,halfj))
            # print(mbuckets)
        

            
        # DEVIATIONS
        dbuckets = [(0,256)]
        while len(dbuckets) < 2**k:
            maxI = 0
            maxSum = 0

            # maksymalne wiadro
            for i in range(len(dbuckets)):
                a,b = dbuckets[i]
                if b-a > 1 and sum(devi[a:b]) > maxSum:
                    maxSum = sum(devi[a:b])
                    maxI = i
            a,b = dbuckets[maxI]
            half = sum(devi[a:b]) / 2
            halfj = b
            acc = 0

            # znajdywanie połowy
            for j in range(a,b):
                acc += devi[j]
                if acc >= half:
                    halfj = j+1
                    break
            if halfj == b:
                acc = 0
                for j in range(b-1,a,-1):
                    acc += devi[j]
                    if acc >= half:
                        halfj = j
                        break

            dbuckets.pop(maxI)
            dbuckets.insert(maxI,(halfj,b))
            dbuckets.insert(maxI,(a,halfj))
        

        # print("ENDEXP-----------------------")        

        
        print("MBUCKETS",mbuckets)

        mCodebook = []
        for a,b in mbuckets:
            mCodebook.extend([ 
                # średnia z tego wiadra
                (b-a)*(b+a-1)//2 //(b-a) for z in range(a,b)
            ])

        dCodebook = []
        for a,b in dbuckets:
            dCodebook.extend([ 
                # średnia z tego wiadra
                (b-a)*(b+a-1)//2 //(b-a) for z in range(a,b)
            ])
        prevMean = 0
        
        # print("MCODEBOOK",mCodebook)
        print("QUANT:")
        print("Means: ",end="")
        for i in range(1,10,2):
            print((data[c][i] + data[c][i-1])//2,end=" ")
        print()
        print("Quant: ",end="")
        for i in range(1,N,2):
            newMean = (data[c][i] + data[c][i-1])//2
            # ind = prevMean - newMean
            ind = mCodebook[prevMean - newMean]
            
            result[c].append(ind)
            if i < 10:
                print(ind,end=" ")
            # prevMean = ind
            prevMean = (prevMean - ind)%256
            # prevMean = newMean
            # result[c].append(data[c][i])
            # result[c].append(mCodebook[(data[c][i] + data[c][i-1])//2])
            # result[c].append(dCodebook[t((data[c][i] - data[c][i-1])/2)])

            if data[c][i] == 0:
                result[c].append(ind)
                continue


            truncData = 0

            if t((data[c][i] - data[c][i-1])/2) >= 127:
                truncData = 127
            elif t((data[c][i] - data[c][i-1])/2) <= -128:
                truncData = -128
            else:
                truncData = t((data[c][i] - data[c][i-1])/2)
            result[c].append(dCodebook[128+truncData] - 128)

            # if t((data[c][i] - data[c][i-1])/2) >= 128:
            #     result[c].append(dCodebook[128])
            # elif t((data[c][i] - data[c][i-1])/2) <= -127:
            #     result[c].append(dCodebook[-127])
            # else:
            #     result[c].append(dCodebook[t((data[c][i] - data[c][i-1])/2)])

            # # Debug
            # result[c].append((data[c][i] + data[c][i-1])//2)
            # if data[c][i] - data[c][i-1] >= 0:
            #     result[c].append((data[c][i] - data[c][i-1])//2)
            # else:
            #     result[c].append(-((data[c][i-1] - data[c][i])//2))
        
        print("")
    return result


from pprint import pprint
def decodeToTGA(X,Y, data, outFileName):
    tgaData = [[] for i in range(Y)]

    col = ["r","g","b"]
    
   
    res = []
    prevMean= {'r':0,'g':0,'b':0}
    for y in range(Y):
        for x in range(X):
            i = y*X+x
            if i%2==0:
                for c in prevMean:
                    data[c][i] = (prevMean[c] - data[c][i]) % 256
                    # data[c][i] = (prevMean[c] - data[c][i])
                    # print(data[c][i], prevMean)
                    prevMean[c] = data[c][i]
                r = (data["r"][i]-data["r"][i+1] + 256) % 256 if data["r"][i]-data["r"][i+1] > 0 else 0
                g = (data["g"][i]-data["g"][i+1] + 256) % 256 if data["g"][i]-data["g"][i+1] > 0 else 0
                b = (data["b"][i]-data["b"][i+1] + 256) % 256 if data["b"][i]-data["b"][i+1] > 0 else 0
                tgaData[y].append((
                    r,
                    g,
                    b,
                ))
                res.append({'r':r,'g':g,'b':b})
            else:
                r = (data["r"][i-1]+data["r"][i] + 256) % 256 if data["r"][i-1]-data["r"][i] > 0 else 0
                g = (data["g"][i-1]+data["g"][i] + 256) % 256 if data["g"][i-1]-data["g"][i] > 0 else 0
                b = (data["b"][i-1]+data["b"][i] + 256) % 256 if data["b"][i-1]-data["b"][i] > 0 else 0
                tgaData[y].append((
                    r,
                    g,
                    b,
                ))
                res.append({'r':r,'g':g,'b':b}) 
    
    
    # pprint(tgaData)
    tgaData.reverse()
    # tgaData =  reversed(tgaData)
    image = pyTGA.Image(data=tgaData)
    
    image.save(outFileName)

    return res

    
import matplotlib.pyplot as plt

def ex():
    file = argv[1]
    k = int(argv[2])
    # image = argv[2]

    col = ["r","g","b"]

    data = {}

    X,Y, data[col[0]],data[col[1]],data[col[2]] = SpliceImageIntoColors(file)

    # coebook1, codebook2, encodedData =  generateCodebooksAndData(data)
    result =  quantizeData(data,k)

    res = decodeToTGA(X,Y, result, "res")

    # DEBUG ---------------------------------------
    for c in col:
        happv = [0 for i in range(256)]
        happq = [0 for i in range(256)]
        yax = [0 for i in range(256)]
        diff = 0
        for i in range(X*Y):
            v = data[c][i]
            q = res[i][c]
            happv[v] += 1
            happq[q] += 1
            # if i%2 == 0 and i > 1:
            #     print(q, data[c][i] - data[c][i-2])
            # if abs(v-q)>100:
            #     print("--------------------")
            #     print(v,q,abs(v-q))
            #     print(i-1,result[c][i-1])
            #     print(i,result[c][i])
            #     print(i+1,result[c][i+1])
            #     print(i-1,data[c][i-1])
            #     print(i,data[c][i])
            #     print(i+1,data[c][i+1])
            #     print("--------------------")
            #     yax[abs(v-q)] += 1
            
        # print( c, "- diff:",diff)
        # plt.plot(range(256),yax)
        # plt.show()
        # plt.plot(range(256),happv)
        # plt.show()
        # plt.plot(range(256),happq)
        # plt.show()
    # DEBUG ---------------------------------------

    for c in col:
        mse = 0
        SNR = 0
        for i in range(X*Y):
            v = data[c][i]
            q = res[i][c]

            mse += (v - q) ** 2
            SNR += v ** 2
        print( c, "- mse:",mse)
        if mse == 0:
            print( c, "- SNR: inf")
        else:
            SNR/=mse
            mse/= Y*X
            print( c, "- SNR:",SNR)
    
    mse = 0
    SNR = 0
    for i in range(X*Y):
        v = [data['r'][i] , data['g'][i] , data['b'][i]]
        q = [res[i]['r'] , res[i]['g'] , res[i]['b']]

        mse += (abs(v[0]-q[0])+abs(v[1]-q[1])+abs(v[2]-q[2])) ** 2
        SNR += (v[0]+v[1]+v[2]) ** 2
    SNR/=mse
    mse/= Y*X
    print( "RGB - mse:",mse)
    print( "RGB - SNR:",SNR)




# experiment()

ex()

# WNIOSKI
# Gdy jest dużo krawędzi to metoda działa gorzej niż kwantyzacja kolorów,
# dla gładkich przejść jest zdecydowanie lepsza
# (według danych, z wyglądu poza artefaktami dzielenia zawsze jest dobrze)