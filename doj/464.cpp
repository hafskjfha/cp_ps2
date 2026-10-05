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
    if (n%2==1){
        cout<<-1;
        return;
    }

    cout<<n/2<<' ';
    for (int i = 0; i < m-2; i++) {
        cout<<0<<' ';
    }
    cout<<n/2;
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