#include <vector>
#include <climits>
using namespace std;

class Solution {
public:
    int minimumArea(vector<vector<int>>& grid) {
        int n = grid.size();
        int m = grid[0].size();

        int maxl = -1, maxb = -1;
        int minl = m, minb = n;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (grid[i][j] == 1) {
                    maxl = max(maxl, j);
                    maxb = max(maxb, i);
                    minl = min(minl, j);
                    minb = min(minb, i);
                }
            }
        }

        if (maxl == -1) return 0;

        return (maxl - minl + 1) * (maxb - minb + 1);
    }
};
