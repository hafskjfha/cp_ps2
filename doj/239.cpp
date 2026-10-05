#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    string s,n="toycartoon",o;
    int idx=-1,subsz;
    cin>>s;

    int sz=s.size();
    
    for (int i = 1; i <= sz; i++) {
        string temp=s.substr(0,i);
        size_t pos=n.find(temp);
        if (pos==string::npos){
            break;
        }
        else{
            o=temp;
            idx=pos;
            subsz=i;
        }
    }

    if (idx==-1){
        if(11+sz>20) cout<<n;
        else cout<<"toycartoon_"<<s;
    }
    else{
        string result=n.substr(0,idx)+s;
        string y=n.substr(idx+subsz),yy=y;
        //cout<<y<<'\n';

        for (int i = sz-1,j=1; i > subsz; i--,j++) {
            string k=s.substr(i);
            //cout<<k<<'\n';
            if(k==y.substr(0,j)){
                yy=y.substr(j);
                //cout<<k<<' '<<yy<<' ';
            }
        }
        result+=yy;

        cout<<(result.size()<21?result:n);
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