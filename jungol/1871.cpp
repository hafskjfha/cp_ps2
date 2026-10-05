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
    int n;
    cin>>n;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    vector<int> lis;
    for(int x:v){
        int idx=lower_bound(lis.begin(),lis.end(),x)-lis.begin();
        if (idx==lis.size()){
            lis.push_back(x);
        }
        else{
            lis[idx]=x;
        }
    }

    cout<<n-lis.size();
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