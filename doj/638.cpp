#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>

using namespace std;
using namespace __gnu_pbds;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

using ordered_set = tree<
    long long,
    null_type,
    less<long long>,
    rb_tree_tag,
    tree_order_statistics_node_update
>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

void solve() {
    int n,q;
    cin>>n>>q;

    ordered_set os;

    for (int i = 0; i < n; i++) {
        ll x;
        cin>>x;
        os.insert(x);
    }

    for (int i = 0; i < q; i++) {
        int c;
        ll x;
        cin>>c>>x;

        if(c==1){
            os.insert(x);
        }
        else if (c==2){
            os.erase(x);
        }
        else{
            cout<<*os.find_by_order(x-1)<<'\n';
        }
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