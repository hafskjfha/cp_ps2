#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

string board[9];
bool status[9];
int n;
ll ans=0;

void backt(int count){
    if (count==n){
        ans++;
        return;
    }

    for (int i = 0; i < n; i++) {
        if (board[i][count]=='.' && !status[i]){
            status[i]=1;
            backt(count+1);
            status[i]=0;
        }
    }
}

void solve() {
    cin>>n;
    for (int i = 0; i < n; i++) {
        cin>>board[i];
    }
    backt(0);
    cout<<ans;

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