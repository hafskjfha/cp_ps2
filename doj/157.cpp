#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

ll modinv(ll a, ll b) {
    ll mod = b;
	ll s0 = 1, s1 = 0;
	ll t0 = 0, t1 = 1;
	ll q, temp;

	while (b != 0) {
		q = a /b;
		temp = a % b;
		a = b;
		b = temp;

		temp = s1;
		s1 = s0 - q * s1;
		s0 = temp;

		temp = t1;
		t1 = t0 - q * t1;
		t0 = temp;
	}

	return ((s0) % (mod) + (mod)) % (mod);
}

void solve() {
    ll n;
    cin >> n;
    vector<vector<ll>> v(3, vector<ll>(n));

    for (int i=0;i<3;i++){
        for (int j=0;j<n;j++){
            cin >> v[i][j];
        }
    }

    sort(all(v[0]));
    sort(all(v[1]));
    sort(all(v[2]));

    const ll mod = 998244353;
    ll inv=modinv((n*n % mod)*n,mod);
    vector<ll> ans(3);

    for (int i=0;i<3;i++){
        for (int j=0;j<n;j++){
            ll cnt1 = lower_bound(all(v[(i+1)%3]), v[i][j]) - v[(i+1)%3].begin();
            ll cnt2 = lower_bound(all(v[(i+2)%3]), v[i][j]) - v[(i+2)%3].begin();

            ans[i] = (ans[i] + cnt1 * cnt2) % mod;
        }
    }

    for (int i=0;i<3;i++){
        cout << (ans[i] * inv) % mod << ' ';
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