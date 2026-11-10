#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int m;
    cin>>m;
    if(m<100){
        cout<<"00"<<endl;
    }
    else if(m<=5000){
        if(m<1000){
            cout<<"0"<<m/100<<endl;
        }
        else{
            cout<<m/100<<endl;
        }
    }
    else if(m<=30000){
        cout<<m/1000+50<<endl;
    }
    else if(m<=70000){
        cout<<(m/1000-30)/5+80<<endl;
    }
    else{
        cout<<89<<endl;
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