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

int n,r,c;

void recursion(int a,int b,int x,int y,int depth,vector<vector<int>>& ans){
    if(depth==0){
        return;
    }

    if(b!=c && a!=r){
        for (int i = 0; i <= depth; i++) {
            ans[b][a+i]=depth;
            ans[b+i][a]=depth;
        }
        recursion(a+1,b+1,x,y,depth-1,ans);
    }
    else if(y!=c && a!=r){
        for (int i = 0; i <= depth; i++) {
            ans[y][a+i]=depth;
            ans[y-i][a]=depth;
        }
        recursion(a+1,b,x,y-1,depth-1,ans);
    }
    else if(b!=c && x!=r){
        for (int i = 0; i <= depth; i++) {
            ans[b][x-i]=depth;
            ans[b+i][x]=depth;
        }
        recursion(a,b+1,x-1,y,depth-1,ans);
    }
    else{
        for (int i = 0; i <= depth; i++) {
            ans[y][x-i]=depth;
            ans[y-i][x]=depth;
        }
        recursion(a,b,x-1,y-1,depth-1,ans);
    }
}

void solve() {
    cin>>n>>c>>r;
    r--;
    c--;
    vector<vector<int>> ans(n,vector<int>(n));

    recursion(0, 0, n-1, n-1, n-1, ans);
    for(auto& v:ans){
        for(auto& x:v){
            cout<<x<<' ';
        }
        cout<<'\n';
    }
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