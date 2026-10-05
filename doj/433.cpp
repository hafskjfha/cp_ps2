#include <algorithm>
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

struct Point{
    int x,y,i;
};

void solve() {
    int n;
    cin>>n;
    vector<Point> v(n);
    DSU dsu(n);
    for (int i = 0; i < n; i++) {
        pii temp;
        cin>>v[i].x>>v[i].y;
        v[i].i=i+1;
    }
    sort(all(v),[](const auto& a, const auto& b){
        if(a.x == b.x) return a.y < b.y;
        return a.x < b.x;
    });
    for (int i = 1; i < n; i++) {
        if (v[i-1].x==v[i].x){
            if (v[i-1].y+1!=v[i].y){
                cout<<"NO";
                return;
            }
            dsu.merge(v[i-1].i, v[i].i);
        }
    }
    
    sort(all(v),[](const auto& a,const auto& b){
        if (a.y == b.y) {
            return a.x < b.x;
        }
        return a.y < b.y;
    });
    for (int i = 1; i < n; i++) {
        if (v[i-1].y==v[i].y){
            if (v[i-1].x+1!=v[i].x){
                cout<<"NO";
                return;
            }
            dsu.merge(v[i-1].i, v[i].i);
        }
    }

    int k=dsu.parent[1];
    for (int i = 2; i < n+1; i++) {
        //cout<<dsu.parent[i]<<' ';
        if (dsu.parent[i]!=k){
            cout<<"NO";
            return;
        }
    }
    cout<<"YES";
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