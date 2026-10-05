#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct DSU {
    vector<int> parent, sz;

    DSU(int n) : parent(n + 1), sz(n + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void merge(int a, int b) {
        a = find(a);
        b = find(b);
        if (a != b) {
            if (sz[a] < sz[b]) {
                swap(a, b);
            }
            parent[b] = a;
            sz[a] += sz[b];
        }
    }
};

void solve() {
    int n,x,y;
    cin>>n>>x>>y;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    DSU dsu(n);

    for (int i = 0; i < n; i++) {
        if (i+x<n){
            dsu.merge(v[i], v[i+x]);
        }
        if (i+y<n){
            dsu.merge(v[i], v[i+y]);
        }
    }

    int last=dsu.parent[1];
    bool flg=true;
    for (int i = 2; i <= n; i++) {
        if(last!=dsu.parent[i]){
            flg=false;
        }
    }

    if(flg){
        cout<<"YES"<<'\n';
    }
    else{
        for (int i = 0; i < n; i++) {
            if (dsu.find(v[i])!=dsu.find(i+1)){
                cout<<"NO"<<'\n';
                return;
            }
        }
        cout<<"YES"<<'\n';
    }


}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}