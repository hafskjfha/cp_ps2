#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,p,q;
    cin>>n>>p>>q;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }
    int pcount=0,qcount=0;
    for (int i = 0; i < n; i++) {
        int temp;
        cin>>temp;
        if(temp==p) pcount++;
        else qcount++;
    }

    ll ans=0;

    priority_queue<pii,vector<pii>,greater<pii>> pq;
    

    cout<<ans;
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