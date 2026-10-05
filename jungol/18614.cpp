#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

int n,node=0;
vector<vector<int>> gr(1000000);
vector<ll> value(1000000);

void make(int p,int node){
    ll v,c;
    cin>>v>>c;
    value[node]=v;
    if(p!=node){
        gr[p].push_back(node);
    }
}

void solve() {
    cin>>n;

    make(0,0);
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