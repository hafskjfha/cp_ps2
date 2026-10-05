#include <bits/stdc++.h>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,m,x;
    cin >> n >> m; m+=20000;
    vector<int> v(n);
    vector<int> visited(40001,-1);
    queue<int> q;

    for (int i = 0; i < n; i++) {
        cin >> v[i];
    }

    q.push(20000);
    visited[20000]=0;

    while (!q.empty()) {
        x=q.front(); q.pop();
        if (x==m){
            cout << visited[x];
            return;
        }

        for (int& dx: v){
            int nx=x+dx;
            if (0<=nx && nx<40001 && visited[nx]==-1){
                visited[nx]=visited[x]+1;
                q.push(nx);
            }
        }
    }

    cout << -1;

}

int main() {
    fastio;

    int T = 1;
    // cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}