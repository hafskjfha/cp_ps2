#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

vector<int> parent(200001);
vector<int> tsize(200001,1);

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

    if(tsize[pu]>tsize[pv]){
        swap(pu,pv);
    }

    tsize[pv]+=tsize[pu];
    parent[pu]=pv;
}

void solve() {
    int n,q;
    cin>>n>>q;

    for (int i = 1; i <= n; i++) {
        parent[i]=i;
    }

    int t,u,v;
    for (int i = 0; i < q; i++) {
        cin>>t>>u>>v;
        if(t==0){
            merge(u,v);
        }
        else{
            int pu=find(u);
            int pv=find(v);
            cout<<(pu==pv ? 1 : 0)<<'\n';
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