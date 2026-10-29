#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,w;
    cin>>n>>w;
    vector<pii> v(n+1);
    for (int i = 1; i <= n; i++) {
        cin>>v[i].first>>v[i].second;
    }

    vector<int> dp(w+1);
    for (int i = 1; i <= n; i++) {
        for(int j=v[i].first;j<=w;j++){
            dp[j]=max(dp[j],dp[j-v[i].first]+v[i].second);
        }
    }

    cout<<dp[w];
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