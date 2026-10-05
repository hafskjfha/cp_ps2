#include <bits/stdc++.h>
#include <string>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

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
    size_t operator()(const T& x) const {
        static const uint64_t FIXED_RANDOM =
            std::chrono::steady_clock::now().time_since_epoch().count();

        return splitmix64(
            static_cast<uint64_t>(std::hash<T>{}(x)) + FIXED_RANDOM
        );
    }

    template <typename T, typename U>
    size_t operator()(const std::pair<T, U>& p) const {
        uint64_t h1 = operator()(p.first);
        uint64_t h2 = operator()(p.second);

        return splitmix64(
            h1 + 0x9e3779b97f4a7c15ULL + (h2 << 6) + (h2 >> 2)
        );
    }
};

string sh(string s){
    vector<int> idx(26,-1), temp;
    int po=0;
    for(char c:s){
        if (idx[c-'A']==-1){
            idx[c-'A']=po;
            po++;
        }
        temp.push_back(idx[c-'A']);
    }
    string res;
    for(int i=0;i<s.size();i++){
        res.push_back('A'+idx[s[i]-'A']);
    }
    return res;
}

void solve() {
    int n;
    cin>>n;
    unordered_map<string, int, custom_hash> mp;
    string s;
    for (int i = 0; i < n; i++) {
        string x;
        cin>>x;
        mp[x]++;
    }
    cin>>s;

    string ssh=sh(s);
    //cout<<ssh<<'\n';

    int maxv=0;
    string anss="-1";
    for(auto [key,value]:mp){
        //cout<<key<<' '<<value<<'\n';
        if (key.size()==s.size() && sh(key)==ssh){
            //cout<<maxv<<' '<<anss<<'\n';
            if (maxv==0) {
                anss=key;
                maxv=value;
                continue;
            }

            if (maxv==value){
                //cout<<(anss < key)<<'\n';
                anss = (anss < key) ? anss : key;
            }
            else if (maxv<value){
                maxv=value;
                anss=key;
            }
        }
    }

    cout<<anss<<'\n';
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