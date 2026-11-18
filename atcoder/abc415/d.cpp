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

void solve() {
    ll n,m;
    cin>>n>>m;
    vector<pll> v(m);
    for (int i = 0; i < m; i++) {
        cin>>v[i].first>>v[i].second;
    }
    sort(all(v),[](const auto& a, const auto& b){
        if(a.first - a.second != b.first - b.second){
            return a.first - a.second < b.first - b.second;
        }
        return a.first < b.first;
    });

    ll ans=0;
    for (ll i = 0; i < m; i++) {
        if(v[i].first > n) continue;
        ll temp=(n-v[i].first)/(v[i].first-v[i].second)+1;
        ans+=temp;
        n-=temp*(v[i].first-v[i].second);
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