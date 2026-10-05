#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    ll n,a,b,x,y;
    cin>>n>>a>>b>>x>>y;

    if ((x+y)*b>=a*x){
        cout<<a*min(x,n)+b*max(0LL,n-x)<<'\n';
    }
    else{
        ll ans=0;
        ans+=a*min(x,n);
        //cout<<a*min(x,n)<<' ';
        n=max(0LL,n-x);
        ans+=a*x*(n/(x+y));
        n=n%(x+y);
        //cout<<n<<' ';
        ans+=max(b*n,a*(n-y));

        cout<<ans<<'\n';
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