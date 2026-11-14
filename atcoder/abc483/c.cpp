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

struct custom_hash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
        return x ^ (x >> 31);
    }

    template <typename T>
    size_t operator()(T x) const {
        static const uint64_t FIXED_RANDOM = std::chrono::steady_clock::now().time_since_epoch().count();
        return static_cast<size_t>(splitmix64(static_cast<uint64_t>(x) + FIXED_RANDOM));
    }

    template <typename T, typename U>
    size_t operator()(const std::pair<T, U>& p) const {
        uint64_t h1 = operator()(p.first);
        uint64_t h2 = operator()(p.second);
        return static_cast<size_t>(splitmix64(h1 + 0x9e3779b97f4a7c15 + (h2 << 6) + (h2 >> 2)));
    }
};

void solve() {
    int n,m;
    cin>>n>>m;
    vector<ll> counter(n+1);
    vector<unordered_map<int, ll, custom_hash>> check(n+1);
    for (int i = 0; i < m; i++) {
        int a,b;
        cin>>a>>b;
        counter[a]++;
        check[a][b]++;
    }

    pair<int,ll> fir,sec;
    for (int i = 1; i <= n; i++) {
        if(fir.second < counter[i]){
            if(sec.second < fir.second){
                sec=fir;
            }
            else if(sec.second == fir.second && sec.first > fir.first){
                sec=fir;
            }
            fir={i,counter[i]};
        }
        else if(sec.second < counter[i]){
            sec={i,counter[i]};
        }
    }

    for (int i = 1; i <= n; i++) {
        pair<int,ll> temp = fir.first != i ? fir : sec;
       // temp.second+=check[i][temp.first];

        for(auto& [k,v]:check[i]){
            if(temp.second < counter[k]+v){
                temp={k,counter[k]+v};
            }
            else if (temp.second == counter[k]+v && temp.first > k){
                temp.first = k;
            }
        }
        cout<<temp.first<<'\n';
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