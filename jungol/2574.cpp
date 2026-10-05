#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

vector<vector<int>> gr(1000001);
ll dp[1000001][2];

void dfs(int node,int parent){
    ll d0=0,d1=0;
    for(int next:gr[node]){
        if(next == parent) continue;

        dfs(next,node);
        d0+=min(dp[next][0],dp[next][1]);
        d1+=dp[next][0];
    }

    dp[node][0] = d0+1;
    dp[node][1] = d1;
    //cout<<node<<' '<<dp[node][0]<<' '<<dp[node][1]<<'\n';
}

void solve() {
    int n;
    cin>>n;
    for (int i = 0; i < n-1; i++) {
        int u,v;
        cin>>u>>v;
        gr[u].push_back(v);
        gr[v].push_back(u);
    }

    dfs(1,0);
    cout<<min(dp[1][0],dp[1][1]);
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