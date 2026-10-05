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
    cin >> n;

    vector<char> type(n + 1);
    vector<string> value(n + 1);
    vector<vector<int>> child(n + 1);

    for (int i = 1; i <= n; i++) {
        cin >> type[i];

        if (type[i] == 'T') {
            int K;
            cin >> value[i] >> K;

            child[i].resize(K);
            for (int &x : child[i]) {
                cin >> x;
            }
        } else {
            cin >> value[i];
        }
    }

    vector<pii> st;
    st.push_back({1, 0});

    while (!st.empty()) {
        auto [cur, state] = st.back();
        st.pop_back();

        if (type[cur] == 'S') {
            cout << value[cur];
            continue;
        }

        if (state == 0) {
            cout << '<' << value[cur] << '>';

            st.push_back({cur, 1});

            for (int i = (int)child[cur].size() - 1; i >= 0; i--) {
                st.push_back({child[cur][i], 0});
            }
        } else {
            cout << "</" << value[cur] << '>';
        }
    }

    cout << '\n';
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