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
    map<ll,ll> count;
    for (int i = 0; i < n; i++) {
        int x;
        cin>>x;
        count[x]++;
    }
    
    vector<ll> temp;
    for(auto [k,v]:count)temp.push_back(k);
    sort(all(temp));

    deque<ll> dq;
    for(ll x:temp)dq.push_back(x);

    ll ansv=0,ansc=0;
    while (dq.size()>1) {
        ll x=dq.front();
        ll y=dq.back();

        ll cx=count[x];
        ll cy=count[y];

        if(cx<cy){
            dq.pop_front();
            ansv+=(dq.front()-x)*cx;
            ansc+=(dq.front()-x);
            count[dq.front()]+=cx;
            count[x]=0;
        }
        else{
            dq.pop_back();
            ansv+=(y-dq.back())*cy;
            ansc+=(y-dq.back());
            count[dq.back()]+=cy;
            count[y]=0;
        }
    }

    cout<<ansv<<' '<<ansc<<'\n';

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