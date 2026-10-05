#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define fastio ios::sync_with_stdio(false); cin.tie(nullptr)
#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

struct custom_hash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
        return x ^ (x >> 31);
    }

    template <typename T>
    size_t operator()(T x) const {
        static const uint64_t FIXED_RANDOM = std::chrono::steady_clock::now().time_since_epoch().count();
        return static_cast<size_t>(splitmix64(static_cast<uint64_t>(x) + FIXED_RANDOM));
    }

    template <typename T, typename U>
    size_t operator()(const std::pair<T, U>& p) const {
        uint64_t h1 = operator()(p.first);
        uint64_t h2 = operator()(p.second);
        return static_cast<size_t>(splitmix64(h1 + 0x9e3779b97f4a7c15 + (h2 << 6) + (h2 >> 2)));
    }
};

constexpr int SIZE = 10000;

bool is_prime[SIZE];

void sieve_of_eratosthenes(){
    fill(is_prime, is_prime + SIZE, true);
    is_prime[0]=false;
    is_prime[1]=false;

    for(int i=2;i*i<SIZE;i++){
        if (is_prime[i]){
            for(int j=i*i;j<SIZE;j+=i){
                is_prime[j]=false;
            }
        }
    }
}

void solve() {
    sieve_of_eratosthenes();
    unordered_set<int, custom_hash> st;
    
    for (int i = 1001; i < SIZE; i++) {
        if (is_prime[i]){
            st.insert(i);
        }
    }
    unordered_map<int, vector<int>, custom_hash> gr;
    for(auto& x:st){
        for (int i = 10; i <= 10000; i*=10) {
            int j=i/10;
            ll temp=x-(x%i/j*j);
            for(int k=0;k<10;k++){
                temp+=k*j;
                if (st.find(temp)!=st.end()){
                    gr[x].push_back(temp);
                }
                temp-=k*j;
            }
        }
    }

    int a,b;
    cin>>a>>b;
    queue<pii> q;
    unordered_set<int, custom_hash> vi;
    q.push({a,0});
    vi.insert(a);
    
    int k,d;

    
    while (!q.empty()) {
        k=q.front().first;
        d=q.front().second;
        q.pop();
        
        if(k==b){
            cout<<d;
            return;
        }

        for(auto& dx:gr[k]){
            if(vi.find(dx)==st.end()){
                q.push({dx,d+1});
                vi.insert(dx);
            }
        }
    }
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