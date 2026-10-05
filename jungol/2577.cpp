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
    int n,d,k,c;
    cin>>n>>d>>k>>c;
    vector<int> v(n);
    int eat[3001]={0};
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    int count=0, ans;
    for (int i = 0; i < k; i++) {
        if (eat[v[i]]==0) count++;
        eat[v[i]]++;
    }
    ans=count+(eat[c]==0);

    for (int i = k; i < n+k; i++) {
        eat[v[(i-k)%n]]--;
        if (eat[v[(i-k)%n]]==0) count--;

        if (eat[v[i%n]]==0) count++;
        eat[v[i%n]]++;

        ans=max(ans,count+(eat[c]==0));
    }
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