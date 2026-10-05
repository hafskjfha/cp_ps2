#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,m,k,s;
    cin>>n>>m>>k>>s;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            int x=i%k,y=j%k;
            if(x+y*k<s) cout<<1;
            else cout<<0;
        }
        cout<<'\n';
    }
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    //cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}