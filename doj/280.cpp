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
    int s1,s2,e1,e2;
    cin>>s1>>e1>>s2>>e2;
    
    unordered_set<pii, custom_hash> st;

    for (int i = s1; i <= e1; i++) {
        for (int j = s2; j <= e2; j++) {
            int g=lcm(i,j);
            if (st.contains({g/i,g/j})){
                //cout<<g<<' '<<g/i<<' '<<g/j<<'\n';
                cout<<"NO";
                return;
            }
            st.insert({{g/i,g/j}});
        }
    }
    cout<<"YES";
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