#include <iostream>
#include <vector>

using std::cout;
using std::endl;
using std::vector;

constexpr int FIRST = 3;
constexpr int SECOND = 7;
constexpr int RECIPE_NUM = 556061;
constexpr int RECIPES_AFTER = 10;

int main() {
    vector<int> sb{FIRST, SECOND};  // short for scoreboard
    int first_pos = 0;
    int second_pos = 1;
    while (sb.size() < RECIPE_NUM + RECIPES_AFTER) {
        int total = sb[first_pos] + sb[second_pos];
        if (total >= 10) {
            sb.push_back(total / 10 % 10);
        }
        sb.push_back(total % 10);

        first_pos = (first_pos + 1 + sb[first_pos]) % sb.size();
        second_pos = (second_pos + 1 + sb[second_pos]) % sb.size();
    }

    cout << "recipe sequence: ";
    for (int i = sb.size() - RECIPES_AFTER; i < sb.size(); i++) {
        cout << sb[i];
    }
    cout << endl;
}
