#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;


ll top_down(vector<ll> &dp,int k,int x){
    if (dp[x]!=LINF) return dp[x];

    if (x<=k){
        dp[x]=0;
        return dp[x];
    }

    int temp=x;
    if (temp%2==0){
        dp[x]=min(dp[x],1+2*top_down(dp, k, x/2));
        while (temp%2==0) {
            temp/=2;
        }
    }

    for (int i = 3; i*i <= x; i+=2) {
        if (temp%i==0){
            dp[x]=min(dp[x],1+i*top_down(dp, k, x/i));
            while (temp % i == 0) {
                temp/=i;
            }
        }
    }

    if (temp>1){
        dp[x]=min(dp[x],1+temp*top_down(dp, k, x/temp));
    }
    
    return dp[x];
}

void solve() {
    int n,k;
    cin>>n>>k;
    vector<ll> dp(n+1,LINF);
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    ll ans=0;
    for(int x:v){
        ans+=top_down(dp, k, x);
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