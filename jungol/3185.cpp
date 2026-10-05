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
    cin>>n>>k;
    vector<ll> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    sort(all(v));

    vector<ll> prefix_sum(n+1);
    for (int i = 0; i < n; i++) {
        prefix_sum[i+1]=prefix_sum[i]+v[i];
    }
    
    ll cur=0,ans=0;
    for (int j = 0; j < k; j++) {
        ans+=(2LL*j-k+1)*v[j];
    }
    cur=ans;

    for (int i = 1; i <= n-k; i++) {
        cur = cur + (k-1LL)*v[i-1] + (k-1LL)*v[i+k-1] - 2LL*(prefix_sum[i+k-1] - prefix_sum[i]);
        ans=min(ans,cur);
    }
    

    cout<<ans;
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