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

vector<bool> fuck;

void dfs(string& s, ll now, int n){
    //cout<<'?'<<now<<'\n';
    if(now==(1<<n)-1){
        return;
    }

    for (int i = 0; i < n; i++) {
        if(((now>>i)&1) == 0 && (now | (1<<i))<=((1<<n)-1) && s[now | (1<<i)]=='0' && fuck[now | (1<<i)]==false){
            //cout<<(now | (1<<i))<<'\n';
            fuck[now | (1<<i)]=true;
            dfs(s,now | (1<<i),n);
        }
    }

}

void solve() {
    int n;
    string s;
    cin>>n>>s;
    s="0"+s;
    fuck.assign(s.size(),false);
    //cout<<fuck.size()<<'\n';
    dfs(s,0,n);
    // for (int i = 0; i < fuck.size(); i++) {
    //     cout<<fuck[i]<<' ';
    // }
    cout<<(fuck[(1<<n)-1]?"Yes":"No")<<'\n';
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