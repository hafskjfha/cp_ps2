#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,m,k;
    cin>>n>>m>>k;
    vector<pii> v(k);
    for (int i = 0; i < k; i++) {
        int d,x;
        cin>>d>>x;
        v.push_back({d,x});
    }
    int a,b;
    cin>>a>>b;

    ll ans=0;
    for(auto&[d,x]:v){
        if(d==1){
            if(a==1){
                int temp=abs(x-b);
                if(x<b) temp=min(temp,2*m+n+x);
                else temp=min(temp,2*m+n+m-x);
            }
        }
        else if(d==2){

        }
    }

    cout<<ans;
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