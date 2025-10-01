#include <string>
using namespace std;
class Solution {
public:
    bool doesAliceWin(string s) {
        int cnt = 0;
        for(char c :s){
            if(c=='a'||c=='e'||c=='i'||c=='o'||c=='u'){
                cnt++;
            }
        }
        if(cnt>0){
            return true;
        }
        return false;
    }
};