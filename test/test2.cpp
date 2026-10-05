#include <bits/stdc++.h>
using namespace std;

long long R;
int N;
int fullMask;
vector<int> deckValue;
array<int, 2> playerInitial;
array<int, 2> dealerInitial;

vector<int> playerScore;
vector<int> dealerScore;
vector<int> power3;
vector<int> playerCode;

vector<double> playerMemo;
vector<double> dealerMemo;
vector<char> playerVisited;  
vector<char> dealerVisited; 

int cardValue(const string& card) {
    char rank = card[0];
    if (rank == 'A') return 1;
    if ('2' <= rank && rank <= '9') return rank - '0';
    return 10;
}

int calculateScore(const array<int, 2>& initial, int addedMask) {
    int lowSum = initial[0] + initial[1];
    bool hasAce = (initial[0] == 1 || initial[1] == 1);

    for (int i = 0; i < N; ++i) {
        if (addedMask & (1 << i)) {
            lowSum += deckValue[i];
            if (deckValue[i] == 1) hasAce = true;
        }
    }

    if (hasAce && lowSum + 10 <= 21) return lowSum + 10;
    return lowSum;
}

double solveDealer(int pMask, int dMask, int code) {
    if (dealerVisited[code]) return dealerMemo[code];
    dealerVisited[code] = 1;

    int pScore = playerScore[pMask];
    int dScore = dealerScore[dMask];
    int remain = fullMask & ~(pMask | dMask);

    if (dScore > 21) {
        return dealerMemo[code] = 1.0;
    }

    if (dScore >= 17 || remain == 0) {
        if (pScore > dScore) return dealerMemo[code] = 1.0;
        if (pScore < dScore) return dealerMemo[code] = -1.0;
        return dealerMemo[code] = 0.0;
    }

    double ret = 0.0;
    int count = __builtin_popcount((unsigned)remain);

    for (int bits = remain; bits; bits &= bits - 1) {
        int bit = bits & -bits;
        int i = __builtin_ctz((unsigned)bit);
        ret += solveDealer(pMask, dMask | bit, code + 2 * power3[i]) / count;
    }

    return dealerMemo[code] = ret;
}

double solvePlayer(int pMask) {
    if (playerVisited[pMask]) return playerMemo[pMask];
    playerVisited[pMask] = 1;

    int pScore = playerScore[pMask];
    int remain = fullMask & ~pMask;

    if (pScore > 21) return playerMemo[pMask] = -1.0;

    double stayValue = solveDealer(pMask, 0, playerCode[pMask]);

    if (pScore == 21 || remain == 0) {
        return playerMemo[pMask] = stayValue;
    }

    double hitValue = 0.0;
    int count = __builtin_popcount((unsigned)remain);

    for (int bits = remain; bits; bits &= bits - 1) {
        int bit = bits & -bits;
        int nextMask = pMask | bit;

        double nextValue;
        if (playerScore[nextMask] > 21) {
            nextValue = -1.0;
        } else {
            nextValue = solvePlayer(nextMask);
        }

        hitValue += nextValue / count;
    }

    return playerMemo[pMask] = max(stayValue, hitValue);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> R >> N;

    string card;
    for (int i = 0; i < 2; ++i) {
        cin >> card;
        playerInitial[i] = cardValue(card);
    }
    for (int i = 0; i < 2; ++i) {
        cin >> card;
        dealerInitial[i] = cardValue(card);
    }

    deckValue.resize(N);
    for (int i = 0; i < N; ++i) {
        cin >> card;
        deckValue[i] = cardValue(card);
    }

    auto initialScore = [](const array<int, 2>& hand) {
        int lowSum = hand[0] + hand[1];
        bool hasAce = (hand[0] == 1 || hand[1] == 1);
        if (hasAce && lowSum + 10 <= 21) return lowSum + 10;
        return lowSum;
    };

    bool playerBlackjack = (initialScore(playerInitial) == 21);
    bool dealerBlackjack = (initialScore(dealerInitial) == 21);

    cout << fixed << setprecision(10);

    if (playerBlackjack || dealerBlackjack) {
        if (playerBlackjack && dealerBlackjack) {
            cout << 0.0 << '\n';
        } else if (playerBlackjack) {
            cout << 1.5L * R << '\n';
        } else {
            cout << -1.0L * R << '\n';
        }
        return 0;
    }

    fullMask = (1 << N) - 1;

    playerScore.resize(1 << N);
    dealerScore.resize(1 << N);
    for (int mask = 0; mask < (1 << N); ++mask) {
        playerScore[mask] = calculateScore(playerInitial, mask);
        dealerScore[mask] = calculateScore(dealerInitial, mask);
    }

    power3.resize(N + 1);
    power3[0] = 1;
    for (int i = 0; i < N; ++i) {
        power3[i + 1] = power3[i] * 3;
    }

    playerCode.assign(1 << N, 0);
    for (int mask = 1; mask < (1 << N); ++mask) {
        int bit = mask & -mask;
        int i = __builtin_ctz((unsigned)bit);
        playerCode[mask] = playerCode[mask ^ bit] + power3[i];
    }

    playerMemo.assign(1 << N, 0.0);
    dealerMemo.assign(power3[N], 0.0);
    playerVisited.assign(1 << N, 0);
    dealerVisited.assign(power3[N], 0);

    double normalizedAnswer = solvePlayer(0);
    cout << normalizedAnswer * static_cast<long double>(R) << '\n';
    return 0;
}