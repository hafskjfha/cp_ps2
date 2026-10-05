#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    string s;
    cin>>s;
    if (s.size()==1){
        cout<<s<<'\n';
        return;
    }
    else if (s.size()==2){
        cout<<0<<'\n';
        return;
    }

    int n=1,k=1;

    while (1) {
        int le=1;
        k=2;
        while (1) {
            le+=1+n*(k-1);
            if (le>=s.size()) break;
            k++;
        }

        if (le==s.size()){
            //cout<<n<<' '<<k<<' '<<le<<'\n';
            break;
        }

        n++;
    }

    //cout<<n<<' '<<k<<'\n';

    
    reverse(all(s));
    for (int i = 0; i < k; i++) {
        for (int j = 0; j < 1+n*i; j++) {
            //cout<<j<<' ';
            cout<<s.back();
            s.pop_back();
        }
        cout<<'\n';
    }
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