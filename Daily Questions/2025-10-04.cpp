#include <vector>
using namespace std;
class Solution {
public:
    int maxArea(vector<int>& height) {
        int n=height.size();
        int maxm=0;
        int p1=0,p2=n-1;
        while(p1<p2){
            int a=height[p1];
            int b=height[p2];
            int j=min(a,b)*(p2-p1);
            maxm=max(maxm,j);
            if(height[p2]<=height[p1]){
                p2--;
            }
            else{
                p1++;
            }
        }
        return maxm;
    }
};