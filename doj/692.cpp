#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    string s;
    cin>>s;
    ll res=1;
    for (char c:s) {
        if (c=='I'){
            res=(res<<1)|1;
        }
        else if (c=='O'){
            res<<=1;
        }
    }
    cout<<res<<'\n';
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}