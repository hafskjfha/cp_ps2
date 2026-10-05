#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n;
    cin>>n;
    if(n==1){
        cout<<-1;
        return;
    }
    vector<vector<int>> gr(n+1);
    for (int i = 0; i < n-1; i++) {
        int u,v;
        cin>>u>>v;
        gr[u].push_back(v);
        gr[v].push_back(u);
    }

    queue<int> q;
    vector<int> dist(n+1,-1);

    for (int i = 1; i < n+1; i++) {
        if(gr[i].size()>2){
            q.push(i);
            dist[i]=0;
        }
    }

    while (!q.empty()) {
        int x=q.front(); q.pop();

        for(int y:gr[x]){
            if(dist[y]==-1){
                q.push(y);
                dist[y]=dist[x]+1;
            }
        }
    }

    for (int i = 1; i < n+1; i++) {
        cout<<(gr[i].size()>1?0:dist[i])<<' ';
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