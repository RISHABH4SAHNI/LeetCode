#include <iostream>
#include <vector>   
#include <numeric>      
#include <algorithm>        
using namespace std;
class Solution {
public:
    int numWaterBottles(int numBottles, int numExchange) {
        int total = 0;
        while(numBottles>=numExchange){
            total+=numExchange;
            numBottles = numBottles-numExchange+1;
        }
        total+=numBottles;
        return total;
    }
};