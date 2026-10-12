#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

int n, centroid=-1;
vector<vector<int>> gr(200000);
vector<pii> edge(200000);
vector<int> nodeCount(200000);
vector<ll> ans, dp;

void countDp(int u,int p){
    nodeCount[u]=1;

    for(int v:gr[u]){
        if (v==p) continue;
        countDp(v,u);
        nodeCount[u]+=nodeCount[v];
        //cout<<u<<' '<<v<<' '<<nodeCount[u]<<'\n';
    }

    bool flg=(n - nodeCount[u] <= n / 2);
    for(int v:gr[u]){
        if (v == p) continue;

        if (nodeCount[v]>n/2){
            flg=false;
            break;
        }
    }
    if(flg) centroid=u;
}

void ansDp(int u,int p){
    for(int v:gr[u]){
        if(v==p) continue;
        dp[v]+=dp[u];
        ansDp(v,u);
    }
}

void solve() {
    cin>>n;
    for (int i = 1; i < n; i++) {
        int u,v;
        cin>>u>>v;
        gr[u].push_back(v);
        gr[v].push_back(u);
        edge[i]={u,v};
    }

    countDp(1,0);
    countDp(centroid,0);

    dp.assign(n+1,0);
    for (int i = 1; i < n; i++) {
        auto [u,v]=edge[i];
        if(nodeCount[u]<nodeCount[v]) swap(u,v);
        dp[v]+=i;
        
    }

    ansDp(centroid,0);
    
    for (int i = 1; i <= n; i++) {
        cout<<1LL*(n-1)/2*n-dp[i]<<' ';
    }
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