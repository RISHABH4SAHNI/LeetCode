#include <vector>
#include <climits>
using namespace std;

class Solution {
private:
    vector<vector<int>> rotateClockWise(const vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        vector<vector<int>> rotated(n, vector<int>(m));

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                rotated[j][m - i - 1] = grid[i][j];
            }
        }
        return rotated;
    }

    int minimumArea(int startRow, int endRow, int startCol, int endCol, const vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();

        int minRow = m, maxRow = -1, minCol = n, maxCol = -1;

        for (int i = startRow; i < endRow; i++) {
            for (int j = startCol; j < endCol; j++) {
                if (grid[i][j] == 1) {
                    minRow = min(minRow, i);
                    maxRow = max(maxRow, i);
                    minCol = min(minCol, j);
                    maxCol = max(maxCol, j);
                }
            }
        }

        if (maxRow == -1) return 0; // no 1s in this subgrid
        return (maxRow - minRow + 1) * (maxCol - minCol + 1);
    }

    int helper(const vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        int result = INT_MAX;

        // Case 1: top + bottomLeft + bottomRight
        for (int rowSplit = 1; rowSplit < m; rowSplit++) {
            for (int colSplit = 1; colSplit < n; colSplit++) {
                int top = minimumArea(0, rowSplit, 0, n, grid);
                int bottomLeft = minimumArea(rowSplit, m, 0, colSplit, grid);
                int bottomRight = minimumArea(rowSplit, m, colSplit, n, grid);

                result = min(result, top + bottomLeft + bottomRight);
            }
        }

        // Case 2: topLeft + topRight + bottom
        for (int rowSplit = 1; rowSplit < m; rowSplit++) {
            for (int colSplit = 1; colSplit < n; colSplit++) {
                int topLeft = minimumArea(0, rowSplit, 0, colSplit, grid);
                int topRight = minimumArea(0, rowSplit, colSplit, n, grid);
                int bottom = minimumArea(rowSplit, m, 0, n, grid);

                result = min(result, topLeft + topRight + bottom);
            }
        }

        // Case 3: top + middle + bottom
        for (int split1 = 1; split1 < m; split1++) {
            for (int split2 = split1 + 1; split2 < m; split2++) {
                int top = minimumArea(0, split1, 0, n, grid);
                int middle = minimumArea(split1, split2, 0, n, grid);
                int bottom = minimumArea(split2, m, 0, n, grid);

                result = min(result, top + middle + bottom);
            }
        }

        return result;
    }

public:
    int minimumSum(vector<vector<int>>& grid) {
        int result = helper(grid);
        vector<vector<int>> rotatedGrid = rotateClockWise(grid);
        result = min(result, helper(rotatedGrid));
        return result;
    }
};