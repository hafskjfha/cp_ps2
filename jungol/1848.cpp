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
    int n,m;
    cin>>n>>m;
    vector<bool> v(n+1);
    for (int i = 0; i < m; i++) {
        int j;
        cin>>j;
        v[j]=true;
    }

    int dp[41]={1,1,};
    for (int i = 2; i <= n; i++) {
        if (v[i] || v[i-1]){
            dp[i]=dp[i-1];
        }
        else{
            dp[i]=dp[i-1]+dp[i-2];
        }
    }

    cout<<dp[n];
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

// 123일때 4을 배치하는가?
// 1234처럼 3뒤에 4
// 1243처럼 12뒤에 43를 붙이는 형식
// dp[i] = dp[i-1] + dp[i-2] 