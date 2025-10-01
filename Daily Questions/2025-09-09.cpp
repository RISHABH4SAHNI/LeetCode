#include <vector>
using namespace std;

class Solution {
public:
    int peopleAwareOfSecret(int n, int delay, int forget) {
        const int mod = 1e9 + 7;
        vector<long long> dp(n + 1, 0);
        dp[1] = 1;
        long long total = 0;
        for (int i = 2; i <= n; i++){
            if (i - delay > 0){
                total = (total + dp[i - delay] + mod) % mod;
            }
            if (i - forget > 0){
                total = (total - dp[i - forget] + mod) % mod;
            }
            dp[i] = total;
        }
        long long res = 0;
        for (int i = n - forget + 1; i <= n; i++){
            res = (res + dp[i]) % mod;
        }
        return (int)res;
    }
};