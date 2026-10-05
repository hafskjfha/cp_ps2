#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,k;
    cin>>n>>k;
    vector<pii> v(n);
    for (int i = 1; i <= n; i++) {
        int temp;
        cin>>temp;
        v[i-1]={temp,i};
    }

    sort(all(v));
    vector<vector<int>> ans(k);
    int idx=0;
    for(auto [x,i]:v){
        ans[idx].push_back(i);
        idx=(idx+1)%k;
    }

    for(auto& vv:ans){
        for(int i:vv){
            cout<<i<<' ';
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