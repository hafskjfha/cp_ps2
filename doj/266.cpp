#include <bits/stdc++.h>
#include <cctype>
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
    int ans=0;
    for (int i = 0; i < n-1; i++) {
        if(s[i]=='C'&&isdigit(s[i+1])) ans++;
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