#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,p,q;
    cin >> n >> p >> q;
    vector<ll> v(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i];
    }

    ll minv=v[0],s=0;
    for (int i = 1; i < n; i++) { minv = min(minv, v[i]); }
    for (int i = 0; i < n; i++) {
        v[i]-=minv;
        s+=(1 << v[i]);
    }

    sort(all(v),greater<ll>());
    int i=0;
    ll k=0;
    for (;i<n;i++){
        k+=(1 << v[i]);
        if (k*q >= s*p){break;}
    }

    cout << i+1;


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