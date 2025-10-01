#include <iostream>
#include <vector>   
#include <numeric>
#include <algorithm>
using namespace std;
class Solution {
public:
    int triangularSum(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) {
            return nums[0];
        }

        while (nums.size() > 1) {
            int m = nums.size();
            vector<int> newNums;
            for (int i = 0; i < m - 1; i++) {
                newNums.push_back((nums[i] + nums[i + 1]) % 10);
            }
            nums = newNums;
        }

        return nums[0];
    }
};
