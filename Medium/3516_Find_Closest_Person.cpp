#include <cmath>

class Solution {
public:
    int findClosest(int x, int y, int z) {
        int x_time = abs(z-x);
        int y_time = abs(z-y);
        if(x_time<y_time){
            return 1;
        }
        if(x_time>y_time){
            return 2;
        }
        return 0;
    }
};