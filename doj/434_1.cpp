#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

vector<vector<int>> gr(500001);

int dfs(int p,int node,int depth){
    if(gr[node].size()>2) return depth;

    for(int next:gr[node]){
        if(next==p) continue;
        return dfs(node,next,depth+1);
    }

    return -1;
}

void solve() {
    int n;
    cin>>n;
    if(n==1){
        cout<<-1;
        return;
    }
    for (int i = 0; i < n-1; i++) {
        int u,v;
        cin>>u>>v;
        gr[u].push_back(v);
        gr[v].push_back(u);
    }

    for (int i = 1; i < n+1; i++) {
        if(gr[i].size()>1){
            cout<<0<<' ';
        }
        else{
            cout<<dfs(0,i,0)<<' ';
        }
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