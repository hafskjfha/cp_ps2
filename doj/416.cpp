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
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    int find=1,size=0,maxv=-1,ans=0;
    bool isFind=false;
    for(int x:v){
        size++;
        maxv=max(maxv,x);
        if (find==x){
            isFind=true;
        }

        if (isFind&&size==maxv){
            ans++;
            find=maxv+1;
            isFind=false;
        }
    }

    cout<<ans;
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