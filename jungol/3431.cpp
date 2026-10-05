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

struct namu{
    int i,x1,x2,y;
};

void solve() {
    int n,q;
    cin>>n>>q;
    vector<namu> v(n);

    for (int i = 1; i <= n; i++) {
        int x1,x2,y;
        cin>>x1>>x2>>y;
        v[i-1]=namu(i,x1,x2,y);
    }

    sort(all(v),[](const namu& a,const namu& b){
        return a.x1<b.x1;
    });

    int x2=v[0].x2;

    DSU dsu(n);
    for(int i=1;i<n;i++){
        if(x2>=v[i].x1){
            dsu.merge(v[i-1].i, v[i].i);
            x2=max(x2,v[i].x2);
        }
        else{
            x2=v[i].x2;
        }
    }

    for (int i = 0; i < q; i++) {
        int u,v;
        cin>>u>>v;
        cout<<(dsu.find(u)==dsu.find(v)?1:0)<<'\n';
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