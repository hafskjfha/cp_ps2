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
    int n;
    cin>>n;
    vector<int> v(n+1);
    for (int i = 1; i <= n; i++) {
        cin>>v[i];
    }

    vector<int> dp(n+1);

    for (int i = 1; i <= n; i++) {
        int x=v[i], k=0;
        for (int j = i-1; j > 0; j--) {
            if(x>v[j]){
                k=max(k,dp[j]);
            }
        }
        dp[i]=k+1;
    }

    // dp[i] = max(dp[i-1],dp[i-2],...)+1; 

    cout<<n-*max_element(dp.begin(),dp.end());

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