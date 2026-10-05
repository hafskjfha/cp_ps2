#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

vector<vector<int>> gr, rgr,sccs;
stack<int> st;
vector<bool> vi;

void dfs1(int x){
    vi[x]=true;

    for(int u:gr[x]){
        if (!vi[u]){
            dfs1(u);
        }
    }

    st.push(x);
}

void dfs2(int x,vector<int>& scc){
    vi[x]=true;
    scc.push_back(x);

    for(int u:rgr[x]){
        if (!vi[u]){
            dfs2(u,scc);
        }
    }
}

void solve() {
    int n,m;
    cin>>n>>m;
    gr.resize(n+1);
    rgr.resize(n+1);
    vi.resize(n+1);
    sccs.resize(n+1);

    for (int i = 0; i < m; i++) {
        int u,v;
        cin>>u>>v;
        gr[u].push_back(v);
        rgr[v].push_back(u);
    }

    for (int i = 1; i <= n; i++) {
        if (!vi[i]){
            dfs1(i);
        }
    }

    vi.assign(n+1,false);
    vector<int> temp;
    while (!st.empty()) {
        int x=st.top();st.pop();
        if (!vi[x]){
            vector<int> scc;
            dfs2(x,scc);
            int root=*min_element(all(scc));
            sccs[root]=scc;
            temp.push_back(root);
        }
    }

    sort(all(temp));
    vector<int> res(n+1);
    for (int i = 0; i < temp.size(); i++) {
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