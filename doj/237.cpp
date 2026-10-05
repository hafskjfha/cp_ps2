#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

constexpr int MAXN=200000;

vector<vector<int>> gr(MAXN+1);
bool vi[MAXN+1];

void dfs(int node){
    vi[node]=1;
    for(auto x:gr[node]){
        if (!vi[x]){
            dfs(x);
        }
    }
}

void solve() {
    int n,m;
    cin>>n>>m;
    int u,v;
    for (int i = 0; i < m; i++) {
        cin>>u>>v;
        gr[u].push_back(v);
        gr[v].push_back(u);
    }

    int count=0;
    for (int i = 1; i <= n; i++) {
        if(!vi[i]){
            dfs(i);
            count++;
        }
        
    }

    cout<<count-1;
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