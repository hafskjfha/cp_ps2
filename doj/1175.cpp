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

#define CEIL(a, b) (((a) + (b) - 1) / (b))

void solve() {
    int n;
    cin>>n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin>>arr[i];
    }

    sort(all(arr));
    int left=1,right=n+1;
    int ans=n;
    while (left<=right) {
        int mid=(left+right)/2;
        vector<int> count(mid);
        int idx=0;
        bool flg=true;
        for (int i = 0; i < n; i++) {
            if (count[idx]>arr[i]){
                flg=false;
                break;
            }
            count[idx]++;
            idx=(idx+1)%mid;
        }

        if(flg){
            ans=mid;
            right=mid-1;
        }
        else{
            left=mid+1;
        }
    }
    cout<<ans;
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