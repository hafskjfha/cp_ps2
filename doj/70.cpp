#include <bits/stdc++.h>
#include <vector>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

vector<int> lis(vector<pii>& v){
    int n=v.size();
    vector<int> tails;
    vector<int> res(n);
    for(int i=0;i<n;i++){
        auto [x,y]=v[i];
        int k = upper_bound(all(tails),y) - tails.begin();

        if(k==tails.size()){
            tails.push_back(y);
        }
        else{
            tails[k]=y;
        }
        res[i]=k+1;
    }
    return res;
}

vector<int> rlis(vector<pii>& v){
    int n=v.size();
    vector<int> tails;
    vector<int> res(n);
    for(int i=n-1;i>=0;i--){
        auto [x,y]=v[i];
        int k = upper_bound(all(tails),-y) - tails.begin();

        if(k==tails.size()){
            tails.push_back(-y);
        }
        else{
            tails[k]=-y;
        }
        res[i]=k+1;
    }
    return res;
}


void solve() {
    int n,k,l;
    cin>>n>>l>>k;
    vector<pii> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i].first>>v[i].second;
    }
    sort(all(v));
    
    vector<int> lis1 = lis(v);
    int temp=lis1[lis1.size()-1];
    vector<int> lis2 = rlis(v);
    
    // for(int x:lis1)cout<<x<<' ';
    // cout<<'\n';
    // for(int x:lis2)cout<<x<<' ';
    // cout<<'\n';

    int ans=0;
    for (int i = 0; i < n; i++) {
        if(lis1[i]>=k && lis2[i]>=l-k+1) {
            //cout<<i<<' ';
            ans++;
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