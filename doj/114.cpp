#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n;
    cin>>n;
    vector<pair<string,int>> v(n);
    vector<int> ans(n);
    for (int i = 0; i < n; i++) {
        int p;
        cin>>v[i].first>>p;
        v[i].second=p;
        ans[i]=p;
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if(i==j) continue;

            if(v[i].first.substr(0,v[j].first.size())==v[j].first){
                ans[i]+=v[j].second;
            }
        }
    }

    cout<<*max_element(all(ans));
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