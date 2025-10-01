#include <vector>
using namespace std;

class Solution {
public:
    vector<int> sumZero(int n) {
        vector<int> result;
        if(n%2==1){
            result.push_back(0);
        }
        int element = 1;
        n=n/2;
        while(n>0){
            result.push_back(element);
            result.push_back(element*(-1));
            element++;
            n--;
        }
        return result;
    }
};