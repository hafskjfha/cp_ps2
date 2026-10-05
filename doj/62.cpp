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
    string s;
    cin >> n >> s;

    if (s=="01" || s=="10"){
        cout << -1;
        return;
    }
    else if (s[0]==s[n-1]){
        cout << 0;
        return;
    }
    else{
        int x=-1,y=-1;
        for (int i=0;i<n;i++){
            if (s[0]!=s[i] && x==-1) x=i;
            if (s[n-1]!=s[n-i-1] && y==-1) y=i;
            if (x!=-1 && y!=-1) break;
        }
        cout << min(x,y);
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