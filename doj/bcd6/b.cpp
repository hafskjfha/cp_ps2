#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct Ress{
    int i1,j1,i2,j2;
};

void solve() {
    int n,m;
    cin>>n>>m;
    vector<string> s;
    for (int i = 0; i < n; i++) {
        cin>>s[i];
    }

    vector<vector<bool>> check(n,vector<bool>(m));

    vector<Ress> res;

    string ccc="ad";

    vector<pii> sq;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (s[i][j]=='s')sq.push_back({i,j});
        }
    }

    for(auto [x,y]:sq){
        vector<pii> temp = {{x,y}};
        int state=0, count=0;
        bool flg=false;

        for (int i = x-1; i > -1; i--) {
            if (check[i][y]) break;

            if (s[i][y]==ccc[state]){
                if (state==1){
                    temp.push_back({i+1,y});
                    temp.push_back({i,y});
                }
                state=(state+1)%2;
            }
            else break;
        }

        if (count!=0){
            flg=true;
            for (auto [a,b]:temp){
                check[a][b]=true;
            }
            res.push_back({temp[temp.size()-1].first+1,temp[temp.size()-1].second+1,temp[0].first+1,temp[0].second+1});
        }

        if (!flg){
            vector<pii> temp = {{x,y}};
            int state=0, count=0;

            for (int j = y-1; j > -1; j--) {
                if (check[x][j]) break;

                if(s[x][j]==ccc[state]){
                    if(state==1){
                        temp.push_back({x,j+1});
                        temp.push_back({x,j});
                    }
                    state=(state+1)%2;
                }
            }

            if (count!=0){
                flg=true;
                for (auto [a,b]:temp){
                    check[a][b]=true;
                }
                res.push_back({temp[temp.size()-1].first+1,temp[temp.size()-1].second+1,temp[0].first+1,temp[0].second+1});
            }
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if(check[i][j]==false){
                cout<<"NO"<<'\n';
                return;
            }
        }
    }

    cout<<"YES"<<'\n'<<res.size()<<'\n';
    for(auto a:res){
        cout<<a.i1<<' '<<a.j1<<' '<<a.i2<<' '<<a.j2<<'\n';
    }


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