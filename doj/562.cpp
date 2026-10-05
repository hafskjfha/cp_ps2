#include <bits/stdc++.h>
#include "calculator.h"
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll LINF = 1e18;

int calculate(int A, int B, char op){
    switch (op) {
        case '+':
            return A+B;
        case '-':
            return A-B;
        case '*':
            return A*B;
        case '/':
            return A/B;
    }
}