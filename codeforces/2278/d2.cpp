#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

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
    int n;
    cin>>n;
    unordered_map<ll, ll, custom_hash> count;
    for (int i = 0; i < n; i++) {
        int x;
        cin>>x;
        count[x]++;
    }
    
    vector<ll> temp;
    for(auto [k,v]:count)temp.push_back(k);
    sort(all(temp));

    deque<ll> dq;
    for(ll x:temp)dq.push_back(x);

    ll ansv=0,ansc=0;
    while (dq.size()>1) {
        ll x=dq.front();
        ll y=dq.back();

        ll cx=count[x];
        ll cy=count[y];

        if(cx<cy){
            dq.pop_front();
            ansv+=(dq.front()-x)*cx;
            ansc+=(dq.front()-x);
            count[dq.front()]+=cx;
            count[x]=0;
        }
        else{
            dq.pop_back();
            ansv+=(y-dq.back())*cy;
            ansc+=(y-dq.back());
            count[dq.back()]+=cy;
            count[y]=0;
        }
    }

    cout<<ansv<<' '<<ansc<<'\n';

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