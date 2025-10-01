
#include <iostream>
#include <vector>
#include <map>
#include <climits>
using namespace std;
class Solution {
public:
    int maxFrequencyElements(vector<int>& nums) {
        map<int,int> freq;
        for(auto num : nums){
            freq[num]++;
        }
        int maxm = INT_MIN;
        int cnt;
        for(auto num : nums){
            if(freq[num]==maxm){
                cnt+=freq[num];
            }
            else if(freq[num]>maxm){
                cnt = freq[num];
                maxm = freq[num];
            }
            freq[num]=0;
        }
        return cnt;
    }
};