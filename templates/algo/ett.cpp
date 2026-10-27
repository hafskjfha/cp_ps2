#include <bits/stdc++.h>
using namespace std;

const int MAX = 100005;

vector<vector<int>> adj(MAX);
vector<int> in(MAX), out(MAX);
vector<int> euler(MAX);
int timer = 0;

void dfs(int v, int parent) {
    in[v] = ++timer;
    euler[timer] = v;

    for (int next : adj[v]) {
        if (next == parent) continue;
        dfs(next, v);
    }

    out[v] = timer;
}
