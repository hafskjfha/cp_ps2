#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

vector<int> ans;
vector<vector<bool>> gr,vi;

const int dx[]={0,0,-1,1};
const int dy[]={1,-1,0,0};

void dfs(int x,int y){

}

void solve() {
    int n,m,k;
    cin>>m>>n>>k;

    gr.assign(m,vector<bool>(n));
    vi.assign(m,vector<bool>(n+1))

    for (int i = 0; i < k; i++) {
        int x1,y1,x2,y2;
        cin>>x1>>y1>>x2>>y2;
        for(;x1<=x2;x1++){
            for(;y1<=y2;y1++){
                gr[x1][y1]=true;
            }
        }
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