#include <iostream>
#include <vector>
#include <algorithm>

using std::cout;
using std::endl;
using std::vector;

constexpr int FIRST = 3;
constexpr int SECOND = 7;
constexpr int TARGET = 556061;

// god even with c++ this takes way too long to complete
int main() {
    int temp_target = TARGET;
    vector<int> match_seq;
    while (temp_target) {
        match_seq.push_back(temp_target % 10);
        temp_target /= 10;
    }
    std::reverse(match_seq.begin(), match_seq.end());

    vector<int> sb{FIRST, SECOND};  // short for scoreboard
    int first_pos = 0;
    int second_pos = 1;
    int recipes_until = -1;
    while (true) {
        int total = sb[first_pos] + sb[second_pos];
        if (total >= 10) {
            sb.push_back(total / 10 % 10);
        }
        sb.push_back(total % 10);

        first_pos = (first_pos + 1 + sb[first_pos]) % sb.size();
        second_pos = (second_pos + 1 + sb[second_pos]) % sb.size();

        vector<int> curr_last;
        for (int i = sb.size() - match_seq.size(); i < sb.size(); i++) {
            curr_last.push_back(sb[i]);
        }
        if (curr_last == match_seq) {
            recipes_until = sb.size() - match_seq.size();
            break;
        }

        curr_last = vector<int>();
        for (int i = sb.size() - match_seq.size() - 1; i < sb.size() - 1; i++) {
            curr_last.push_back(sb[i]);
        }
        if (curr_last == match_seq) {
            recipes_until = sb.size() - match_seq.size() - 1;
            break;
        }
    }

    cout << "recipes until given seq: " << recipes_until << endl;
}
