#include <cmath>
#include <iostream>

struct Bot {
    int x, y, z;
    int r;

    long long dist(const Bot& b) const {
        return (long long) abs(x - b.x) + abs(y - b.y) + abs(z - b.z);
    }
};

std::ostream& operator<<(std::ostream& out, const Bot& b) {
    return out << "((" << b.x << ' ' << b.y << ' ' << b.z << ") " << b.r << ')';
}
