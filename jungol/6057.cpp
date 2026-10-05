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
    int p,n,cmd,pi,mi;
    cin >> p >> n;

    int ans=0;
    vector<queue<int>> v(p+1);

    for (int i = 0; i < n; i++) {
        cin >> cmd >> pi;
        if (cmd){
            if (!v[pi].empty()){
                ans+=v[pi].front();
                v[pi].pop();
            }
        }
        else{
            cin >> mi;
            v[pi].push(mi);
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