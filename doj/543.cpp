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
    vector<vector<pii>> vi(n+1,vector<pii>(m+1,{INF,INF}));
    q.push({sx,sy,false});
    vi[sx][sy]={0,INF};

    while (!q.empty()) {
        auto [x,y,flg]=q.front(); q.pop();

        if(x==ex && y==ey){
            break;
        }

        if(x==cx && y==cy){
            flg=true;
            if(vi[x][y].second==INF) vi[x][y].second = vi[x][y].first;
        }

        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                int nx=x+dx[i], ny=y+dy[i];
                if(0<nx && nx<=n && 0<ny && ny<=m ){
                    bool fflg=false;
                    if(!flg && vi[nx][ny].first == INF){
                        vi[nx][ny]={vi[x][y].first+1,vi[nx][ny].second};
                        fflg=true;
                    }

                    if(vi[x][y].second != INF && vi[nx][ny].second == INF && flg){
                        vi[nx][ny]={vi[nx][ny].first,vi[x][y].second+1};
                        fflg=true;
                    }
                    
                    if(fflg)
                        q.push({nx,ny,flg});
                }
            }
        }

        if(flg){
            

            for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 4; j++) {
                    int nx=x+dx2[i], ny=y+dy2[i];
                    if(0<nx && nx<=n && 0<ny && ny<=m){
                        bool fflg=false;
                        // if (vi[nx][ny].first == INF){
                        //     vi[nx][ny]={vi[x][y].first+1,vi[nx][ny].second};
                        //     fflg=true;
                        // }
                        if(vi[nx][ny].second == INF){
                            vi[nx][ny]={vi[nx][ny].first,vi[x][y].second+1};
                            fflg=true;
                        }
                        

                        if(fflg){
                            q.push({nx,ny,flg});
                        }
                        
                    }
                }
            }
        }

        //cout<<q.size()<<endl;
    }

    int ans = min(vi[ex][ey].first,vi[ex][ey].second);
    // cout<<vi[ex][ey].first<<' '<<vi[ex][ey].second<<'\n';
    // cout<<vi[4][4].first<<' '<<vi[4][4].second<<'\n';
    // cout<<vi[sx][sy].first<<' '<<vi[sx][sy].second<<'\n';
    
    cout<<(ans==INF?-1:ans);
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