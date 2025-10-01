#include <iostream>
#include <unordered_map>
#include <string>
#include <cctype>
using namespace std;

class Spreadsheet {
public:
    unordered_map<string,int> sheet;
    Spreadsheet(int rows) {

    }
    
    void setCell(string cell, int value) {
        sheet[cell] = value;
    }
    
    void resetCell(string cell) {
        sheet[cell] = 0;
    }
    
    int getValue(string formula) {
        int idx = formula.find('+');
        string left = formula.substr(1, idx - 1);
        string right = formula.substr(idx + 1);

        int valLeft = 
            isalpha(left[0]) 
            ? (sheet.count(left) ? sheet[left] : 0) 
            : stoi(left);

        int valRight = 
            isalpha(right[0]) 
            ? (sheet.count(right) ? sheet[right] : 0) 
            : stoi(right);

        return valLeft + valRight;
    }
};

/**
 * Your Spreadsheet object will be instantiated and called as such:
 * Spreadsheet* obj = new Spreadsheet(rows);
 * obj->setCell(cell,value);
 * obj->resetCell(cell);
 * int param_3 = obj->getValue(formula);
 */