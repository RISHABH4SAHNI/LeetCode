#include <vector>
using namespace std;

class Solution {
public:
    bool isValid(char k, vector<vector<char>>& board, int i, int j) {
        for (int ii = 0; ii < 9; ii++) {
            if (ii != i && board[ii][j] == k) return false;
        }
        for (int ji = 0; ji < 9; ji++) {
            if (ji != j && board[i][ji] == k) return false;
        }

        int rowStart = (i / 3) * 3;
        int colStart = (j / 3) * 3;
        for (int r = rowStart; r < rowStart + 3; r++) {
            for (int c = colStart; c < colStart + 3; c++) {
                if ((r != i || c != j) && board[r][c] == k) return false;
            }
        }

        return true;
    }

    bool isValidSudoku(vector<vector<char>>& board) {
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (board[i][j] == '.') continue;
                if (!isValid(board[i][j], board, i, j)) return false;
            }
        }
        return true;
    }
};
