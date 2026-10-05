#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    ll n,m,k;
    cin>>n>>m>>k;
    vector<ll> v;
    vector<ll> le;
    ll prev=-1,temp=0;
    for (int i = 0; i < k; i++) {
        ll x;
        cin>>x;
        if(x%2==0){
            x>>=1;
            v.push_back(x);
            if (x-1!=prev) temp=x;

            le.push_back(temp);
            prev=x;
        }
    }

    // for(auto x:v){
    //     cout<<x<<' ';
    // }
    // cout<<'\n';
    // for(auto x:le){
    //     cout<<x<<' ';
    // }
    // cout<<'\n';

    if (n==1){
        for(ll x:v){
            if(x<m){
                cout<<x*2;
                return;
            }
        }
        cout<<0;
        return;
    }

    ll ans=0;

    for(int i=0;i<m-1;i++){
        auto idx=lower_bound(all(v),ans+n)-v.begin();
        if (idx==v.size()){
            ans+=n;
        }
        else{
            if (v[idx]==ans+n){
                if (le[idx]-1==ans){
                    cout<<(ans+n)*2;
                    return;
                }
                ans=le[idx]-1;
            }
            else{
                ans+=n;
            }
        }
        //cout<<idx<<' '<<ans<<'\n';
    }
    cout<<ans*2+n*2-1;

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