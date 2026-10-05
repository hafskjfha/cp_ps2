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
    int n,h;
    cin >> n >> h;
    vector<int> imos(h+2);

    int t;
    for (int i = 0; i < n; i++) {
        cin >> t;
        if (i%2==0){
            imos[1]++;
            imos[t+1]--;
        }
        else{
            imos[h-t+1]++;
            imos[h+1]--;
        }
    }

    

    ll now=0;
    ll ans_cut=LINF, ans_count;
    for (int i = 1; i < h+1; i++) {
        now += imos[i];
        if (now < ans_cut){
            ans_cut = now;
            ans_count = 1;
        }
        else if (now == ans_cut){
            ans_count++;
        }
        
    }

    cout << ans_cut << ' ' << ans_count;
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

//[3:5]+1 [3]++ [6]--
//[4:8]+2 [1,1,1,1,]