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
    cin>>n;
    vector<string> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    for (int i = 1; i < n-1; i++) {
        if(v[i-1]==v[i+1]){
            cout<<"linear";
            return;
        }
    }
    cout<<"circular";

}

int main() {
    fastio;

    int T = 1;
    //cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}