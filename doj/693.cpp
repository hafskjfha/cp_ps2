#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,q;
    string s;
    cin>>n>>q>>s;
    vector<int> v(n,0);
    vector<int> idx(n);
    for (int i = 0; i < n; i++) {
        if (s[i]=='P') {
            v[i]+=1;
            idx[i]=i;
        }
        else if (s[i]=='M'){
            v[i+1]+=1;
            idx[i]=i+1;
        }
        else{
            v[i-1]+=1;
            idx[i]=i-1;
        }
    }
    vector<int> prefixSum(n+1,0);
    for (int i = 0; i < n; i++) {
        prefixSum[i+1]=prefixSum[i]+v[i];
    }

    for (int i = 0; i < q; i++) {
        int l,r;
        cin>>l>>r;
        //cout<<prefixSum[r]-prefixSum[l-1]<<'\n';
        if(prefixSum[r]-prefixSum[l-1]==r-l+1 && idx[l-1]!=l-2 && idx[r-1]!=r) cout<<"YES"<<'\n';
        else cout<<"NO"<<'\n';
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