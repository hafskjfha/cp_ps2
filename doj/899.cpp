#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n;
    cin>>n;
    vector<ll> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    ll ans=v[n-1]+v[0];
    for (int i = 0; i < n-1; i++) {
        ans=min(v[i]+v[i+1],ans);
    }
    cout<<max(ans,*max_element(all(v)));
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