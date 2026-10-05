#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n;
    cin>>n;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    ll ans;
    ll left=0,right=1e18;
    while (left<=right) {
        ll mid = left + (right - left) / 2;
        ll temp=mid;

        bool flg=true;
        for(auto x:v){
            temp+=x;
            if (temp<0){
                flg=false;
                break;
            }
        }

        if (flg){
            right=mid-1;
            ans=mid;
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