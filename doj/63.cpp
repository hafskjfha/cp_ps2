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
    ll a,b,temp,ans=0;
    cin >> a >> b;
    if (a<b) swap(a,b);

    while (b) {
        ans+=(a/b)*b;
        temp=a%b;
        a=b;
        b=temp;
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