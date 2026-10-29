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
    int n,t;
    cin>>n>>t;
    
    vector<ll> dp(t+1,-LINF);
    dp[0]=0;
    for (int i = 0; i < n; i++) {
        ll w1,v1,w2,v2;
        cin>>w1>>v1>>w2>>v2;
        for (int j = t; j >= min(w1,w2); j--) {
            ll temp=-LINF;
            if (j-w1>=0 && dp[j-w1]!=-LINF) temp=max(temp,dp[j-w1]+v1);
            if (j-w2>=0 && dp[j-w2]!=-LINF) temp=max(temp,dp[j-w2]+v2);
            dp[j]=temp;
        }

        for (int j = 0; j < min(w1,w2); j++) {
            dp[j]=-LINF;
        }
    }
    cout<<*max_element(all(dp));
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