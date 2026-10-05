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
    vector<int> v(n);

    v[0]=0;
    for (int i=1;i<n;i++){
        v[i]= (i%2 ? -1 : 1) * ((i+1)/2);
    }

    for (int i = 0; i < n; i++) {
        cout << v[i] << ' ';
    }
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