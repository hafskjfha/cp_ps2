#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int r,c,sr,sc,n;
    cin>>r>>c>>sr>>sc>>n;

    int mu,mb,ml,mr;
    cin>>mu>>ml;
    mb=mu;mr=ml;
    for (int i = 0; i < n-1; i++) {
        int ir,ic;
        cin>>ir>>ic;
        mu=min(mu,ir);
        mb=max(mb,ir);
        ml=min(ml,ic);
        mr=max(mr,ic);

    }

    ll ans;
    if(sr<mu){
        ans=mb-sr;
    }
    else if (sr>mb){
        ans=sr-mu;
    }
    else{
        ans=mb-mu;
    }

    if(sc<ml){
        ans+=mr-sc;
    }
    else if(sc>mr){
        ans+=sc-ml;
    }
    else{
        
        ans+=2LL*min(sc-ml,mr-sc)+max(sc-ml,mr-sc);
    }
    //cout<<sc-ml<<' '<<mr-sc<<'\n';

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