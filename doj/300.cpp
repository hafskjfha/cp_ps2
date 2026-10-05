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
    int n,k;
    string s;
    cin>>n>>k>>s;
    
    vector<bool> dp(n);

    dp[0]=true;
    for (int i = 1; i < n; i++) {
        if(s[i]=='#') continue;
        if(i-k>=0){
            dp[i]=dp[i-1]|dp[i-k];
        }
        else{
            dp[i]=dp[i-1];
        }
    }

    cout<<(dp[n-1]?"YES":"NO");
    
}

int main() {
    fastio;

    int T = 1;
    //cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}