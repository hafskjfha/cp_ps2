#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    int tc;
    cin >> tc;
    for (int x = 0; x < tc; x++) {
        int n;
        cin >> n;
        vector<int> arr(n);
        for (int i = 0; i < n; i++) { cin >> arr[i]; }

        if (n == 1) { cout << "Yes" << "\n"; continue; }
        else if (n == 2) { cout << (arr.front() == arr.back() ? "Yes" : "No") << "\n"; continue; }

        vector<int> h1, h2;
        const int L = (n+1)/2;
        for (int i = 0; i < L; i++) { h1.push_back(arr[i]); }
        for (int i = 0; i < L; i++) { h2.push_back(arr[n-1-i]); }

        bool good = true;
        int h1s=0, h2s=0;
        for (int i = 1; i < L; i++) {
            if (h1[i-1] < h1[i]) { good = false; break; }
            if (h2[i-1] < h2[i]) { good = false; break; }
            h1s+=h1[i-1]-h1[i];
            h2s+=h2[i-1]-h2[i];
        }
        cout << ((good && (h1s+h2s)%2==0) ? "Yes" : "No") << "\n";
    }
    return 0;
}