from sys import argv
from numpy import log2
from os import stat
import pyTGA
from numba import njit
import numba as nb
import numpy as np
import random

def readPixels(file):
    Elements = []

    f = open(file, "rb")
    
    f.read(12)
    X = int.from_bytes(f.read(2),"little")
    Y = int.from_bytes(f.read(2),"little")
    f.read(2)
    
    for y in range(Y):
        for x in range(X):
            b = int.from_bytes(f.read(1),"little")
            g = int.from_bytes(f.read(1),"little")
            r = int.from_bytes(f.read(1),"little")
            Elements.append([r,g,b])
            
    f.close()

    return X, Y, Elements

def d(A,B):
    # return np.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2)
    return abs(A[0]-B[0]) + abs(A[1]-B[1]) + abs(A[2]-B[2])


@njit#(parallel=True)
def LBG(Elements, n,sample,empty, empty1d):
    oldCodebook = empty
    newCodebook = sample

    elemSize = len(Elements)
    
    while not np.array_equal(newCodebook, oldCodebook):
        
        methodError = 0
        oldCodebook = newCodebook
        newCodebook = np.copy(empty)
        spaceSize = np.copy(empty1d)

        # przypisanie do centroidu
        for i in nb.prange(elemSize):
            v = Elements[i]
            minDistance = 3*255
            minCentroid = -1
            for centroid in range(n):
                dist = abs(oldCodebook[centroid][0]-v[0]) + abs(oldCodebook[centroid][1]-v[1]) + abs(oldCodebook[centroid][2]-v[2])
                if dist < minDistance:
                    minDistance = dist
                    minCentroid = centroid
            methodError += minDistance
            newCodebook[minCentroid][0] += v[0]
            newCodebook[minCentroid][1] += v[1]
            newCodebook[minCentroid][2] += v[2]
            spaceSize[minCentroid] += 1
        
        
        for i in range(n):
            if spaceSize[i] != 0:
                newCodebook[i][0] //= spaceSize[i]
                newCodebook[i][1] //= spaceSize[i]
                newCodebook[i][2] //= spaceSize[i]
        
    return newCodebook
            
def quantizeVector(v, centroids):
    minDistance = 3*255
    minCentroid = 0
    for centroid in range(len(centroids)):
        dist = d(centroids[centroid], v)
        if dist < minDistance:
            minDistance = dist
            minCentroid = centroid
    return centroids[minCentroid]

def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def quantize():
    file = argv[1]
    image = argv[2]
    n = int(argv[3])

    N = 2**n
    X, Y, Elements = readPixels(file)
    
    # kolory unikalne do losowania
    setE = []   
    for elem in Elements:
        if elem not in setE:
            setE.append(elem)
    
    
    sample = random.sample(setE,N)
    
    npE = np.array(Elements)
    nps = np.array(sample)
    npem3 = np.array([[0,0,0] for i in range(N)])
    npem1 = np.array([0 for i in range(N)])


    codeBook = LBG(npE, N, nps, npem3, npem1)
    

    tgaData = [[] for i in range(Y)]

    mse = 0
    SNR = 0

    for y in range(Y):
        for x in range(X):
            v = Elements[y*X+x]
            c = quantizeVector(v,codeBook)
            tgaData[y].append((c[0],c[1],c[2]))

            mse += d(v,c) ** 2
            SNR += (v[0]+v[1]+v[2]) ** 2
    
    SNR /= mse
    mse /= Y*X
    
    print("n:",n)
    print("Błąd średniokwadratowy:",mse)
    print("Stosunek sygnału do szumu:",SNR)

    image = pyTGA.Image(data=tgaData)
    
    image.save(argv[2])
    


def experiment():
    file = argv[1]
    image = argv[2]
    

    X, Y, Elements = readPixels(file)
    
    
    setE = []   
    for elem in Elements:
        if elem not in setE:
            setE.append(elem)
    
    
   
   
    npE = np.array(Elements)

    for i in range(1,13):
        N = 2**i

        sample = random.sample(setE,N)
        nps = np.array(sample)
        npem3 = np.array([[0,0,0] for i in range(N)])
        npem1 = np.array([0 for i in range(N)])


        codeBook = LBG(npE, N, nps, npem3, npem1)
    
    

        tgaData = [[] for i in range(Y)]

        mse = 0
        SNR = 0

        for y in range(Y):
            for x in range(X):
                v = Elements[y*X+x]
                c = quantizeVector(v,codeBook)
                tgaData[y].append((c[0],c[1],c[2]))

                mse += d(v,c) ** 2
                SNR += (v[0]+v[1]+v[2]) ** 2
        
        SNR /= mse
        mse /= Y*X
    
        print("n:",i)
        print("Błąd średniokwadratowy:",mse)
        print("Stosunek sygnału do szumu:",SNR)
        print("")

        image = pyTGA.Image(data=tgaData)
        
        image.save(argv[2]+str(i))


# experiment()

quantize()