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
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }
    vector<pii> ans;
    for (int i = 0; i < n; i++) {
        int j=i;
        for(j=i;j<n;j++){
            if(v[j]==i+1) break;
        }
        for(int k=j;k>i;k--){
            ans.push_back({k-1,k});
            int temp=v[k-1];
            v[k-1]=v[k];
            v[k]=temp;
        }
    }
    cout<<ans.size()<<'\n';
    for(auto [i,j]:ans){
        cout<<i+1<<' '<<j+1<<'\n';
    }
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