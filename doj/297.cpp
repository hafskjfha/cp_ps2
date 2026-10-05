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

    if(n==1){
        cout<<v[0];
        return;
    }

    sort(all(v),greater());
    cout<<v[1]<<'\n';
    while (size(v)>1) {
        int temp;
        for (int j = 0; j < 3; j++) {
            if(j==1) temp=v.back();
            cout<<v.back()<<' ';
            v.pop_back();
        }
        cout<<'\n';
        v.push_back(temp);
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