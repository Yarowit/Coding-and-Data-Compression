#include <bits/stdc++.h>

using namespace std;

ulong umax;
ulong L,R;
using ui = __uint128_t;


u_char currentMessage = 0;
int bitsSent = 0;
ulong totalBytesSent = 0;

// Początek przedziału literki i
int Ranges[257]; // Suma to 256*2
const ulong sumRanges = 512;
ulong counter = 0;

int Encounters[256];
void resizeRanges(){
    Ranges[0] = 0;
    
    for(int i=1; i<=256;i++){
        Ranges[i] = Ranges[i-1] + 1 + Encounters[i-1];
        Encounters[i-1] = 0;
    }
}


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

ulong totalBytesDecoded = 0;
void code(uint byte){
    if(byte == 0){
        int kk;
        kk = 3;
    }
    ui d = (ui)R - L + 1; // bo granica to 2^k -1
    
    ulong l = L + d * (ui)Ranges[byte] / sumRanges;
    ulong r = (ulong)(L + d * (ui)Ranges[byte+1] / sumRanges) - 1;
    
    Encounters[byte]++;
    totalBytesDecoded++;
    if(totalBytesDecoded % 256 == 0)
        resizeRanges();
    
    const ulong half = umax/2 + 1;

    while(true){
        if( r < half){
            l <<= 1;
            r = (r<<1) + 1;

            send(0);
            for(int i=0;i<counter;i++)
                send(1);

            counter = 0;

        }else if(l >= half ){
            l <<= 1;
            r = (r<<1) + 1;

            send(1);
            for(int i=0;i<counter;i++)
                send(0);
                
            counter = 0;

        }else if(l >= (half>>1) && r < half + (half>>1)){
            l = (l<<1) - (half);
            r = (r<<1) - (half) + 1;
            counter++;
        } else break;
    }

    R = r;
    L = l;
}


int main(int argc, char **argv) {
    
    umax = std::numeric_limits<ulong>::max();
    L = 0;
    R = umax;

    for(int i=0;i<256;i++){
        Encounters[i] = 1;
    }
    resizeRanges();

    // // DO DEBUGGERA
    // FILE *f = freopen("test23.bin", "rb", stdin);

    // uint size = std::filesystem::file_size("test23.bin");


    FILE *f = freopen(argv[1], "rb", stdin);

    uint size = std::filesystem::file_size(argv[1]);
    
    // rozmiar pliku
    cout<<size<<endl;

    for(uint i=0; i<size; i++){
        uint byte = getchar();
        
        if(byte == 153){
            int f;
        }
        // cout<<byte<<" "<<bitsSent<<endl;
        code(byte);
    }
    // czy wysłaliśmy wystarczająco bitów?
    // dobić do bajta ( końcowe po counterze na pewno muszą się dodać)
    counter = (counter/8 + 1)*8;
    // counter = max(counter,8);

    if(L < (umax/2 + 1)/2){
        send(0);
        for(int i=0;i<counter;i++)
            send(1);
    }else{
        send(1);
        for(int i=0;i<counter;i++)
            send(0);
    }
    
    return 0;
}