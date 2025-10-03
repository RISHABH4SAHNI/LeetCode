#include <vector>
#include <queue>
#include <algorithm>
using namespace std;    
class Solution {
public:
    int trapRainWater(vector<vector<int>>& heightMap) {

        priority_queue<vector<int>, vector<vector<int>>, greater<>> q;

        int n = heightMap.size();
        int m = heightMap[0].size();
        vector<vector<int>> vis(n, vector<int>(m, 0));

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (i == 0 || i == n - 1 || j == 0 || j == m - 1) {
                    q.push({heightMap[i][j], i, j});
                    vis[i][j] = 1;
                }
            }
        }

        int dx[] = {1, -1, 0, 0};
        int dy[] = {0, 0, 1, -1};

        int ans = 0;

        while (!q.empty()) {
            int h = q.top()[0];
            int x = q.top()[1];
            int y = q.top()[2];
            q.pop();

            for (int k = 0; k < 4; k++) {

                int nx = dx[k] + x;
                int ny = dy[k] + y;

                if (nx >= 0 && nx < n && ny >= 0 && ny < m && !vis[nx][ny] ) {

                    ans += max(h - heightMap[nx][ny],0);
                    q.push({max(h, heightMap[nx][ny]), nx, ny});
                    vis[nx][ny] = 1;
                }
            }
        }

        return ans;
    }
};