#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>        
using namespace std;
class Solution {
public:
    int largestPerimeter(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        
        for (int i = n - 1; i >= 2; i--) {
            int a = nums[i - 2];
            int b = nums[i - 1];
            int c = nums[i];
            if (a + b > c) {
                return a + b + c;
            }
        }
        return 0;
    }
};