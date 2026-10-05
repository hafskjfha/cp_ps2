#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)

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
    int n;
    cin>>n;
    unordered_map<pll, int, custom_hash> mp;
    ll a,b,c;
    for (int i = 0; i < n; i++) {
        cin>>a>>b>>c;
        pll s = {-a,b};
        if(s.second < 0){
            s.first*=-1;
            s.second*=-1;
        }
        ll d = gcd(s.first,s.second);
        s.first/=d;
        s.second/=d;

        mp[s]++;
    }

    ll ans=n*(n-1)/2;
    for(auto& [k,v]:mp){
        ans-=v*(v-1)/2;
    }
    cout<<ans;

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