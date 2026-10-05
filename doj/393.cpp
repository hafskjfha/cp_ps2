#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct DSU{
    vector<int> parent, sz;

    DSU(int n){
        parent.resize(n+1);
        sz.assign(n+1,1);
        for (int i = 1; i <= n; i++) {
            parent[i]=i;
        }
    }

    int find(int u){
        if (parent[u]==u){
            return u;
        }
        return parent[u]=find(parent[u]);
    }

    void merge(int u,int v){
        int pu=find(u);
        int pv=find(v);
        if(pu==pv){
            return;
        }
        if(sz[pu]>sz[pv]){
            swap(pu,pv);
        }
        sz[pv]+=sz[pu];
        parent[pu]=pv;
    }
};

struct Edge{
    int u,v,w;

    bool operator<(const Edge& other) const {
        return w < other.w;
    }
};

ll mst(vector<Edge>& egr, bool is0, int n){
    DSU dsu(n);
    int count=0;
    ll mstw=0;

    for (auto& [u,v,w]: egr) {
        if (dsu.find(u)!=dsu.find(v)){
            if (u==0 || v==0) is0=true;
            mstw+=w;
            dsu.merge(u, v);
            count++;
            if(count==n-(is0 ? 0 : 1)){
                return mstw;
            }
        }
    }

    if (count == n-(is0 ? 0 : 1)){
        return mstw;
    }
    else{
        return LINF;
    }
}

void solve() {
    int n,m;
    cin>>n>>m;
    
    vector<Edge> egr(m);
    for (int i = 0; i < m; i++) {
        int u,v,w;
        cin>>u>>v>>w;
        egr.push_back({u,v,w});
    }

    sort(all(egr));

    ll a,b;
    a=mst(egr,false,n);

    for (int i = 0; i < n; i++) {
        int a;
        cin>>a;
        egr.push_back({0,i+1,a});
    }

    sort(all(egr));
    b=mst(egr,true,n);

    cout<<min(a,b);
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