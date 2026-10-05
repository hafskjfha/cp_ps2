#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    ll n,a,b;
    cin>>n>>a>>b;
    if((a|b)!=b){
        cout<<-1;
        return;
    }
    if (a==b){
        cout<<0;
        return;
    }
    
    vector<ll> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    int count=0;
    vector<int> res;

    for (int i = 0; i < n; i++) {
        if((v[i]|b)==b && (a|v[i])!=a){
            a|=v[i];
            count++;
            res.push_back(i+1);
            if(a==b) break;
        }
    }

    if(a==b && count<=100){
        cout<<count<<'\n';
        for(int i:res){
            cout<<i<<' ';
        }
    }
    else{
        cout<<-1;
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