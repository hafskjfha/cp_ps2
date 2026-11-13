#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    ll n,k;
    cin>>n>>k;
    vector<ll> arr(n);
    ll s=0;
    for (int i = 0; i < n; i++) {
        cin>>arr[i];
        arr[i]%=2;
        s^=arr[i];
    }

    ll temp=0;
    deque<ll> dq;
    for (int i = n-1; i >= 0; i--) {
        arr[i]^=temp;
        s^=min(k,(ll)i)*arr[i];
        temp^=arr[i];
        dq.push_back(arr[i]);
        if (dq.size()>k){
            temp^=dq.front();
            dq.pop_front();
        }
    }

    cout<<(s%2 ? "Alice" : "Bob")<<'\n';
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