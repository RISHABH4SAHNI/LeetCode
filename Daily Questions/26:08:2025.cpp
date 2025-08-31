#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    int areaOfMaxDiagonal(vector<vector<int>>& dimensions) {
        priority_queue<pair<int,int>,vector<pair<int,int>>> pq;
        for(int i=0;i<dimensions.size();i++){
            int diagnol = dimensions[i][0]*dimensions[i][0] + dimensions[i][1]*dimensions[i][1];
            int area = dimensions[i][0]*dimensions[i][1];
            pq.push({diagnol,area});
        }
        return pq.top().second;
    }
};