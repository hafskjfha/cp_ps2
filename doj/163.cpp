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
    int n,m=0;
    ll temp;
    cin >> n;
    unordered_map<ll, int> counter;
    for (int i = 0; i < n; i++) {
        cin >> temp;
        counter[temp]++;
    }

    for (auto &[key,v]: counter){
        m=max(m,v);
    }

    cout << max(0,2*m-n);

    


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