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
    int n;
    string s;
    cin >> n >> s;
    string s1,s2;

    for (int i = 0; i < n; i++) {
        if (i%2){
            s1+=(s[i]=='0' ? '1' : '0');
            s2+=(s[i]=='0' ? '0' : '1');
        }else{
            s1+=(s[i]=='0' ? '0' : '1');
            s2+=(s[i]=='0' ? '1' : '0');
        }
    }

    int c1=0,c2=0;
    int s1i=-1,s2i=-1;
    for (int i = 0; i < n; i++) {
        if (s1[i]=='1'){
            if (s1i==-1) s1i=i;
        }else{
            if (s1i!=-1){
                c1++;
                s1i=-1;
            }
        }

        if (s2[i]=='1'){
            if (s2i==-1) s2i=i;
        }else{
            if (s2i!=-1){
                c2++;
                s2i=-1;
            }
        }

    }

    if (s1i!=-1) c1++;
    if (s2i!=-1) c2++;

    cout << min(c1,c2);
}

int main() {
    fastio;

    int T = 1;
    // cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}