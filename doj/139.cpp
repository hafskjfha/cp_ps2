#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,k;
    cin>>n>>k;
    if((n==1 && k>1)){
        cout<<-1;
        return;
    }
    if(k==0){
        for (int i = 0; i < n; i++) {
            cout<<0<<' ';
        }
        return;
    }
    
    
    for (int i = 0; i < min(n,k-1); i++) {
        cout<<i<<' ';
    }
    for (int i = 0; i < n-k+1; i++) {
        cout<<k+2<<' ';
    }
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