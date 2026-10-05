#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
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
    ll l,x,v;
    int n,k;
    cin>>l>>n>>k;
    queue<pll> q;
    unordered_set<ll, custom_hash> st;

    
    for (int i = 0; i < n; i++) {
        cin>>x;
        pll pair={x,0};
        st.insert(x);
        q.push(pair);
    }
    
    while (!q.empty()) {
        x=q.front().first;
        v=q.front().second;
        q.pop();

        cout<<v<<'\n';
        k--;
        if (k==0){
            return;
        }

        if(x>=1 && st.find(x-1)==st.end()){
            pll pair={x-1,v+1};
            q.push(pair);
            st.insert(x-1);
        }

        if (x<l && st.find(x+1)==st.end()){
            pll pair={x+1,v+1};
            q.push(pair);
            st.insert(x+1);
        }
    }
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