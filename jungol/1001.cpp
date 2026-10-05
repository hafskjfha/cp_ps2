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
    int a,b;
    while (1) {
        cin >> a >> b;
        if (a==0 && b==0) return;
        if (a < 0 || a > 1000 || b < 0 || b > 4000){
            cout << "INPUT ERROR!" << '\n';
            continue;
        }

        if (b%2 == 1 || b/2-a <= 0 || 2*a - b/2 <= 0){
            cout << 0 << '\n';
            continue;
        }

        cout << b/2-a << ' ' << 2*a - b/2 << '\n';

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