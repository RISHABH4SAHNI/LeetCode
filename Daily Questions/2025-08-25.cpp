#include <vector>
using namespace std;

class Solution {
public:
    vector<int> findDiagonalOrder(vector<vector<int>>& mat) {
        int n = mat.size();
        int m = mat[0].size();
        vector<int> final_arr;
        final_arr.reserve(n * m);

        int i = 0, j = 0;
        int dir = 1;

        while (final_arr.size() < n * m) {
            final_arr.push_back(mat[i][j]);

            if (dir == 1) {
                if (j == m - 1) {
                    i++;
                    dir = -1;
                } else if (i == 0) {
                    j++;
                    dir = -1;
                } else {
                    i--;
                    j++;
                }
            } 
            else {
                if (i == n - 1) {
                    j++;
                    dir = 1;
                } else if (j == 0) {
                    i++;
                    dir = 1;
                } else {
                    i++;
                    j--;
                }
            }
        }

        return final_arr;
    }
};
