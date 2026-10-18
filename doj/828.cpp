#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    ll n,k;
    cin>>n>>k;
    if(k%2 || n<k/2){
        cout<<0;
    }
    else if(k==0){
        cout<<n;
    }
    else{
        cout<<k/2*6*(n-k/2);
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