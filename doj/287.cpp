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
    cin>>n;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    ll rain=0,tour=0,temp=0;
    for (int i = 0; i < n; i++) {
        temp+=v[i];
        tour+=temp;
    }

    temp=0;
    for (int i = n-1; i >= 0; i--) {
        temp+=v[i];
        rain+=temp;
    }

    cout<<rain-tour<<'\n';
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