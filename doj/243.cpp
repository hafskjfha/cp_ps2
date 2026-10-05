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
    int n;
    string s,a;
    cin >> n >> s >> a;
    int na=a.length();
    
    if (na>n) {
        cout << -1;
        return;
    }

    for (int i = 0; i < n; i++) {
        if (s[i]=='?') s[i]='9';
    }

    if (n>na){
        cout << s;
        return;
    }

    int x,y;
    bool flg=1;

    for (int i = 0; i < n; i++) {
        x=s[i]-'0';
        y=a[i]-'0';
        if (flg && y>x){
            cout << -1;
            return;
        }else if (x>y){
            flg=0;
        }
    }

    cout << s;


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