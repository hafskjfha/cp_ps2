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
    ll n, temp;
    cin >> n;
    ll b=1, ansb=1, maxv=(n-1)*10+1;

    for (int i = 1; i < 10; i++) {
        b*=10;
        if (b>=n) break;
        temp=(n-b)*b*10+b;
        if (maxv < temp) {
            ansb=b; 
            maxv=temp;
        }

    }

    cout << n-ansb << ' ' << ansb;
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