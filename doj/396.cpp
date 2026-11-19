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

void solve() {
    int n;
    string s;
    cin>>n>>s;
    int left=0, right=3*n-1;
    for (int i = 0; i < s.size(); i++) {
        if(left>right){
            cout<<"No";
            return;
        }

        int x=(s[i]=='B'?0:s[i]=='L'?1:2);

        if(x!=left%3 && x!=right%3){
            cout<<"No";
            return;
        }
        else{
            if (left%3 != right%3){
                if(left%3==x){
                    left++;
                }
                else{
                    right--;
                }
            }
            else{
                if(i<s.size()-1){
                    int t=(s[i+1]=='B'?0:s[i+1]=='L'?1:2);
                    if((left+1)%3==t){
                        left++;
                    }
                    else{
                        right--;
                    }
                }
            }
        }
    }

    cout<<"Yes";
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