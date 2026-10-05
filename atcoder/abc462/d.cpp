#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

constexpr int M = 1000001;

int imos[M];

void solve() {
    int n,d,s,t;
    ll ans=0, cur=0;
    cin >> n >> d;
    vector<pii> v(n);

    for (int i = 0; i < n; i++) {
        cin >> s >> t;
        if (d > t-s) continue;
        imos[s]++;
        imos[t-d+1]--;
    }

    for (int i = 1; i < M; i++) {
        cur += imos[i];
        ans += (cur-1) * cur / 2;
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