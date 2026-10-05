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
    string s;
    cin>>n>>s;
    ll ans=0;
    array<int,4> ch={0,1,2,3};
    for (int i = 0; i < n; i++) {
        array<int,4> st = {0,1,2,3};
        for (int j = i; j < n; j++) {
            if(s[j]=='H'){
                swap(st[0],st[2]);
                swap(st[1],st[3]);
            }
            else if (s[j]=='X'){
                swap(st[0],st[1]);
            }
            else{
                swap(st[2],st[3]);
            }
            if (st==ch) ans++;
            // for(int x:st)cout<<x<<' ';
            // cout<<'\n';
        }
        
    }
    cout<<ans<<'\n';
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