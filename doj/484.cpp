#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

int cscore(string c){
    if (c=="Bronze") return 0;
    if (c=="Silver") return 5;
    if (c=="Gold") return 10;
    if (c=="Platinum") return 15;
    if (c=="Diamond") return 20;
    return 25;
}

void solve() {
    int n,d;
    string c;
    cin>>n>>c>>d;

    int base=cscore(c)+5-d;
    //cout<<base<<'!'<<'\n';

    vector<pii> v(n);
    for (int i = 0; i < n; i++) {
        int k;
        string _;
        cin>>k>>_>>c>>d;
        v[i]={cscore(c)+5-d,k};
        //cout<<v[i].first<<'!'<<'\n';
    }

    sort(all(v));

    int low=0,high=v.size()-1,ans_idx=-1;

    while (low<=high) {
        int mid=(low+high)/2;

        if(v[mid].first<=base){
            //cout<<v[mid].first<<' '<<base<<"!\n";
            ans_idx=mid;
            low=mid+1;
        }
        else{
            high=mid-1;
        }
    }

    vector<int> ans;
    if(ans_idx==-1){
        cout<<-1<<'\n';
        return;
    }
    else{
        for (int i = 0; i <= ans_idx; i++) {
            ans.push_back(v[i].second);
        }
    }

    for(int x:ans) cout<<x<<'\n';

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