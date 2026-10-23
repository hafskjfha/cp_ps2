#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,k;
    string s;
    cin>>n>>k>>s;
    ll ans=s[n-1]=='1';
    ll count0110=0,count11=0;
    for (int i = 0; i < n-1; i++) {
        if((s[i]=='0' && s[i+1]=='1') || (s[i]=='1' && s[i+1]=='0')){
            count0110++;
        }
        else if(s[i]=='1' && s[i+1]=='1'){
            count11++;
        }
        ans+=(s[i]=='1');
    }

    for (int i = 0; i < k; i++) {
        ans+=count11;
        count11*=2;
        ans+=count0110;
        count11+=count0110;
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