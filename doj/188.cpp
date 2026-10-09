#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    ll n;
    cin>>n;
    ll left=0,right=2e9,ans;
    while (left<=right) {
        ll mid = left+(right-left)/2;

        ll q=mid/3,r=mid%3;
        if(9*q*(q+1)/2+3*r*(q+1)-2<=n){
            ans=mid;
            left=mid+1;
        }
        else{
            right=mid-1;
        }
    }
    cout<<ans+1<<'\n';
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