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
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        cin>>v[i];
    }

    vector<int> p(n);
    p[0]=v[0];
    for (int i = 1; i < n; i++) {
        p[i]=p[i-1]+(i%2==0?1:-1)*v[i];
        //cout<<p[i]<<' ';
    }
    
    if(n%2==1){
        for (int i = 0; i < n; i++) {
            if(i%2==0){
                if (p[n-1]-p[i]<0){
                    cout<<"No"<<'\n';
                    return;
                }
            }
            else{
                if(p[i]<0){
                    cout<<"No"<<'\n';
                    return;
                }
            }
        }
        cout<<"Yes"<<'\n';
    }
    else{
        if (p[n-1]!=0){
            cout<<"No"<<'\n';
            return;
        }
        for (int i = 1; i < n; i+=2) {
            if(p[i]<0){
                cout<<"No"<<'\n';
                return;
            }
        }
        cout<<"Yes"<<'\n';
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