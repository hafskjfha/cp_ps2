#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

const ll MOD = 1000000007;

vector<int> v;
ll ans=0;
int n,k;

void dfs(vector<int>& res,int e,int depth){
    // for(int x:res)cout<<x<<' ';
    
    // cout<<'\n'<<e<<' '<<depth<<'\n';
    if (e<0) return;

    if(depth==n){
        ans=(ans+1)%MOD;
        return;
    }
    for(int d=max(0,res[depth-1]-k);d<=res[depth-1]+k;d++){
        res[depth]=d;
        dfs(res,e-abs(v[depth]-d),depth+1);
    }
}

void solve() {
    int e;
    cin>>n>>k>>e;
    v.resize(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    vector<int> res(n);
    res[0]=0;
    dfs(res,e-v[0],1);
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