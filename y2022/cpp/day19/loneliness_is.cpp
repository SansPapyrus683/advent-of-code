/* this runs really slow, but at least it works... */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <regex>
#include <map>

using namespace std;  // screw it

constexpr int P1_TIME = 24;
constexpr int P2_TIME = 32;
constexpr int P2_AMT = 3;

/** struct of relevant resources */
struct RStruct {
    int ore, clay, obby;

    bool can_craft(const RStruct& o) const {
        return ore >= o.ore && clay >= o.clay && obby >= o.obby;
    }

    int operator[](const int& ind) const {
        switch (ind) {
            case 0:
                return ore;
            case 1:
                return clay;
            case 2:
                return obby;
        }
        return -1;
    }
};

RStruct operator+(const RStruct& r1, const RStruct& r2) {
    return {r1.ore + r2.ore, r1.clay + r2.clay, r1.obby + r2.obby};
}

RStruct operator-(const RStruct& r1, const RStruct& r2) {
    return {r1.ore - r2.ore, r1.clay - r2.clay, r1.obby - r2.obby};
}

bool operator<(const RStruct& r1, const RStruct& r2) {
    if (r1.ore != r2.ore) {
        return r1.ore < r2.ore;
    }
    return r1.clay != r2.clay ? r1.clay < r2.clay : r1.obby < r2.obby;
}

struct Blueprint {
    int id;
    RStruct ore, clay, obby, geode;

    int most_geodes(const RStruct& robots, const RStruct& amt, int time) const {
        RStruct most{
            max({ore.ore, clay.ore, obby.ore, geode.ore}),
            max({ore.clay, clay.clay, obby.clay, geode.clay}),
            max({ore.obby, clay.obby, obby.obby, geode.obby})
        };

        vector<RStruct> costs{ore, clay, obby};
        vector<RStruct> build{{1, 0, 0}, {0, 1, 0}, {0, 0, 1}};
        map<pair<RStruct, RStruct>, int> best{{{robots, amt}, 0}};
        int total_max = 0;
        for (int t = 0; t < time; t++) {
            map<pair<RStruct, RStruct>, int> n_best;

            int time_left = time - t;
            int max_more = (time_left) * (time_left - 1) / 2;
            for (const auto& [state, g] : best) {
                if (g + max_more < total_max) {
                    continue;
                }

                const auto& [r, amt] = state;
                RStruct n_amt = amt + r;

                bool all_craftable = true;
                for (int i = 0; i < costs.size(); i++) {
                    if (amt.can_craft(costs[i])) {
                        if (r[i] < most[i]) {
                            pair<RStruct, RStruct> n_state = {
                                r + build[i], n_amt - costs[i]
                            };
                            n_best[n_state] = max(n_best[n_state], g);
                        }
                    } else {
                        all_craftable = false;
                    }
                }

                if (!all_craftable) {
                    n_best[{r, n_amt}] = max(n_best[{r, n_amt}], g);
                }

                if (amt.can_craft(geode)) {
                    RStruct nn_amt = n_amt - geode;
                    int next_geodes = g + time - t - 1;
                    n_best[{r, nn_amt}] = max(n_best[{r, nn_amt}], next_geodes);
                    total_max = max(total_max, next_geodes);
                }
            }
            best = n_best;
        }

        return total_max;
    }
};

int main() {
    ifstream read("what_ive_captured.txt");

    regex bot_fmt(
        "Blueprint (\\d+): Each ore robot costs (\\d+) ore. "
        "Each clay robot costs (\\d+) ore. "
        "Each obsidian robot costs (\\d+) ore and (\\d+) clay. "
        "Each geode robot costs (\\d+) ore and (\\d+) obsidian."
    );
    vector<Blueprint> bps;
    for (string bot; getline(read, bot);) {
        smatch match;
        if (regex_search(bot, match, bot_fmt)) {
            int id = stoi(match.str(1));
            bps.push_back({
                stoi(match.str(1)),
                { stoi(match.str(2)), 0, 0 },
                { stoi(match.str(3)), 0, 0 },
                { stoi(match.str(4)), stoi(match.str(5)), 0 },
                { stoi(match.str(6)), 0, stoi(match.str(7)) },
            });
        }
    }

    RStruct robot_start{1, 0, 0};

    int quality = 0;
    for (const Blueprint& bp : bps) {
        quality += bp.most_geodes(robot_start, {}, P1_TIME) * bp.id;
    }

    cout << "total quality level of blueprints: " << quality << endl;

    int p2_prod = 1;
    for (int i = 0; i < P2_AMT; i++) {
        p2_prod *= bps[i].most_geodes(robot_start, {}, P2_TIME);
    }

    cout << "product of first " << P2_AMT << " blueprints: " << p2_prod << endl;
}
