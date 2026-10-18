#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;



void solve() {
    int n,m;
    cin>>n>>m;
    vector<vector<pii>> gr(n+1);
    vector<int> ans(m+1,-1);

    for(int i=1;i<=m;i++){
        int u,v;
        cin>>u>>v;
        gr[u].push_back({v,i});
        gr[v].push_back({u,i});
    }

    vector<bool> vi(n+1);
    queue<int> q;
    int cost=1;

    vi[1]=true;
    q.push(1);
    

    while (!q.empty()) {
        int u=q.front();q.pop();
        for(auto [v,i]:gr[u]){
            if(!vi[v]){
                vi[v]=true;
                q.push(v);
                ans[i]=cost++;
                //cout<<u<<' '<<v<<' '<<i<<'\n';
            }
        }
    }

    for(int i=1;i<=m;i++){
        cout<<(ans[i]!=-1 ? ans[i] : cost++)<<' ';
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