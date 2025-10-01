#include <string>
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    string sortVowels(string s) {
        string t = s;
        priority_queue<char,vector<char>,greater<char>> container;
        vector<int> positions;
        for(int i=0;i<s.size();i++){
            if(s[i]=='a'|| s[i]=='e'||s[i]=='i'||s[i]=='o'||s[i]=='u'||s[i]=='A'||s[i]=='E'||s[i]=='I'||s[i]=='O'||s[i]=='U'){
                container.push(s[i]);
                positions.push_back(i);
            }
        }
        for(int i=0;i<positions.size();i++){
            t[positions[i]] = container.top();
            container.pop();
        }
        return t;
    }
};