#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

vector<ll> v;
int p;
ll x;

ll pow(ll a, int b) {
    ll res = 1;
    for (int i = 0; i < b; i++) {
        if (res > x / a)
            return x + 1;
        res *= a;
    }
    return res;
}

bool dfs(int depth,ll sum){
    if(depth==p){
        for(int k=p+1;k<11;k++){
            ll si=0;
            for(int i=0;i<p;i++){
                ll temp=0;
                for(int j=0;j<k-i-1;j++){
                    temp+=v[j];
                }
                si+=pow(temp,p-i);
            }
            if(si==x) return true;
            else if(si>x) return false;
            v[k-1]=si;
        }

        return false;
    }

    ll limit = 0;

    while (pow(limit + 1, p) <= x) {
        limit++;
    }

    for (ll i = 1; ; i++) {
        if (sum + i + (p - depth - 1) > limit)
            break;

        v[depth] = i;

        if (dfs(depth + 1, sum + i))
            return true;
    }

    return false;

}

void solve() {
    cin>>x>>p;
    v.assign(11,0);
    v[0]=p;
    dfs(1,p);

    for(int i=1;i<p;i++){
        cout<<v[i]<<' ';
    }
    cout<<'\n';
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}