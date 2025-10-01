#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

// Define gcd and lcm if not available (for C++14 or earlier)
#ifndef __cpp_lib_gcd
int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a;
}
int lcm(int a, int b) {
    return a / gcd(a, b) * b;
}
#endif
             
class Solution {
public:
    vector<int> replaceNonCoprimes(vector<int>& nums) {
        int n = nums.size();
        vector<int> result;
        int pre = nums[0];
        int post;
        for(int i=1;i<n;i++){
            post = nums[i];
            if(gcd(pre,post)!=1){
#ifdef __cpp_lib_gcd
                pre = lcm(pre,post);
#else
                pre = ::lcm(pre,post);
#endif
                while (!result.empty() && gcd(result.back(), pre) != 1) {
#ifdef __cpp_lib_gcd
                    pre = lcm(result.back(), pre);
#else
                    pre = ::lcm(result.back(), pre);
#endif
                    result.pop_back();
                }
            }
            else{
                result.push_back(pre);
                pre = post;
            }
        }
        
        result.push_back(pre);
        return result;
    }
};