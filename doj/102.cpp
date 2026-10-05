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
    string s;
    cin>>s;
    if (s=="BOB"){
        string x;
        cin>>x;
        if (x.length()==1){
            cout<<"0 "<<x[0];
        }else{
            cout<<x[0]<<' '<<x[1];
        }
    }
    else{
        int a,b;
        cin>>a>>b;
        cout<<a<<b<<'\n';
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