#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

string ans = "";
vector<vector<char>> v(1024,vector<char>(1024));

void divq(int x, int y, int w){
    bool flg=false;
    char target=2;

    for (int i=0;i<w;i++){
        if (flg) break;

        for (int j=0;j<w;j++){
            if (target==2){
                target = v[x+i][y+j];
                continue;
            }

            if (target != v[x+i][y+j]){
                flg=true;
                break;
            }
        }
    }

    if (flg){
        ans.push_back('X');
        w>>=1;
        divq(x,y,w);
        divq(x,y+w,w);
        divq(x+w,y,w);
        divq(x+w,y+w,w);
    }
    else{
        ans.push_back(target);
        return;
    }
}

void solve() {
    int n;
    cin >> n;
    
    for (int i = 0; i < n; i++) {
        for (int j = 0;j<n;j++){
            cin >> v[i][j];
        }
    }

    divq(0,0,n);
    cout << ans;
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