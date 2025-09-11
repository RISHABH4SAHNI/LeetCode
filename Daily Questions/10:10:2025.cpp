#include <vector>
#include <unordered_set>
#include <climits>
using namespace std;

class Solution {
public:
    int minimumTeachings(int n, vector<vector<int>>& languages, vector<vector<int>>& friendships) {
        int m = languages.size();
        vector<unordered_set<int>> know(m);
        for (int i = 0; i < m; i++) {
            for (int lang : languages[i]) {
                know[i].insert(lang);
            }
        }

        unordered_set<int> needTeaching;
        for (auto &f : friendships) {
            int u = f[0] - 1, v = f[1] - 1;
            bool ok = false;
            for (int lang : know[u]) {
                if (know[v].count(lang)) {
                    ok = true;
                    break;
                }
            }
            if (!ok) {
                needTeaching.insert(u);
                needTeaching.insert(v);
            }
        }

        if (needTeaching.empty()) return 0;

        int ans = INT_MAX;
        for (int lang = 1; lang <= n; lang++) {
            int cnt = 0;
            for (int person : needTeaching) {
                if (!know[person].count(lang)) cnt++;
            }
            ans = min(ans, cnt);
        }

        return ans;
    }
};
