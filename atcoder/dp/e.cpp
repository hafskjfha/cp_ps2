#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

const int nv=500000;

vector<ll> dp(nv+1,LINF);

void solve() {
    int n,w;
    cin>>n>>w;
    dp[0]=0;
    for (int i = 0; i < n; i++) {
        ll wi,vi;
        cin>>wi>>vi;
        for (int j = nv; j >= vi; j--) {
            dp[j]=min(dp[j],dp[j-vi]+wi);
        }
    }

    ll ans=0;
    for (ll i = 0; i <= nv; i++) {        
        if(dp[i]<=w) ans=max(ans,i);
    }
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
