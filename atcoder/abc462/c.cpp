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
    cin >> n;
    vector<pii> v(n);

    for (int i = 0; i < n; i++) {
        pii temp;
        cin >> temp.first >> temp.second;
        v[i] = temp;
    }

    sort(all(v));

    int miny=INF, ans=0;
    for (auto& [x,y]: v){
        if (y < miny){
            ans++;
            miny=y;
        }
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