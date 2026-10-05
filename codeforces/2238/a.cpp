#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,c;
    cin>>n>>c;
    vector<int> a(n),b(n);
    for (int i = 0; i < n; i++) {
        cin>>a[i];
    }
    for (int i = 0; i < n; i++) {
        cin>>b[i];
    }

    int temp1=0;
    bool flg1=true;
    for (int i = 0; i < n; i++) {
        if(a[i]>=b[i]){
            temp1+=a[i]-b[i];
        }
        else{
            flg1=false;
            break;
        }
    }

    sort(all(a));
    sort(all(b));

    int temp2=c;
    bool flg2=true;
    for (int i = 0; i < n; i++) {
        if(a[i]>=b[i]){
            temp2+=a[i]-b[i];
        }
        else{
            flg2=false;
            break;
        }
    }

    if (!flg1) temp1=INF;
    if (!flg2) temp2=INF;

    if (temp1==INF && temp2==INF) cout<<-1<<'\n';
    else cout<<min(temp1,temp2)<<'\n';

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