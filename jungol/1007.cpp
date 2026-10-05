#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    while (1) {
        int y,m,d;
        cin>>y>>m>>d;
        if (m==2){
            if ((y%400==0 || (y%4==0 && y%100!=0))){
                if (d>29){
                    cout<<"INPUT ERROR!"<<'\n';
                    return;
                }
                
            }
            else{
                if(d>28){
                    cout<<"INPUT ERROR!"<<'\n';
                    return;
                }
            }
        }


        

    }
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