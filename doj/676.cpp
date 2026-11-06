#include <bits/stdc++.h>
using namespace std;

const int dx[4]={1,-1,0,0};
const int dy[4]={0,0,1,-1};

int check(vector<string> ss,int n) {
    int count=0;

    for (int i = 0;i < 2;i++) {
        for (int j = 0;j < n;j++) {
            if (ss[i][j] == 'S') {
                for (int k = 0;k < 4;k++) {
                    int x=i+dx[k],y=j+dy[k];
                    if (0 <= x && x < 2 && 0 <= y && y < n && ss[x][y]=='K') {
                        for (int l = 0;l < 4;l++) {
                            int x2=x+dx[l],y2=y+dy[l];
                            if (0 <= x2 && x2 < 2 && 0 <= y2 && y2 < n && ss[x2][y2] == 'H') {
                                count++;
                            }
                        }
                    }
                }
            }
        }
    }

    return count;
}

int main() {
    int n;
    cin>>n;
    
    vector<string> ss(2);

    for (int i = 0; i < 2; i++) {
        int c=0;
        for (int j = 0; j < n; j++) {
            if(i==0){
                if(j%2==1 && c<n/3){
                    //cout<<c<<' '<<n/3<<'\n';
                    cout<<'K';
                    ss[i].push_back('K');
                    c++;
                    
                }
                else{
                    cout<<'S';
                    ss[i].push_back('S');
                }
            }
            else{
                if(j%2==0 && j>0 && c<n/3){
                    cout<<'K';
                    ss[i].push_back('K');
                    c++;
                }
                else{
                    cout<<'H';
                    ss[i].push_back('H');
                }
            }
        }
        cout<<'\n';
    }


    //cout<<check(ss,ss[0].size())<<' '<<4*n/3;
}