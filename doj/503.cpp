#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;

using ll = long long;
using i128 = __int128;
using pii = pair<int, int>;
using pll = pair<ll, ll>;
using ordered_set = tree<ll,null_type,less<ll>,rb_tree_tag,tree_order_statistics_node_update>;

#define all(v) (v).begin(), (v).end()
template <typename T>
T max(const vector<T>& v){ return ranges::max(v); }
template <typename T>
T min(const vector<T>& v){ return ranges::min(v); }
template <typename T>
ll sum(const vector<T>& v){ return accumulate(all(v), 0LL); }
vector<string> split(const string& s, char delim = ' '){ vector<string> res; for (auto part : s | views::split(delim)) {res.emplace_back(part.begin(), part.end());} return res; }

const int INF = 1e9;
const ll LINF = 1e18;

struct Res{
    ll x1,y1,x2,y2;
};

void solve() {
    ll n,m,K;
    cin>>n>>m>>K;
    ll k=K;
    ll x=0,y=0;
    for (int i = 1; i <= max(n,m); i++) {
        if(k%i==0 && k/i<=min(n,m)){
            cout<<1<<'\n';
            if(n>m){
                cout<<0<<' '<<0<<' '<<i<<' '<<k/i<<'\n';
            }
            else{
                cout<<0<<' '<<0<<' '<<k/i<<' '<<i<<'\n';
            }
            return;
        }
    }

    cout<<2<<'\n';
    for (ll i = n; i >= 1; i--) {
        if(k/i>0){
            cout<<x<<' '<<y<<' '<<i<<' '<<y+k/i<<'\n';
            y+=k/i;
            k-=k/i*i;
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