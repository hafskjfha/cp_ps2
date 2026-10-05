#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int xw,yw,x1,y1,x2,y2;
    cin>>xw>>yw>>x1>>y1>>x2>>y2;

    if(xw==x1){
        if(((yw<y1 && y1<y2) || (yw>y1 && y1>y2)) && x1!=x2){
            cout<<1;
            return;
        }
    }
    if(yw==y1){
        //cout<<(xw<x1 && x1<x2)<<(xw>x1 && x1>x2)<<'\n';
        if(((xw<x1 && x1<x2) || (xw>x1 && x1>x2)) && y1!=y2){
            cout<<1;
            return;
        }
    }
    if(xw==x2){
        if(((yw<y2 && y2<y1) || (yw>y2 && y2>y1)) && x1!=x2){
            cout<<1;
            return;
        }
    }
    if(yw==y2){
        if(((xw<x2 && x2<x1) || (xw>x2 && x2>x1)) && y1!=y2){
            cout<<1;
            return;
        }
    }
    cout<<0;
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    //cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}