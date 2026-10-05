#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

int vi[2][501], vcount[501];

void dfs(vector<vector<int>> &gr,int x,bool isr,int cur){
    vi[isr][cur]=x;
    vcount[x]++;

    for(auto& dx:gr[cur]){
        if(vi[isr][dx]!=x){
            dfs(gr,x,isr,dx);
        }
    }
}

void solve() {
    int n,m;
    cin>>n>>m;

    vector<vector<int>> gr(n+1);
    vector<vector<int>> rev_gr(n+1);
    
    int a,b;
    for (int j = 0; j < m; j++) {
        cin>>a>>b;
        gr[a].push_back(b);
        rev_gr[b].push_back(a);
    }

    int ans=0;
    for (int i = 1; i <= n; i++) {
        dfs(gr,i,false,i);
        dfs(rev_gr,i,true,i);
        if(vcount[i]==n+1) ans++;
    }

    cout<<ans;

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