#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

vector<vector<pii>> gr(101);
vector<int> indgree(101);

void cut(int node){
    for(auto& [next,w]:gr[node]){
        indgree[next]--;
        if(indgree[next]==0){
            cut(next);
        }
    }
}

void solve() {
    int n,m;
    cin>>n>>m;
    for (int i = 0; i < m; i++) {
        int u,v,w;
        cin>>u>>v>>w;
        gr[u].push_back({v,w});
        indgree[v]++;
    }

    vector<int> vcount(n+1);
    vector<bool> isbasic(n+1);
    vcount[n]=1;

    queue<int> q;
    q.push(n);

    for (int i = 1; i < n; i++) {
        if(indgree[i]==0){
            cut(i);
        }
    }

    while(!q.empty()){
        int node=q.front(); q.pop();

        if(gr[node].size()==0){
            isbasic[node]=true;
        }
        else{
            for(auto& [next,w]:gr[node]){
                vcount[next]+=vcount[node]*w;
                indgree[next]--;
                if(indgree[next]==0){
                    q.push(next);
                }
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        if(isbasic[i]){
            cout<<i<<' '<<vcount[i]<<'\n';
        }
    }
}

int main() {
    fastio;

    int T = 1;
    //cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}
