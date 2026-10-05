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
    ll l;
    cin>>n>>l;
    vector<ll> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    ll ans=0;
    ll left=1,high=l;
    while (left<=high) {
        ll mid = left + (high-left)/2;

        ll sum=0;
        for(ll x:v){
            sum+=min(x,mid);
        }

        if (sum==l){
            ans=mid;
            high=mid-1;
        }
        else if (sum>l){
            high=mid-1;
        }
        else{
            left=mid+1;
        }
    }

    cout<<ans<<'\n';
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