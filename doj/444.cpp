#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct Compare {
    bool operator()(const pii& a, const pii& b) {
        if (a.first == b.first) {
            return a.second > b.second;
        }
        return a.first > b.first;
    }
};

void solve() {
    int n;
    cin>>n;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    vector<int> dp(n,INF);
    priority_queue<pii,vector<pii>,Compare> pq;
    dp[0]=0;
    pq.push({0,v[0]});

    for (int i = 1; i < n; i++) {
        while (!pq.empty() && pq.top().second<i) {
            pq.pop();
            
        }
        if(!pq.empty()){
            int x=pq.top().first;
            dp[i]=x+1;
            pq.push({x+1,i+v[i]});
        }
    }

    cout<<(dp[n-1]==INF?-1:dp[n-1])<<'\n';
}

int main() {
    fastio;

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}