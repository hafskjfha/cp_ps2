#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void floyd(vector<vector<int>>& gr, int N) {
    for (int k = 0; k < N; ++k) {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                if (gr[i][k] != INF && gr[k][j] != INF) {
                    gr[i][j] = min(gr[i][j], gr[i][k] + gr[k][j]);
                }
            }
        }
    }
}

void solve() {
    int n,m;
    cin>>n>>m;
    vector<vector<int>> gr(n, vector<int>(n, INF));

    for (int i = 0; i < n; i++) {
        gr[i][i]=0;
    }

    int a,b;
    for (int i = 0; i < m; i++) {
        cin>>a>>b;
        gr[a-1][b-1]=1;
    }

    floyd(gr,n);

    int ans=0;
    for (int i = 0; i < n; i++) {
        bool flg=true;
        for (int j = 0; j < n; j++) {
            if(gr[i][j]==INF && gr[j][i]==INF){
                flg=false;
                break;
            }
        }
        if(flg)ans++;
    }
    cout<<ans;
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