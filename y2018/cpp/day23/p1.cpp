#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <regex>
#include <algorithm>

#include "bot.hpp"

using std::cout;
using std::endl;
using std::vector;

int main() {
    std::ifstream read("input/day23.txt");

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
    
    int max_r = INT32_MIN;
    for (const Bot& b : bots) {
        max_r = std::max(max_r, b.r);
    }

    int in_range = 0;
    for (const Bot& b1 : bots) {
        if (b1.r == max_r) {
            for (const Bot& b2 : bots) {
                in_range += b1.dist(b2) <= b1.r;
            }
            break;
        }
    }

    cout << "# of bots in range of biggest one: " << in_range << endl;
}
