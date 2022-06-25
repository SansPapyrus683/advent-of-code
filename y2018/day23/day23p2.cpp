#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <regex>
#include <set>
#include <algorithm>

#include "bot.hpp"

using std::cout;
using std::endl;
using std::vector;
using std::set;

set<int> set_union(const set<int>& s1, const set<int>& s2) {
    set<int> ret(s1);
    ret.insert(s2.begin(), s2.end());
    return ret;
}

set<int> set_intersection(const set<int>& s1, const set<int>& s2) {
    set<int> ret;
    for (int i : s2) {
        if (s1.count(i)) {
            ret.insert(i);
        }
    }
    return ret;
}

class BronKerbosch {
    private:
        const vector<set<int>>& adj;
        set<int> best;

        void calculate(set<int> p, set<int> r, set<int> x) {
            if (p.empty() && x.empty()) {
                if (r.size() > best.size()) {
                    best = r;
                }
            } else {
                std::pair<int, int> most_adj{-1, 0};
                for (int i : set_union(p, x)) {
                    if (adj[i].size() > most_adj.second) {
                        most_adj = {i, adj[i].size()};
                    }
                }
                for (int i : p) {
                    if (!adj[most_adj.first].count(i)) {
                        set<int> tmp_r(r);
                        tmp_r.insert(i);
                        calculate(
                            set_intersection(p, adj[i]),
                            tmp_r,
                            set_intersection(x, adj[i])
                        );
                    }
                }
            }
        }
    public:
        BronKerbosch(const vector<set<int>>& adj) : adj(adj) {
            set<int> p, r, x;  // the public radio exchange???!!
            for (int i = 0; i < adj.size(); i++) {
                p.insert(i);
            }
            calculate(p, r, x);
        }

        const set<int>& max_clique() const {
            return best;
        }
};

int main() {
    std::ifstream read("day23.txt");

    std::regex bot_fmt("pos=<(-?\\d+),(-?\\d+),(-?\\d+)>,\\s*r=(\\d+)");
    vector<Bot> bots;
    for (std::string bot; getline(read, bot);) {
        std::smatch match;
        if (std::regex_search(bot, match, bot_fmt)) {
            int x = std::stoi(match.str(1));
            int y = std::stoi(match.str(2));
            int z = std::stoi(match.str(3));
            int r = std::stoi(match.str(4));
            bots.push_back({x, y, z, r});
        }
    }

    vector<set<int>> adj(bots.size());
    for (int b1 = 0; b1 < bots.size(); b1++) {
        const Bot& bot1 = bots[b1];
        for (int b2 = b1 + 1; b2 < bots.size(); b2++) {
            const Bot& bot2 = bots[b2];
            if (bot1.dist(bot2) <= bot1.r + bot2.r) {
                adj[b1].insert(b2);
                adj[b2].insert(b1);
            }
        }
    }

    // sauce: https://todd.ginsberg.com/post/advent-of-code/2018/day23/
    const set<int>& best = BronKerbosch(adj).max_clique();

    Bot origin{0, 0, 0, -1};
    long long min_dist = INT64_MIN;
    for (int b : best) {
        min_dist = std::max(min_dist, bots[b].dist(origin) - bots[b].r);
    }

    cout << "mandattan distance of best point: " << min_dist << endl;
}
