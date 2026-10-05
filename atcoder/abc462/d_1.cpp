#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

constexpr int maxt = 1000001;

int imos[maxt];

void solve() {
    int n,d,s,t;
    cin >> n >> d;
    
    for (int i = 0; i < n; i++) {
        cin >> s >> t;
        if (t-s<d) continue;
        imos[s]++;
        imos[t-d+1]--;
    }

    ll ans=0,cur=0;
    for (int i=0;i<maxt;i++){
        cur += imos[i];
        ans += cur*(cur-1)/2;
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