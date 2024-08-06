#include <iostream>
#include <map>
#include <bits/stdc++.h>
#include <filesystem>
#include <fstream>

using namespace std;

map<string,int> dictionary;
uint biggestStringSize = 1;
string buffer = "";
uint n = 1;

u_char currentMessage = 0;
int bitsSent = 0;
ulong totalBytesSent = 0;

void send(bool bit){
    currentMessage = (currentMessage<<1) + bit;
    bitsSent++;

    if(bitsSent == 8){
        write(1,&currentMessage,1);
        currentMessage = 0;
        bitsSent = 0;
        totalBytesSent++;
    }
}

void gammaCode(ulong byte){
    stack<bool> bits;
    while(byte>0){
        bits.push(byte%2);
        byte >>= 1;
    }
    for(int i=0; i<bits.size() - 1;i++)
        send(0);
    while(!bits.empty()){
        send(bits.top());
        bits.pop();
    }
}

void deltaCode(ulong n){
    stack<bool> bits;
    while(n>0){
        bits.push(n%2);
        n >>= 1;
    }
    bits.pop(); //usuwamy pierwszą jednkę
    n = bits.size() + 1;
    int k = 0;
    while(n>0){
        bits.push(n%2);
        n >>= 1;
        k++;
    }
    for(int i=0; i<k - 1;i++)
        send(0);
    while(!bits.empty()){
        send(bits.top());
        bits.pop();
    }
}

void omegaCode(ulong n){
    stack<bool> bits;
    bits.push(0);
    
    while(n > 1){
        int k = 0;
        while(n>0){
            bits.push(n%2);
            n >>= 1;
            k++;
        }
        n = k-1;
    }
    while(!bits.empty()){
        send(bits.top());
        bits.pop();
    }
}

vector<ulong> fibb = {1,2};

void fibbCode(ulong n){
    stack<bool> bits;
    bits.push(1);
    
    int biggestFibb = 0;
    
    int i = 0;
    while(n >= fibb[i]){
        if(i == fibb.size()-1)
            fibb.push_back(fibb[i-1] + fibb[i]);
        
        i++;
    }

    i--;
    
    for(int j = i; j >= 0; j--){
        if( n >= fibb[j]){
            n -= fibb[j];
            bits.push(1);
        }else{
            bits.push(0);
        }
    }
    
    while(!bits.empty()){
        send(bits.top());
        bits.pop();
    }
}

ulong encode(bool addToDictionary){
    // cout<<" - "<<buffer.size()<<endl;
    int chars = buffer.size() + 1;
    int code = 0;
    while(chars > 0 && code == 0){
        chars--;
        string match = buffer.substr(0, chars);
        code = dictionary[match];
    }
    if(addToDictionary){
        dictionary[buffer.substr(0, chars+1)] = n++;
        if(chars+2 > biggestStringSize) biggestStringSize = chars+2;
    }
    buffer = buffer.substr(chars,buffer.size()-chars);
    return code;    

}

int main(int argc, char** argv){
    FILE *f = freopen(argv[1], "rb", stdin);

    uint size = std::filesystem::file_size(argv[1]);
    
    // słownik początkowy
    for(int c=0; c<256;c++){
        dictionary[string(1,(char)c)] = n++;
    }

    for(uint i=0; i<size; i++){
        buffer += getchar();
        if(buffer.size() < biggestStringSize+1)
            continue;
        ulong code = encode(true);
        
        if(argc < 3)
            omegaCode(code);
        else
        switch(argv[2][0]){
            case 'g':
                gammaCode(code);
                break;
            case 'd':
                deltaCode(code);
                break;
            case 'f':
                fibbCode(code);
                break;
            case 'o':
            default:
                omegaCode(code);
                break;
        }
    }
    // cout<<"B: "<<buffer<<endl;
    // pozostałe litery
    while(buffer.size()>0){
        ulong code = encode(false);

        if(argc < 3)
            omegaCode(code);
        else
        switch(argv[2][0]){
            case 'g':
                gammaCode(code);
                break;
            case 'd':
                deltaCode(code);
                break;
            case 'f':
                fibbCode(code);
                break;
            case 'o':
            default:
                omegaCode(code);
                break;
        }
    }
    // dobijamy do bajta
    for(int i=0; i<8; i++)
        if(argc < 3 || argv[2][0] == 'o')
            send(1);
        else
            send(0);

    // rozmiar pliku
    // cout<<size<<endl;
    // gammaCode(size);
    
    
    // jakoś zakończyć przekaz
}


/*int main(int argc, char** argv){
    FILE *f = freopen(argv[1], "rb", stdin);

    uint size = std::filesystem::file_size(argv[1]);
    
    // słownik początkowy
    for(int c=0; c<255;c++){
        dictionary[string(1,(char)c)] = n++;
    }

    // rozmiar pliku
    // cout<<size<<endl;
    // gammaCode(size);
    switch(argv[2][0]){
        case 'g':
            for(uint i=0; i<size; i++){
                buffer += getchar();
                if(buffer.size() < biggestStringSize+1)
                    continue;
                ulong code = encode(true);
                gammaCode(code);
            }
            // pozostałe litery
            while(buffer.size()>0)
                encode(false);
            // dobijamy do bajta
            for(int i=0; i<8; i++)
                send(0);
            break;
        case 'd':
            for(uint i=0; i<size; i++){
                buffer += getchar();
                if(buffer.size() < biggestStringSize+1)
                    continue;
                ulong code = encode(true);
                deltaCode(code);
            }
            // pozostałe litery
            while(buffer.size()>0)
                encode(false);
            // dobijamy do bajta
            for(int i=0; i<8; i++)
                send(0);
            break;
        case 'f':
            for(uint i=0; i<size; i++){
                buffer += getchar();
                if(buffer.size() < biggestStringSize+1)
                    continue;
                ulong code = encode(true);
                fibbCode(code);
            }
            // pozostałe litery
            while(buffer.size()>0)
                encode(false);
            // dobijamy do bajta
            for(int i=0; i<8; i++)
                send(0);
            break;
        case 'o':
        default:
            for(uint i=0; i<size; i++){
                buffer += getchar();
                if(buffer.size() < biggestStringSize+1)
                    continue;
                ulong code = encode(true);
                omegaCode(code);
            }
            // pozostałe litery
            while(buffer.size()>0)
                encode(false);
            // dobijamy do bajta
            for(int i=0; i<8; i++)
                send(1);
            break;
        
    }
    
    // jakoś zakończyć przekaz
}
*/