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
    vector<ll> dp(n);
    dp[0]=v[0];
    for (int i = 1; i < n; i++) {
        dp[i]=max(dp[i-1]+v[i],v[i]);
    }
    cout<<*max_element(all(dp))<<'\n';
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}