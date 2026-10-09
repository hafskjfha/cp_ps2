#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int v;
    cin>>v;
    if (v==1 || v==2 || v==3){
        cout<<-1<<'\n';
        return;
    }

    if (v%2){
        cout<<-1<<'\n';
    }
    else{
        cout<<3*v/2<<'\n';
        for (int i = 0; i < v; i++) {
            cout<<i+1<<' '<<(i+1)%v+1<<'\n';
            if (i<v/2) cout<<i+1<<' '<<(i+v/2)%v+1<<'\n';
        }
    }
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}