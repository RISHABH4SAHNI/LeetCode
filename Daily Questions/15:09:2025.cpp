#include <iostream>
#include <string>
#include <unordered_set>
#include <sstream>
#include <vector>    
#include <iterator>
using namespace std;
class Solution {
public:
    int canBeTypedWords(string text, string brokenLetters) {
        unordered_set<char> broken;
        for (char c : brokenLetters) {
            broken.insert(c);
        }

        int cnt = 0;
        std::istringstream iss(text);
        std::vector<std::string> words{std::istream_iterator<std::string>(iss),
                                       std::istream_iterator<std::string>()};

        for (const string &s : words) {
            bool flag = true;
            for (char c : s) {
                if (broken.count(c)) {
                    flag = false;
                    break;
                }
            }
            if (flag) {
                cnt++;
            }
        }
        return cnt;
    }
};
