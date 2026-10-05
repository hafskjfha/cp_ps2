#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

const ll MOD = 998244353;

void solve() {
    ll a=0, b=0, c=0;
    string s;
    cin >> s;

    for (auto& x: s){
        if (x=='a') a=(a+b+c+1)%MOD;
        else if (x=='b') b=(a+b+c+1)%MOD;
        else c=(a+b+c+1)%MOD;
    }

    cout << (a+b+c)%MOD;

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