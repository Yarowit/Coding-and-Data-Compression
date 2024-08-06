#include <iostream>
#include <map>
#include <bits/stdc++.h>
#include <filesystem>
#include <fstream>

using namespace std;

vector<string> reverseDictionary;
string buffer = "";

int bitsRead = 7;
u_char currentByte = 0;
ulong bytesRemaining;

bool getNextBit(){
    bitsRead++;
    if(bitsRead == 8){
        if((bytesRemaining--) == 0)
            exit(0);
        currentByte = getchar();
        bitsRead = 0;
    }
    
    bool bit = currentByte>>7;
    currentByte<<=1;
    return bit;
}

ulong gammaDecode(){
    bool bit = getNextBit();
    
    // warunek końca
    // if(bit) return 0;

    int len = 0;
    while(!bit){
        len++;
        bit = getNextBit();
    }
    // cout<<"$"<<len<<"$";
    ulong n = bit;
    for(int i=0;i<len;i++){
        n <<= 1;
        n += getNextBit();
    }//cout<<"$>"<<n<<"<$";
    return n;
}

ulong deltaDecode(){
    bool bit = getNextBit();
    
    // warunek końca
    // if(bit) return 0;
    
    int len = 0;
    while(!bit){
        len++;
        bit = getNextBit();
    }
    int n = bit;
    for(int i=0;i<len;i++){
        n <<= 1;
        n += getNextBit();
    }
    ulong x = 1;
    for(int i=0;i<n-1;i++){
        x <<= 1;
        x += getNextBit();
    }
    return x;
}

ulong omegaDecode(){
    ulong n = 1;
    bool bit = getNextBit();
    
    while(bit){
        ulong x = bit;
        for(int i = 0; i < n; i++){
            x <<= 1;
            x += getNextBit();
        }
        n = x;
        bit = getNextBit();
    }

    return n;
}

vector<ulong> fibb = {1,2};

ulong fibbDecode(){
    ulong n = 0;
    bool bit = getNextBit();
    bool nextBit = getNextBit();

    int i = 0;

    while(!(bit && nextBit)){
        n += bit * fibb[i++];

        if(i == fibb.size()-1)
            fibb.push_back(fibb[i-1] + fibb[i]);

        bit = nextBit;
        nextBit = getNextBit();
    }
    n += bit * fibb[i];

    return n;
}


string bufferedEntry = "";

void print(string s){
    // cout<<"["<<s<<"]";
    for(char c : s)
        putchar(c);
}

void decode(int i){
    if(i < reverseDictionary.size()){
        print(reverseDictionary[i]);
        bufferedEntry += reverseDictionary[i][0];
    }else{
        bufferedEntry += bufferedEntry[0];
        print(bufferedEntry);
    }
        /// cos

    reverseDictionary.push_back(bufferedEntry);
    bufferedEntry = reverseDictionary[i];
}

int main(int argc, char** argv){
    FILE *f = freopen(argv[1], "rb", stdin);
    bytesRemaining = std::filesystem::file_size(argv[1]);
    
    reverseDictionary.push_back("");

    // słownik początkowy
    for(int c=0; c<256;c++){
        reverseDictionary.push_back(string(1,(char)c));
    }

    ulong code;
    if(argc < 3)
        code = omegaDecode();
    else
    switch(argv[2][0]){
        case 'g':
            code = gammaDecode();
            break;
        case 'd':
            code = deltaDecode();
            break;
        case 'f':
            code = fibbDecode();
            break;
        case 'o':
        default:
            code = omegaDecode();
            break;
    }
    // cout<<"{"<<code<<"}";
    print(reverseDictionary[code]);
    bufferedEntry = reverseDictionary[code];
    while(true){
        if(argc < 3)
            code = omegaDecode();
        else
        switch(argv[2][0]){
            case 'g':
                code = gammaDecode();
                break;
            case 'd':
                code = deltaDecode();
                break;
            case 'f':
                code = fibbDecode();
                break;
            case 'o':
            default:
                code = omegaDecode();
                break;
        }
        // cout<<"{"<<code<<"}";
        decode(code);
    }
    
    
    
}