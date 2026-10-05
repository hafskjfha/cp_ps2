#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void dijkstra(int k, vector<ll>& d, vector<vector<pair<ll, int>>>& eg) {
    d[k] = 0;

    priority_queue<
        pll,
        vector<pll>,
        greater<pll>
    > heap;

    heap.push({0, k});

    while (!heap.empty()) {
        auto [w, v] = heap.top();
        heap.pop();

        if (d[v] != w) continue;

        for (auto [nw, nv] : eg[v]) {
            if (d[nv] > w + nw) {
                d[nv] = w + nw;
                heap.push({d[nv], nv});
            }
        }
    }
}

void solve() {
    int n,m,s;
    cin>>n>>m>>s;

    vector<vector<pair<ll,int>>> eg(n+1);
    for (int i = 0; i < m; i++) {
        int u,v;
        ll w;
        cin>>u>>v>>w;
        eg[u].push_back({w,v});
    }

    vector<ll> dist(n+1,LINF);
    dijkstra(s, dist, eg);
    for (int i = 1; i < n+1; i++) {
        if(dist[i]==LINF) cout<<"INF"<<' ';
        else cout<<dist[i]<<' ';
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