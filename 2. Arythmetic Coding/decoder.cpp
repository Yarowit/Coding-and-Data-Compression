#include <bits/stdc++.h>
int errCount = 0;

using namespace std;

ulong umax;
ulong L,R;
using ui = __uint128_t;

int Ranges[257];
const ulong sumRanges = 512;
ulong counter = 0;

ulong step;

int Encounters[256];
void resizeRanges(){
    Ranges[0] = 0;
    
    for(int i=1; i<=256;i++){
        Ranges[i] = Ranges[i-1] + 1 + Encounters[i-1];
        Encounters[i-1] = 0;
    }

}

int lRange=0;
int rRange = 257;

int isInRange(ulong l, ulong r){
    ui d = (ui)R-L+1;
    //zawęź range
    //lewo
    while(L+(ui)Ranges[lRange+1]*d/sumRanges <= l)
        lRange++;
    //prawo
    while(r < L+(ui)Ranges[rRange-1]*d/sumRanges)
        rRange--;
    
    if(lRange + 1 == rRange){
        int i = lRange;
        lRange = 0; rRange = 257;
        return i;
    }

    // for(int i=0; i< 256; i++){
    //     if(L+(ui)Ranges[i]*d/sumRanges <= l && r < L+(ui)Ranges[i+1]*d/sumRanges){
    //         lRange = 0; rRange = 257;
    //         return i;
    //     }
    // }
    
    return 300;
}

ulong totalBytesDecoded = 0;
u_char deducedByte = 0;
u_char deduceByte(uint stream,ulong l, ulong r){
    l = 0;
    r = umax;
    if(totalBytesDecoded > 395){
        int ll;
        ll=0;
    }
    while(true){
        if(l==r){
            int s;
            s=3;
        }
        ulong d = (r-l)/2 + 1;
        
        bool bit = stream>>31;
        stream = stream<<1;

        if(bit){ // == 1
            l = l+d;
        }else{
            r = l+d -1;
        }
            int code = isInRange(l,r);
        if(code < 256){
            // deducedByte = code;

            u_char s = code;
            return s;
        }
    }
}



uint bitstream = 0;

int totalBytesRead = -4;
int bitsRead = 7;
u_char currentByte = 0;
bool getNextBit(){
    bitsRead++;
    if(bitsRead == 8){
        currentByte = getchar();
        totalBytesRead++;
        bitsRead = 0;
    }
    
    bool bit = currentByte>>7;
    currentByte<<=1;
    return bit;
}

void code(uint byte){
    if(byte==101)
        int k=0;
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

            bitstream <<= 1;
            bitstream += getNextBit();

        }else if(l >= half ){
            l <<= 1;
            r = (r<<1) + 1;

            bitstream <<= 1;
            bitstream += getNextBit();

        }else if(l >= (half>>1) && r < half + (half>>1)){
            l = (l<<1) - (half);
            r = (r<<1) - (half) + 1;
            // counter++;
            // ZJADAM Z INPUTU I BITFLIP

            bitstream <<= 1;
            bitstream ^= (1<<31);
            bitstream += getNextBit();
        } else break;
    }

    R = r;
    L = l;
}



int main(int argc, char **argv) {
    umax = std::numeric_limits<ulong>::max();
    L = 0; R = umax;
    ulong n = 0;

    step = umax/sumRanges + 1;

    // for(int i=0;i<257;i++){
    //     Ranges[i] = 2*i;
    // }
    for(int i=0;i<256;i++){
        Encounters[i]=1;
    }
    resizeRanges();
    // FILE *f = freopen("temp", "rb", stdin);

    uint size;
    cin>>size;

    
    getchar();
    u_char g;

    for(int i=0;i<32;i++){
        bool bit = getNextBit();
        bitstream = (bitstream<<1) + bit;
    }


    while(totalBytesDecoded < size){
        g = deduceByte(bitstream,L,R);
        write(1,&g,1);
        code(g);

        // cout<<(char)g<<" -- "<<g<<endl;
        // cout<<g;
    }
    return 0;
}

