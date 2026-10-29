#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,m;
    cin>>n>>m;
    vector<ll> dp(m+1);
    for (int i = 0; i < n; i++) {
        ll w,c,k;
        cin>>w>>c>>k;
        for(ll l=1;k>0;l<<=1){
            ll t=min(k,l);
            k-=t;

            ll tw=w*t;
            ll tc=c*t;
            for (int j = m; j >= tw; j--) {
                dp[j]=max(dp[j],dp[j-tw]+tc);
            }
        }
    }

    // for (int i = 0; i < m; i++) {
    //     cout<<dp[i]<<' ';
    // }
    cout<<dp[m];
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