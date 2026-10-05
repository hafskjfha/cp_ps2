#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

bool isVaild(string& s){
    int sz=s.size();
    stack<int> st;

    for(int i=0;i<sz;i++){
        char c=s[i];
        if (c=='(' || c=='[' || c=='{'){
            st.push(c=='('?0:c=='['?1:2);
        }
        else{
            if (st.empty()){
                return false;
            }
            else{
                int x=st.top();st.pop();
                int y=c==')'?0:c==']'?1:2;
                if(x!=y){
                    return false;
                }
            }
        }
    }

    if(st.empty()) return true;
    else return false;
}

void solve() {
    string s;
    cin>>s;

    if(isVaild(s)){
        cout<<"YES"<<' '<<0<<'\n';
        return;
    }

    int sz=s.size();
    string k="()[]{}";

    for (int i = 0; i < sz; i++) {
        char p=s[i];
        for(char& c:k){
            if(s[i]==c)continue;
            s[i]=c;
            if(isVaild(s)){
                cout<<"YES"<<' '<<1<<'\n'<<i+1<<' '<<c<<'\n';
                return;
            }
        }
        s[i]=p;
    }

    cout<<"NO"<<'\n';
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