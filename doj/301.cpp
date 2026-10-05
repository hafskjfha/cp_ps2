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
    ll h,s;
    cin >> h >> s;
    if (h==1 || h==2){
        cout << 1;
        return;
    }
    else if (h==3 || h==4){
        cout << s+(h+1)/2;
        return;
    }
    
    ll r=0, k=min((h-5),s);
    r+=2*k;
    s-=k;
    if (s>0){
        r+=s/2*3;
        s%=2;
        if (s){
            r+=4;
        }
        else{
            r+=3;
        }
    }
    else{
        r+=(h-k+1)/2;
    }

    cout << r;
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