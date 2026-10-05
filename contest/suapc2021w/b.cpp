#include <bits/stdc++.h>
using namespace std;

using ll = long long;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)

void solve() {
    int n, count[50001]={0},c;
    cin>>n;
    for (int i = 0; i < n; i++) {
        cin>>c;
        count[c]++;
    }
    int ans=0;
    for (int i = 1; i < 50001; i++) {
        ans=max(ans,count[i]);
    }
    cout<<ans;
}

int main() {
    fastio;

    solve();

    return 0;
}