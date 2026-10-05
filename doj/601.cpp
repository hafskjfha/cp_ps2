#include <algorithm>
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
    vector<ll> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }
    vector<ll> temp;
    vector<ll> table;
    int lisSize=0;

    for (auto x:v) {
        if (temp.empty() || temp.back()<x){
            temp.push_back(x);
            table.push_back(lisSize);
            lisSize++;
        }
        else {
            int k=lower_bound(all(temp),x)-temp.begin();
            table.push_back(k);
            temp[k]=x;
        }
    }
    cout<<lisSize<<'\n';

    vector<ll> res;
    while (!table.empty()) {
        ll x=table.back(); table.pop_back();
        if(x==lisSize-1){
            res.push_back(v.back());v.pop_back();
            lisSize--;
        }
        else{
            v.pop_back();
        }
        if(lisSize==-1) break;
    }

    while (!res.empty()) {
        cout<<res.back()<<' ';
        res.pop_back();
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