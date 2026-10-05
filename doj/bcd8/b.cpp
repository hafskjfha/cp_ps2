#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,m;
    cin>>n>>m;
    int ans=0;
    vector<bool> check(n+1);
    for (int i = 0; i < m; i++) {
        int x;
        cin>>x;
        if(check[x]) ans++;
        else{
            check[x]=true;

        }
    }
    cout<<ans<<'\n';
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