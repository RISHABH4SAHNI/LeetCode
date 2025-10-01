#include <iostream>     
#include <vector>   
#include <numeric>      
#include <algorithm>
#include <climits>  
using namespace std;
class Solution {
public:
    int n;
    vector<vector<int>> dp;
    int minimum_path(int i, int j, vector<vector<int>>& triangle) {
        if (i == n - 1) {
            return triangle[i][j];
        }
        if(dp[i][j]!=INT_MAX){
            return dp[i][j];
        }
        int down    = minimum_path(i + 1, j, triangle);
        int diagonal = minimum_path(i + 1, j + 1, triangle);
        return dp[i][j] = triangle[i][j] + std::min(down, diagonal);
    }
    
    int minimumTotal(vector<vector<int>>& triangle) {
        n = triangle.size();
        dp.assign(n, vector<int>(n, INT_MAX)); 
        return minimum_path(0, 0, triangle);
    }
};
