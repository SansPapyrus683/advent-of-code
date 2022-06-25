#include <iostream>
#include <fstream>
#include <cassert>
#include <string>
#include <vector>
#include <map>
#include <set>

#include "ops.hpp"

using std::cout;
using std::endl;
using std::vector;
using std::string;

// might vary input to input, put the index of the "eqrr" instruction here
const int CHECK_IND = 28;
// this might also vary, just look for the register with the crazy numbers
const int CHECK_REG = 1;

// let's see if c++ is faster
int main() {
    std::ifstream read("day21.txt");

    string ip_token;
    int ip;
    read >> ip_token >> ip;
    assert(ip_token == "#ip");

    string op;
    int a, b, c;
    vector<Op> ops;
    while (read >> op >> a >> b >> c) {
        ops.push_back({OP_MAP.at(op), a, b, c});
    }

    // might not need long longs, not taking any chances
    std::set<long long> seen;
    vector<int> order;

    int ip_val = 0;
    vector<long long> reg(6);
    while (0 <= ip_val && ip_val < ops.size()) {
        if (ip_val == CHECK_IND) {
            int val = reg[CHECK_REG];
            if (seen.count(val)) {
                break;
            }
            seen.insert(val);
            order.push_back(val);
        }
        Op o = ops[ip_val];
        reg[ip] = ip_val;
        exe_op(reg, o);
        ip_val = reg[ip];
        ip_val++;
    }

    cout << "least op amt: " << order.front() << endl;
    cout << "most op amt: " << order.back() << endl;
}
