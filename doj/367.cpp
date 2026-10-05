#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct Point{
    int x,y,idx;
};

void solve() {
    int n;
    cin>>n;
    vector<Point> v(n);
    for (int i = 0; i < n; i++) {
        Point temp;
        cin>>temp.x>>temp.y;
        temp.idx=i+1;
        v[i]=temp;
    }
    vector<Point> v2=v;

    sort(all(v),[](const Point& a, const Point& b){
        return a.x>b.x;
    });
    sort(all(v2),[](const Point& a, const Point& b){
        return a.y>b.y;
    });

    vector<bool> check(n+1);
    vector<int> ans;

    for (int i = 1; i <= n; i++) {
        if (i&1){
            while (check[v2.back().idx]) {
                v2.pop_back();
            }
            ans.push_back(v2.back().idx);
            check[v2.back().idx]=true;
        }
        else{
            while (check[v.back().idx]) {
                v.pop_back();
            }
            ans.push_back(v.back().idx);
            check[v.back().idx]=true;
        }
        
        //if(ans.size()==n) break;
    }

    cout<<"YES"<<'\n';
    for(int x:ans){
        cout<<x<<' ';
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