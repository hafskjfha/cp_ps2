#include <iostream>
#include <algorithm>
using namespace std;

int ans = 0;
int memo[6][16][16][16];


void backtrack(int m3, int m5, int m7, int left, int used) {
    // 3+3+3, 3+5, 3+7, 5+5, 3+3, 3, 5, 7, -
    //if (memo[left][m3][m5][m7]!=0) {ans = max(ans,memo[left][m3][m5][m7]); return;}

    if (left == 0 || used >= 15) { ans = max(ans, used); return; }
    if (m3 >= 3) { backtrack(m3 - 3, m5, m7, left-1, used+3); }
    if (m3 >= 1 && m7 >= 1) { backtrack(m3 - 1, m5, m7 - 1, left-1, used+2); }
    if (m3 >= 1 && m5 >= 1) { backtrack(m3 - 1, m5 - 1, m7, left-1, used+2); }
    if (m5 >= 2) { backtrack(m3, m5 - 2, m7, left-1, used+2); }
    if (m3 >= 2) { backtrack(m3 - 2, m5, m7, left-1, used+2); }
    if (m7 >= 1) { backtrack(m3, m5, m7 - 1, left-1, used+1); }
    if (m5 >= 1) { backtrack(m3, m5 - 1, m7, left-1, used+1); }
    if (m3 >= 1) { backtrack(m3 - 1, m5, m7, left-1, used+1); }
    
    ans = max(ans, used);
    //memo[left][m3][m5][m7]=used;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    int tc;
    cin >> tc;
    for (int x = 0; x < tc; x++) {
        int a, b, c;
        cin >> a >> b >> c;
        if (a >= 15) { cout << 15 << "\n"; continue; }
        ans = 0; backtrack(min(15,a), min(15,b), min(15,c), 5, 0);
        cout << ans << "\n";
    }
    return 0;
}