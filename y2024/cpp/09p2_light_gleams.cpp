 #include <algorithm>
 #include <iostream>
 #include <string>
 #include <vector>

 using std::cout;
 using std::endl;
 using std::pair;
 using std::vector;

 int main() {
     std::string files;
     std::cin >> files;

     vector<pair<int, int>> blocks;
     vector<int> sizes;
     int at = 0;
     for (int i = 0; i < files.size(); i++) {
         const int size = files[i] - '0';
         if (i % 2 == 0) {
             blocks.push_back({at, i / 2});
             sizes.push_back(size);
         }
         at += size;
     }

     for (int id = sizes.size() - 1; id >= 0; id--) {
         int ind = 0;
         for (; blocks[ind].second != id; ind++);
         for (int ins_to = 1; ins_to <= ind; ins_to++) {
             const pair<int, int>& prev = blocks[ins_to - 1];
             const int space = blocks[ins_to].first - prev.first - sizes[prev.second];
             if (space >= sizes[id]) {
                 blocks.erase(blocks.begin() + ind);
                 const int new_pos = prev.first + sizes[prev.second];
                 blocks.insert(blocks.begin() + ins_to, {new_pos, id});
                 break;
             }
         }
     }

     long long checksum = 0;
     for (const auto& [start, id] : blocks) {
         for (int i = 0; i < sizes[id]; i++) {
             checksum += id * (start + i);
         }
     }

     printf("wrote p2 in c++ for better constant factor: %lld\n", checksum);
 }
