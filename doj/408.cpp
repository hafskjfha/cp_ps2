#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using uint64 = unsigned long long;

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

struct Event {
    ll finishTime;
    ll judgeTime;
    ll problem;
    int user;
    int order;
};

struct EventGreater {
    bool operator()(const Event& a, const Event& b) const {
        if (a.finishTime != b.finishTime) {
            return a.finishTime > b.finishTime;
        }
        return a.order > b.order;
    }
};

struct ProblemRecord {
    ll judgeTime;
    ll finishTime;
    int order;
    int user;
};

bool recordLess(const ProblemRecord& a,
                const ProblemRecord& b) {
    if (a.judgeTime != b.judgeTime) {
        return a.judgeTime < b.judgeTime;
    }
    if (a.finishTime != b.finishTime) {
        return a.finishTime < b.finishTime;
    }
    return a.order < b.order;
}

void solve(){
    int N, Q;
    cin >> N >> Q;

    vector<ll> serverFinish(N + 1, 0);
    priority_queue<Event,
                   vector<Event>,
                   EventGreater> events;

    map<string, int> userId;
    vector<string> userName;
    vector<int> solvedCount;
    vector<ll> achievedTime;

    unordered_map<ll,
                  vector<ProblemRecord>,
                  custom_hash> problemTop5;
    problemTop5.reserve(Q * 2);

    unordered_set<uint64, custom_hash> solvedPair;
    solvedPair.reserve(Q * 2);

    set<tuple<int, ll, string>> userRanking;

    auto getUserId = [&](const string& name) -> int {
        auto it = userId.find(name);
        if (it != userId.end()) {
            return it->second;
        }

        int id = static_cast<int>(userName.size());
        userId[name] = id;
        userName.push_back(name);
        solvedCount.push_back(0);
        achievedTime.push_back(0);
        return id;
    };

    auto processUntil = [&](ll t) {
        while (!events.empty() &&
               events.top().finishTime <= t) {
            Event e = events.top();
            events.pop();

            auto& top = problemTop5[e.problem];
            top.push_back({e.judgeTime,
                           e.finishTime,
                           e.order,
                           e.user});
            sort(top.begin(), top.end(), recordLess);
            if (top.size() > 5) {
                top.pop_back();
            }

            uint64 pairKey =
                (uint64(static_cast<uint32_t>(e.user)) << 32)
                | uint64(static_cast<uint32_t>(e.problem));

            if (solvedPair.insert(pairKey).second) {
                int oldCount = solvedCount[e.user];
                if (oldCount > 0) {
                    userRanking.erase({
                        -oldCount,
                        achievedTime[e.user],
                        userName[e.user]
                    });
                }

                ++solvedCount[e.user];
                achievedTime[e.user] = e.finishTime;
                userRanking.insert({
                    -solvedCount[e.user],
                    achievedTime[e.user],
                    userName[e.user]
                });
            }
        }
    };

    for (int order = 0; order < Q; ++order) {
        int type;
        ll t;
        cin >> type >> t;

        processUntil(t);

        if (type == 1) {
            int server;
            ll problem, judgeTime;
            string name;
            cin >> server >> problem >> judgeTime >> name;

            int uid = getUserId(name);
            ll startTime =
                max(t, serverFinish[server]);
            ll finishTime = startTime + judgeTime;
            serverFinish[server] = finishTime;

            events.push({finishTime,
                         judgeTime,
                         problem,
                         uid,
                         order});
        } else if (type == 2) {
            ll problem;
            cin >> problem;

            auto it = problemTop5.find(problem);
            if (it == problemTop5.end() ||
                it->second.empty()) {
                cout << -1 << '\n';
                continue;
            }

            for (const ProblemRecord& record : it->second) {
                cout << userName[record.user] << ' '
                     << record.judgeTime << '\n';
            }
        } else {
            if (userRanking.empty()) {
                cout << -1 << '\n';
                continue;
            }

            int printed = 0;
            for (auto it = userRanking.begin();
                 it != userRanking.end() && printed < 5;
                 ++it, ++printed) {
                const auto& [negativeCount, time, name] = *it;
                cout << name << ' '
                     << -negativeCount << '\n';
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ios::sync_with_stdio(false); cin.tie(nullptr);

    int T = 1;
    cin >> T;

    while (T--) {
        solve();
    }

    return 0;
}