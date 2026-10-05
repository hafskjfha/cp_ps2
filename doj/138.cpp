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
        string s;
        cin>>n>>s;

        stack<char> stk;
        for (int i = 0; i < n; i++) {
            char c=s[i];
            if (stk.empty()) stk.push(c);
            else{
                if (stk.top()==c) stk.pop();
                else{
                    if(stk.size()>1){
                        char temp=stk.top();stk.pop();
                        if(stk.top()==c) stk.pop();
                        else{
                            stk.push(temp);
                            stk.push(c);
                        }
                    }
                    else{
                        stk.push(c);
                    }
                    
                }
            }
            //cout<<i<<' '<<stk.size()<<'\n';
        }

        if(stk.empty()) cout<<-1;
        else{
            vector<char> res(stk.size());
            int i=stk.size()-1;
            while (!stk.empty()) {
                res[i--]=stk.top();
                stk.pop();
            }
            for(char c:res)cout<<c;
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