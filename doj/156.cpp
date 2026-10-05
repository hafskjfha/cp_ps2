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

    vector<int> prefix_sum(n+1);
    for (int i = 0; i < n; i++) {
        prefix_sum[i+1]=prefix_sum[i]+(s[i] == 'R');
    }
    
    int ans=min(prefix_sum[n],n-prefix_sum[n]);

    for (int i = 0; i < n; i++) {
        ans=min(
            min(
                ans, 
                i+1-prefix_sum[i+1]+prefix_sum[n]-prefix_sum[i+1]
            ),
            2*prefix_sum[i+1]+n-i-1-prefix_sum[n]
        );
    }

    cout << ans;
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