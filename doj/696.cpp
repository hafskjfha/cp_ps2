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
    vector<vector<int>> dp(n+1,vector<int>(m+1));
    dp[0][0]=1;

    for(int i=1;i<=n;i++){
        for (int j = 1; j <= m; j++) {
            dp[i][j]=dp[i-1][j-1];
            dp[i][0]+=dp[i][j];
        }
    }

    for(auto& vv:dp){
        for(int x:vv){
            cout<<x<<' ';
        }
        cout<<'\n';
    }
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