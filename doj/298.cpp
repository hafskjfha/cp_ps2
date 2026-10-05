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

    if(n%2==1){
        cout<<"NO";
        return;
    }

    string t="PAUL";
    int state=0;
    
    for (int i = 0; i < n; i++) {
        if(s[i]==t[state] && state%2 == i%2){
            state++;
        }
    }

    cout<<(state==4?"YES":"NO");
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