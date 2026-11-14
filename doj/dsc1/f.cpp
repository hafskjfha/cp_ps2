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

ll countsq(const string& s){
    int count[26]={0};
    for(char c:s){
        count[c-'a']++;
    }
    ll temp=0;
    for (int i = 0; i < 26; i++) {
        temp+=count[i]*count[i];
    }
    return temp;
}

void solve() {
    int n;
    cin>>n;
    vector<string> arr(n);
    for (int i = 0; i < n; i++) {
        cin>>arr[i];
    }

    sort(all(arr),[](const string& a, const string& b){
        ll ac=countsq(a);
        ll bc=countsq(b);
        if(ac != bc){
            return ac<bc;
        }

        if(a.size()!=b.size()){
            return a.size() < b.size();
        }

        return a<b;
    });

    for(auto& s:arr){
        cout<<s<<'\n';
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