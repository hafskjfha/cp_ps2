#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct Itme{
    int x,y;
    bool flg;
};

void solve() {
    int n,m;
    cin>>n>>m;
    int sx,sy,ex,ey,cx,cy;
    cin>>sx>>sy>>ex>>ey>>cx>>cy;
    int a,b,c;
    cin>>a>>b>>c;

    int dx[] = {-b,b,0,0};
    int dy[] = {0,0,-a,a};

    int dx2[] = {-c,c,0,0};
    int dy2[] = {0,0,-c,c};

    queue<Itme> q;
    vector<vector<int>> vi(n+1,vector<int>(m+1,-1));
    q.push({sx,sy,false});
    vi[sx][sy]=0;

    while (!q.empty()) {
        auto [x,y,flg]=q.front(); q.pop();

        if(x==ex && y==ey){
            break;
        }

        if(x==cx && y==cy) flg=true;

        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                int nx=x+dx[i], ny=y+dy[i];
                if(0<nx && nx<=n && 0<ny && ny<=m && vi[nx][ny]==-1){
                    vi[nx][ny]=vi[x][y]+1;
                    q.push({nx,ny,flg});
                }
            }
        }

        if(flg){
            for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 4; j++) {
                    int nx=x+dx2[i], ny=y+dy2[i];
                    if(0<nx && nx<=n && 0<ny && ny<=m && vi[nx][ny]==-1){
                        vi[nx][ny]=vi[x][y]+1;
                        q.push({nx,ny,flg});
                    }
                }
            }
        }
    }

    cout<<vi[ex][ey];
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