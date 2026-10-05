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
    cin>>n>>s;
    char c=s[0];
    for (int i = 1; i < n; i++) {
        if(c=='.'){
            c=s[i];
        }
        else{
            if(s[i]!='.' && c!=s[i]){
                cout<<0<<'\n';
                return;
            }
        }
    }

    cout<<(c=='.' ? 26 : 1)<<'\n';
}

int main() {
    fastio;

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}