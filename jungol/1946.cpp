#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,m;
    cin>>n>>m;
    vector<vector<int>> gr(n+1);
    vector<int> ing(n+1);

    for (int i = 0; i < m; i++) {
        int k,u,v;
        cin>>k;
        for (int j = 0; j < k; j++) {
            cin>>v;
            if(j!=0){
                gr[u].push_back(v);
                ing[v]++;
            }
            u=v;
        }
    }

    vector<int> result;
    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if(ing[i]==0){
            result.push_back(i);
            q.push(i);
        }
    }

    while (!q.empty()) {
        int x=q.front();
        q.pop();

        for(auto y:gr[x]){
            ing[y]--;
            if(ing[y]==0){
                result.push_back(y);
                q.push(y);
            }
        }
    }

    if(result.size()==n){
        for(auto x:result){
            cout<<x<<'\n';
        }
    }
    else{
        cout<<0;
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