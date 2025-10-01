#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <climits>
using namespace std;    
class Solution {
public:
    int dp[50][50]={};
    int minScoreTriangulation(vector<int>& values, int i=0,int j=0,int res = 0) {
        if(j==0){
            j = values.size()-1;
        }
        if(j-i<2){
            return 0;
        }
        if(dp[i][j]!=0){
            return dp[i][j];
        }
        res = INT_MAX;
        for(int k=i+1;k<j;k++){
            int score = minScoreTriangulation(values,i,k) + minScoreTriangulation(values,k,j) + values[i]*values[j]*values[k];
            res = min(res,score);
        }
        return dp[i][j] = res;
        
    }
};