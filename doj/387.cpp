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
    int a,g;
    cin>>a>>g;
    cout << (a==g ? "He is a real alpaca" : abs(g-a)<=3 ? "He is similar alpaca" : "He is a fake alpaca") << '\n';
}

int main() {
    fastio;

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}