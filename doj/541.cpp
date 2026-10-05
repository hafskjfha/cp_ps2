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
    vector<char> v;
    cin>>n>>s;

    for(char c:s){
        if (c=='H') cout<<'H';
        else v.push_back(c);
    }
    sort(all(v));
    for(char c:v) cout<<c;
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