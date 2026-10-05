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

    int x=-1,ans=0;
    
    for (int i = 0; i < n; i++) {
        if (s[i]=='6' || s[i]=='7'){
            if (x==-1) x=i;
        }
        else{
            if (x!=-1){
                ans+=(i-x+1)/2;
                x=-1;
            }
        }
    }

    if (x!=-1){
        ans+=(n-x+1)/2;
        x=-1;
    }

    cout << (ans > n/2 ? -1 : ans);
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