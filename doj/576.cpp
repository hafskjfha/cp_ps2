#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 4e18;

void solve() {
    int N, K;
    cin >> N >> K;

    vector<vector<int>> adj(N + 1);

    for (int i = 0; i < N - 1; i++) {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> V(N + 1);
    for (int i = 1; i <= N; i++) {
        cin >> V[i];
    }

    vector<ll> C(N + 1);
    for (int i = 1; i <= N; i++) {
        cin >> C[i];
    }

    vector<ll> F(N + 1);
    for (int i = 2; i <= N; i++) {
        cin >> F[i];
    }

    vector<int> parent(N + 1, -1);
    vector<int> order;
    order.reserve(N);

    stack<int> st;
    st.push(1);
    parent[1] = 0;

    while (!st.empty()) {
        int v = st.top();
        st.pop();

        order.push_back(v);

        for (int to : adj[v]) {
            if (to == parent[v]) continue;

            parent[to] = v;
            st.push(to);
        }
    }

    vector<int> sz(N + 1, 1);

    for (int i = N - 1; i >= 1; i--) {
        int v = order[i];
        sz[parent[v]] += sz[v];
    }

    vector<int> a(N + 1);
    vector<int> R(N + 1);

    for (int i = 1; i <= N; i++) {
        a[i] = order[i - 1];
        R[i] = i + sz[a[i]];
    }

    vector<ll> prev(N + 2, 0);
    vector<ll> cur(N + 2, 0);

    prev[N + 1] = 0;

    for (int i = N; i >= 2; i--) {
        int v = a[i];

        prev[i] = C[v] + prev[i + 1];
    }

    for (int t = 1; t <= K; t++) {
        cur[N + 1] = 0;

        for (int i = N; i >= 2; i--) {
            int v = a[i];

            ll normal = C[v] + cur[i + 1];
            ll force = F[v] + prev[R[i]];

            cur[i] = min(normal, force);
        }

        swap(prev, cur);
    }

    cout << prev[2] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}