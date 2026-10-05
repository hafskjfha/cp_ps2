#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

int dfsCount=0;
vector<int> id, low,temp;
stack<int> st;
vector<vector<int>> graph,sccs;
vector<bool> finished;


void dfs(int cur){
    id[cur]=low[cur]=++dfsCount;
    st.push(cur);

    for(int v:graph[cur]){
        if(id[v]==0){
            dfs(v);
            low[cur]=min(low[cur],low[v]);
        }

        else if (!finished[v]){
            low[cur]=min(low[cur],id[v]);
        }
    }

    if(id[cur]==low[cur]){
        vector<int> scc;
        
        while (1) {
            int u=st.top();st.pop();

            finished[u]=true;
            scc.push_back(u);

            if(cur==u) break;
        }

        int root=*min_element(all(scc));
        temp.push_back(root);
        sccs[root]=scc;
    }
}

void solve() {
    int n,m;
    cin>>n>>m;
    graph.resize(n+1);
    id.resize(n+1);
    low.resize(n+1);
    finished.resize(n+1);
    sccs.resize(n+1);

    for (int i = 0; i < m; i++) {
        int u,v;
        cin>>u>>v;
        graph[u].push_back(v);
    }

    for (int i = 1; i <= n; i++) {
        if(id[i]==0){
            dfs(i);
        }
    }

    sort(all(temp));
    vector<int> res(n+1);
    for(int i=0;i<temp.size();i++){
        for(int x:sccs[temp[i]]){
            res[x]=i+1;
        }
    }

    for (int i = 1; i <= n; i++) {
        cout<<res[i]<<' ';
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