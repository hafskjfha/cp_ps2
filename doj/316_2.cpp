#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct Edge{
    int v,w;

    bool operator<(const Edge& other) const {
        return w < other.w;
    }
};

struct Compare {
    bool operator()(const Edge& a, const Edge& b) {
        return a.w > b.w; // min heap
    }
};

void solve() {
    int n,m;
    cin>>n>>m;
    vector<vector<Edge>> gr(n+1);
    for (int i = 0; i < m; i++) {
        int u,v,w;
        cin>>u>>v>>w;
        gr[u].push_back({v,w});
        gr[v].push_back({u,w});
    }

    priority_queue<Edge,vector<Edge>,Compare> pq;
    vector<bool> vi(n+1);
    ll mstw=0;
    int count=0;

    pq.push({1,0});
    

    while (!pq.empty()) {
        auto [u,w]=pq.top();
        pq.pop();

        if(vi[u]) continue;
        vi[u]=true;
        count++;
        mstw+=w;

        if(count==n) break;

        for(Edge e:gr[u]){
            pq.push(e);
        }
    }

    if (count==n){
        cout<<mstw;
    }
    else{
        cout<<"IMPOSSIBLE";
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