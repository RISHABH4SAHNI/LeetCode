#include <vector>
#include <queue>
using namespace std;

class Solution {
public:

    double gain(int pass, int total) {
        double before = (double)pass / total;
        double after = (double)(pass + 1) / (total + 1);
        return after - before;
    }

    double maxAverageRatio(vector<vector<int>>& classes, int extraStudents) {
        int n = classes.size();

        priority_queue<pair<double, pair<int,int>>> pq;

        for(int i=0; i<n; i++){
            int pass = classes[i][0], total = classes[i][1];
            pq.push({gain(pass, total), {pass, total}});
        }

        while(extraStudents > 0){
            auto top = pq.top();
            pq.pop();

            int pass = top.second.first;
            int total = top.second.second;

            pass++;
            total++;

            pq.push({gain(pass, total), {pass, total}});
            extraStudents--;
        }

        double mean_sum = 0.0;
        while(!pq.empty()){
            auto top = pq.top();
            pq.pop();
            int pass = top.second.first;
            int total = top.second.second;
            mean_sum += (double)pass / total;
        }

        return mean_sum / n;
    }
};
