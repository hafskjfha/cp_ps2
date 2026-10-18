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
    vector<int> v(n);
    unordered_map<int, int, custom_hash> count;
    for (int i = 0; i < n; i++) {
        cin>>v[i];
        count[v[i]]++;
    }
    ll ans=0;
    priority_queue<int,vector<int>,greater<>> pq;
    for(auto [x,c]:count){
        if (c>1) pq.push(x);
    }

    while (!pq.empty()) {
        int x=pq.top();pq.pop();
        if(count[x]%2==0 && count[x+1]%2==1 && count[x+2]%2==1){
            cout<<-1<<'\n';
            return;
        }

        int k=count[x]/2;
        ans+=k;
        count[x]=count[x]%2 ? 1 : 0;

        if((count[x+1]==0 && k>1) || count[x+1]==1){
            
            pq.push(x+1);
        }

        if((count[x+3]==0 && k>1) || count[x+3]==1){
            
            pq.push(x+3);
        }

        count[x+1]+=k;
        count[x+3]+=k;
        

        // cout<<x<<' '<<ans<<'\n';
        // cout<<count[x+1]<<' '<<count[x+3]<<'\n';

    }

    cout<<ans<<'\n';
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