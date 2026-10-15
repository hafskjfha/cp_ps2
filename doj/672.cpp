#include <iostream>
#include <algorithm>

using namespace std;
using ll = long long;
using pii=pair<int,int>;

#define F first
#define S second

void print(int t,int i,int j){
    cout<<t<<' '<<i<<' '<<j<<'\n';
}

int main() {
    cin.tie(NULL);
    ios_base::sync_with_stdio(false);
    
    int n;
    cin>>n;
    pii leftX,rightX,upY,downY;
    for (int i = 0;i < n;i++) {
        int x1,y1,x2,y2;
        cin>>x1>>y1>>x2>>y2;
        if (i == 0) {
            leftX={x1,1};
            rightX={x2,1};
            downY={y1,1};
            upY={y2,1};
        }
        else {
            if(upY.F < y1){
                print(2,upY.S,i+1);
                return 0;
            }
            if (downY.F > y2){
                print(2,downY.S,i+1);
                return 0;
            }
            if(rightX.F < x1){
                print(2,rightX.S,i+1);
                return 0;
            }
            if(leftX.F > x2){
                print(2,leftX.S,i+1);
                return 0;
            }
            

            if(leftX.F < x1){
                leftX={x1,i+1};
            }
            if(rightX.F > x2){
                rightX={x2,i+1};
            }
            if(downY.F < y1){
                downY={y1,i+1};
            }
            if(upY.F > y2){
                upY={y2,i+1};
            }
        }
        //cout << leftX << ' ' << rightX << ' ' << downY <<' '<< upY<< '\n';
    }

    cout << 1 << ' '<<leftX.F<< ' '<<upY.F<<'\n';
    
}