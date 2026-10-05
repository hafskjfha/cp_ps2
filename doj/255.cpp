#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    string s,t;
    cin>>s>>t;
    set<char> tset(all(t));

    ll ans=0;
    unordered_map<char,int> mp;
    for(auto& c:s){
        mp[c]++;
    }

    for(auto& c:tset){
        ans+=mp[c];
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