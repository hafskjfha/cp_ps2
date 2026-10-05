#include <bits/stdc++.h>
#include <cctype>
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
    cin >> n;
    vector<int> stack;

    char c;
    int a,b;
    for (int i = 0; i < n; i++) {
        cin >> c;
        if (isdigit(c)){
            stack.push_back(c-'0');
        }
        else{
            a=stack.back(); stack.pop_back();
            b=stack.back(); stack.pop_back();

            if (c=='+'){
                stack.push_back(b+a);
            }
            else if (c=='-'){
                stack.push_back(b-a);
            }
            else if (c=='*'){
                stack.push_back(b*a);
            }
            else{
                stack.push_back(b/a);
            }
        }
    }

    cout << stack[0];
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