#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct Point{
    int x,y,w;

    bool operator<(const Point& other){
        if(x!=other.x){
            return x<other.x;
        }
        return y<other.y;
    }
};

void solve() {
    int n;
    cin>>n;
    vector<Point> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i].x>>v[i].y>>v[i].w;
    }
    sort(all(v));

    ll ans=0,sum=0;
    for (int i = 0; i < n; i++) {
        sum+=v[i].w;
    }
    for (int i = n-1; i >= 0; i--) {
        sum-=v[i].w;
        ans+=sum*v[i].w;
        //cout<<sum<<' '<<ans<<'\n';
    }
    cout<<ans;
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