#include <vector>
using namespace std;    

class Solution {
public:
    vector<vector<int>> dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    int m,n;
    void dfs(vector<vector<int>>& h, int i, int j, vector<vector<bool>>& vis){
        vis[i][j] = true;
        for(auto &d : dirs){
            int x = i+d[0];
            int y = j+d[1];
            if(x>=0 && x<n && y>=0 && y<m && h[x][y]>=h[i][j] && !vis[x][y]){
                dfs(h,x,y,vis);
            }
        }
    }
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        n = heights.size();
        m = heights[0].size();
        vector<vector<bool>> a(n,vector<bool>(m,false)); 
        vector<vector<bool>> p(n,vector<bool>(m,false));
        for(int i=0;i<n;i++){
            dfs(heights,i,0,p);
            dfs(heights,i,m-1,a);
        }
        for(int i=0;i<m;i++){
            dfs(heights,0,i,p);
            dfs(heights,n-1,i,a);
        }
        vector<vector<int>> result;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(p[i][j] && a[i][j]){
                    result.push_back({i,j});
                }
            }
        }
        return result;
    }
};