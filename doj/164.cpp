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
    ll m, tempm;
    cin >> n >> m;
    tempm=m;
    
    int j=0; ll temp;
    vector<ll> v(n);
    for (int i = 0; i < n; i++) {
        cin >> temp;
        if (temp <= m){
            v[j]=temp;
            j++;
        }
    }

    if (j==0) {
        cout << -1;
        return;
    }

    ll ans=0;
    int i=0;

    while (tempm > 0) {
        if (tempm & 1){
            ll temp=0, temp2=0;
            for (auto &x: v){
                if ((((x >> i) & 1) == 0) && ((m >> i) | (x >> i)) == (m >> i)){
                    temp|=x;
                }
                if ((x | m) == m){
                    temp2|=x;
                }
            }
            ans=max(ans,max(temp,temp2));
        }

        tempm>>=1;
        i++;
    }

    cout << ans;


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