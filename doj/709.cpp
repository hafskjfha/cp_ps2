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
    array<int,2> count0={0,0};
    array<int,2> count1={0,0};
    vector<int> v(n);
    
    for (int i = 0; i < n; i++) {
        cin>>v[i];
        if(v[i]==0) count0[1]++;
        else count1[1]++;
    }

    vector<vector<int>> ans(2,vector<int> (n-1));

    for (int i = 0; i < n-1; i++) {
        if(v[i]==0){
            count0[0]++;
            count0[1]--;
        }
        else{
            count1[0]++;
            count1[1]--;
        }

        ans[0][i]=min(count0[0],count1[1])+min(count0[1],count1[0]);
        ans[1][i]=min(max(0,count0[0]-count1[0]),max(0,count1[1]-count0[1])) +
                min(max(0,count1[0]-count0[0]),max(0,count0[1]-count1[1]));
    }

    for(auto& vv:ans){
        for(int x:vv){
            cout<<x<<' ';
        }
        cout<<'\n';
    }
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    //cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}