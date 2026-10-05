#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    ll n;
    cin >> n;
    __int128 nn=n;
    __int128 res=nn*(nn-1)/2;


    cout << 1 << '\n';
    if (res==0){
        cout << 0;
        return;
    }

    string s="";

    while (res>0) {
        s+=char('0'+(res%10));
        res/=10;
    }

    for (int i = (int)s.length()-1; i>=0; i--) {
        cout << s[i];
    }
}

int main() {
    fastio;

    int T = 1;
    // cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}