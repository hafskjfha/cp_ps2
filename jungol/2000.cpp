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
    int n,w;
    cin>>n;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }
    cin>>w;

    int dp[64001];
    fill(dp,dp+64001,INF);
    for(int& x:v){
        dp[x]=1;
    }

    for (int i = 1; i <= w; i++) {
        int temp=dp[i];
        for(int& x:v){
            if (i-x>0){
                temp=min(temp,dp[i-x]);
            }
        }
        if(temp!=INF){
            dp[i]=min(dp[i],temp+1);
        }
    }

    if(dp[w]==INF){
        cout<<"impossible";
    }else{
        cout<<dp[w];
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

// 50워늘 만들어야하고 1,5,10,15
// 1,5,10,15 =1개씩
// 2->1+1,..., 6