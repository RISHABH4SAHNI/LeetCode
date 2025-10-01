#include <iostream>
#include <vector>  
#include <map>
#include <set>
using namespace std;

class TaskManager {
public:
    map<int, pair<int, int>> mp;          // taskId -> {userId, priority}
    set<pair<int, int>> st;              // {priority, taskId}

    TaskManager(vector<vector<int>>& tasks) {
        for (auto it : tasks) {
            st.insert({it[2], it[1]});    // priority, taskId
            mp[it[1]] = {it[0], it[2]};  // taskId -> {userId, priority}
        }
    }
    
    void add(int userId, int taskId, int priority) {
        st.insert({priority, taskId});
        mp[taskId] = {userId, priority};
    }
    
    void edit(int taskId, int newPriority) {
        pair<int, int> p = mp[taskId];     // {userId, priority}
        st.erase({p.second, taskId});      // remove old {priority, taskId}
        st.insert({newPriority, taskId});  // insert new {priority, taskId}
        mp[taskId] = {p.first, newPriority};
    }
    
    void rmv(int taskId) {
        pair<int, int> p = mp[taskId];     // {userId, priority}
        st.erase({p.second, taskId});      // remove from set
        mp.erase(taskId);                  // remove from map
    }
    
    int execTop() {
        if (mp.empty()) return -1;
        auto it = st.end();
        it--;                              // highest priority element
        pair<int, int> p = *it;
        int ans = mp[p.second].first;      // userId
        mp.erase(p.second);                // remove from map
        st.erase(it);                      // remove from set
        return ans;
    }
};