#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

constexpr int SIZE = 1e6;
ll imos[SIZE+1], sum[SIZE+1];

void solve() {
    int n;
    cin>>n;
    
    int s,e,t;
    for (int i = 0; i < n; i++) {
        cin>>s>>e>>t;
        imos[s]+=t;
        imos[e+1]-=t;
    }

    ll cur=0;
    for (int i = 0; i < SIZE; i++) {
        cur+=imos[i];
        sum[i]=cur;
    }

    int q;
    cin>>q;
    for (int i = 0; i < q; i++) {
        cin>>t;
        cout<<sum[t]<<'\n';
    }

}

int main() {
    fastio;

    int T = 1;
    // cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}