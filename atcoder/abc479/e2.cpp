#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

int n;
vector<vector<int>> gr(200000);
vector<pii> edge(200000);
vector<int> in(200000),out(200000),euler(200000);
vector<ll> diff(200000);
int timer=0;

void dfs(int v,int p){
    in[v]=++timer;
    euler[timer]=v;

    for(int u:gr[v]){
        if (u==p) continue;
        dfs(u,v);
    }
    out[v]=timer;
}

void solve() {
    cin>>n;
    for (int i = 1; i < n; i++) {
        int u,v;
        cin>>u>>v;
        gr[u].push_back(v);
        gr[v].push_back(u);
        edge[i]={u,v};
    }

    dfs(1,0);
    ll total=0;
    for (int i = 1; i < n; i++) {
        auto [u,v]=edge[i];
        if(in[u]>in[v]) swap(u,v);
        
        int sz=out[v]-in[v]+1;
        if (sz > n-sz){
            diff[in[v]] += i;
            diff[out[v] + 1] -= i;
        }
        else{
            total += i;
            diff[in[v]] -= i;
            diff[out[v] + 1] += i;
        }
    }

    ll cur=0;
    vector<ll> ans(n+1);
    for (int i = 1; i <= n; i++) {
        cur += diff[i];
        ans[euler[i]] = total + cur;
    }

    for (int i = 1; i <= n; i++) {
        cout<<ans[i]<<' ';
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