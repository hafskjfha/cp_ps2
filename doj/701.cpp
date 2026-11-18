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

void query(int m,int x){
    if(m==1){
        cout<<"? first "<<x<<'\n'<<flush;
    }
    else{
        cout<<"? second "<<x<<'\n'<<flush;
    }
}

void solve() {
    int n;
    cin>>n;
    vector<int> check(n+1,-1);

    int now=1;
    while (now<=2*n) {
        query(1, now);
        int k;
        cin>>k;
        if(check[k]!=-1){
            query(2, check[k]);
            cin>>k;
            now+=1;
        }
        else{
            check[k]=now;
            now+=1;
            query(2,now);
            int t=k;
            cin>>k;
            if(t==k){
                now+=1;
                continue;
            }
            if(check[k]!=-1){
                query(1, check[k]);
                cin>>k;
                query(2, now);
                cin>>k;
                now+=1;
            }
            else{
                check[k]=now;
                now+=1;
            }
        }
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