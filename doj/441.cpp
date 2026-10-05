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
    string s;
    cin>>n>>s;

    int mcount=0,lcount=0;
    ll ans=0;

    vector<int> v;
    for (int i = 1; i <= 2*n; i++) {
        if(s[i-1]=='L'){
            lcount++;
            ans+=i;
        }
        else if(s[i-1]=='M'){
            mcount++;
            ans+=2*i;
        }
        else{
            v.push_back(i);
        }
    }

    for(int x:v){
        if(mcount<n){
            mcount++;
            ans+=2*x;
        }
        else{
            lcount++;
            ans+=x;
        }
    }

    cout<<((mcount==n && lcount==n)?ans:-1)<<'\n';
}

int main() {
    fastio;

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}