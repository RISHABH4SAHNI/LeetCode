#include <vector>
using namespace std;

class Solution {
public:
    bool isValid(char k, vector<vector<char>>& board, int i, int j) {
        for (int ii = 0; ii < 9; ii++) {
            if (board[ii][j] == k) return false;
        }
        for (int ji = 0; ji < 9; ji++) {
            if (board[i][ji] == k) return false;
        }

        int rowStart = (i / 3) * 3;
        int colStart = (j / 3) * 3;
        for (int r = rowStart; r < rowStart + 3; r++) {
            for (int c = colStart; c < colStart + 3; c++) {
                if (board[r][c] == k) return false;
            }
        }

        return true;
    }

    bool solve(vector<vector<char>>& board) {
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (board[i][j] != '.') continue;

                for (int k = 0; k < 9; k++) {
                    char ch = '1' + k;
                    if (isValid(ch, board, i, j)) {
                        board[i][j] = ch;
                        if (solve(board)) return true;
                        board[i][j] = '.';
                    }
                }
                return false;
            }
        }
        return true;
    }

    void solveSudoku(vector<vector<char>>& board) {
        solve(board);
    }
};
