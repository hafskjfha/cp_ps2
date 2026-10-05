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
    string s;
    cin >> n >> s;
    vector<vector<int>> dp(n,vector<int>(3,-INF));

    if (s[0]=='O' || s[0]=='?'){
        dp[0][0]=1;
    }
    if (s[0]=='X' || s[0]=='?'){
        dp[0][1]=0;
    }

    for (int i=1;i<n;i++){
        if (s[i]=='O' || s[i]=='?'){
            dp[i][0] = max(dp[i-1][1],dp[i-1][2])+1;
        }
        if (s[i]=='X' || s[i]=='?'){
            dp[i][1]=dp[i-1][0];
            dp[i][2]=dp[i-1][1];
        }
    }

    int ans=max(dp[n-1][0],max(dp[n-1][1],dp[n-1][2]));
    cout << (ans >=0 ? ans : -1);


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