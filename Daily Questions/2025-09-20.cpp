#include <iostream>
#include <queue>
#include <unordered_set>
#include <unordered_map>
#include <vector>
#include <algorithm>    
using namespace std;
struct Packet {
    int source, destination, timestamp;
};

class Router {
    int limit;
    queue<Packet> router;
    unordered_set<string> hash;
    unordered_map<int, vector<int>> destMap;

    string key(const Packet& p) {
        return to_string(p.source) + "#" + to_string(p.destination) + "#" + to_string(p.timestamp);
    }

public:
    Router(int memoryLimit){
        limit = memoryLimit;
    }

    bool addPacket(int source, int destination, int timestamp) {
        Packet packet{source, destination, timestamp};
        string k = key(packet);
        if (hash.count(k)) return false;

        if (router.size() == limit) {
            Packet oldPacket = router.front(); router.pop();
            hash.erase(key(oldPacket));

            auto& vec = destMap[oldPacket.destination];
            vec.erase(vec.begin());
        }

        router.push(packet);
        hash.insert(k);
        destMap[destination].push_back(timestamp);
        return true;
    }

    vector<int> forwardPacket() {
        if (router.empty()) return {};
        Packet packet = router.front(); router.pop();
        hash.erase(key(packet));

        auto& vec = destMap[packet.destination];
        vec.erase(vec.begin());
        return {packet.source, packet.destination, packet.timestamp};
    }

    int getCount(int destination, int startTime, int endTime) {
        if (destMap.find(destination) == destMap.end()) return 0;
        const auto& vec = destMap[destination];

        auto lb = lower_bound(vec.begin(), vec.end(), startTime);
        auto ub = upper_bound(vec.begin(), vec.end(), endTime);

        return distance(lb, ub);
    }
};