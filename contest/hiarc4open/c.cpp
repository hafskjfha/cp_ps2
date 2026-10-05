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
    int n,m;
    string s;
    cin>>n>>m>>s;

    vector<pii> rv, pv;

    for (int i = 0; i < n; i++) {
        string c;
        int a,b;
        cin>>c>>a>>b;
        if(c=="R"){
            rv.push_back({a,b});
        }
        else{
            pv.push_back({a,b});
        }
    }

    sort(all(rv),[](const pii&a, const pii&b){
        if (a.first==b.first){
            return a.second<b.second;
        }
        return a.first<b.first;
    });
    sort(all(pv),[](const pii&a, const pii&b){
        if (a.first==b.first){
            return a.second<b.second;
        }
        return a.first<b.first;
    });

    priority_queue<pii,vector<pii>,greater<pii>> rpq,ppq;

    int rp=0,pp=0,ans=0;
    
    for (int i = 1; i <= m; i++) {
        while (!rpq.empty()&&rpq.top().first<i) {rpq.pop();}
        while (!ppq.empty()&&ppq.top().first<i) {ppq.pop();}

        while (rp<rv.size()&&rv[rp].first<=i) {rpq.push({rv[rp].second,rv[rp].first});rp++;}
        while (pp<pv.size()&&pv[pp].first<=i) {ppq.push({pv[pp].second,pv[pp].first});pp++;}

        if(s[i-1]=='R'){
            if(!rpq.empty()){
                ans++;
                rpq.pop();
            }
        }
        else{
            if(!ppq.empty()){
                ans++;
                ppq.pop();
            }
        }
    }

    cout<<ans;


}

int main() {
    fastio;

    int T = 1;
    //cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}