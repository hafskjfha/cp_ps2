#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,q;
    cin>>n>>q;
    vector<vector<int>> v(5,vector<int>(n+1));

    for (int i = 0; i < q; i++) {
        int c,a,b;
        cin>>c>>a;
        if(c==1){
            cin>>b;
            v[a][b]++;
            if(b>1) v[a][b-1]++;
            if(b+1<=n) v[a][b+1]++;
            if(a>1) v[a-1][b]++;
            if(a+1<=4) v[a+1][b]++;
        }
        else{
            int maxv=v[a][1], idx=1;
            for (int i = 2; i < n+1; i++) {
                if(maxv<v[a][i]){
                    maxv=v[a][i];
                    idx=i;
                }
            }
            cout<<idx<<'\n';
        }
    }

    int maxv=v[1][1];
    pii ans={1,1};
    for (int i = 1; i < 5; i++) {
        for (int j = 1; j < n+1; j++) {
            if(maxv<v[i][j]){
                maxv=v[i][j];
                ans={i,j};
            }
        }
    }

    cout<<ans.first<<' '<<ans.second<<'\n';
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