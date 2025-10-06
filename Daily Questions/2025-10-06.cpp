#include <vector>
using namespace std;    
class Solution {
public:
    int n;
    vector<vector<int>> dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    bool dfs(vector<vector<int>>& grid, vector<vector<bool>>& vis, int i, int j, int limit) {
        if (i == n - 1 && j == n - 1) {
            return true;
        }

        vis[i][j] = true;

        for (auto& dir : dirs) {
            int i_ = i + dir[0];
            int j_ = j + dir[1];
            if (i_ >= 0 && i_ < n && j_ >= 0 && j_ < n && !vis[i_][j_] && grid[i_][j_]<=limit) {
                if (dfs(grid, vis, i_, j_, limit)) {
                    return true;
                }
            }
        }
        return false;
    }

    int swimInWater(vector<vector<int>>& grid) {
        n = grid.size();

        int s = max(grid[0][0], grid[n - 1][n - 1]);
        int e = n * n - 1;

        int ans = e;

        while (s <= e) {
            int mid = s + (e - s) / 2;

            vector<vector<bool>> vis(n, vector<bool>(n, false));

            if (grid[0][0] <= mid && dfs(grid, vis, 0, 0, mid)) {
                ans = mid;
                e = mid - 1;
            } else {
                s = mid + 1;
            }
        }
        return ans;
    }
};