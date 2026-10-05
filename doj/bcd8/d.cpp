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
    vector<int> a(n);
    vector<int> b(m);
    for (int i = 0; i < n; i++) {
        cin>>a[i];
    }
    for (int i = 0; i < m; i++) {
        cin>>b[i];
    }

    ll along=0,blong=0;
    ll count=0;
    for (int i = 0; i < n; i++) {
        if (a[i]==0){
            along=max(along,count);
            count=0;
        }
        else{
            count++;
        }
    }
    along=max(along,count);
    count=0;
    for (int i = 0; i < m; i++) {
        if (b[i]==0){
            blong=max(blong,count);
            count=0;
        }
        else{
            count++;
        }
    }
    blong=max(blong,count);
    count=0;
    cout<<along*blong<<'\n';
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