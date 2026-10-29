#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

#define safe_mod(x,mod) ((x%mod)+mod)%mod

void solve() {
    int n;
    cin>>n;
    vector<ll> dp1(50,-1);
    dp1[0]=0;

    for (int i = 0; i < n; i++) {
        vector<ll> dp2 = dp1;
        ll x;
        cin>>x;
        if(x>=20000 || x<=500) continue;
        x-=500;
        ll w=safe_mod(x,500)/10;
        for (int j = 0; j<50;j++) {
            if (dp1[safe_mod(j-w, 50)]!=-1){
                dp2[j]=max(dp1[j],dp1[safe_mod(j-w, 50)]+x);
            }
        }
        dp1.swap(dp2);
        
    }

    cout<<dp1[0];
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