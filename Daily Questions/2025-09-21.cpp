#include <vector>
#include <map>
#include <set>
#include <tuple>
#include <algorithm>

using namespace std;

class MovieRentingSystem {
private:
    // Maps movie ID to a sorted set of {price, shop} pairs for available movies.
    map<int, set<pair<int, int>>> available_movies;

    // A sorted set of {price, shop, movie} tuples for all rented movies.
    set<tuple<int, int, int>> rented_movies;

    // Maps {shop, movie} pair to its price for quick lookups.
    map<pair<int, int>, int> prices;

public:
    /**
     * @brief Initializes the system with shops and movie entries.
     */
    MovieRentingSystem(int n, vector<vector<int>>& entries) {
        for (const auto& entry : entries) {
            int shop = entry[0];
            int movie = entry[1];
            int price = entry[2];

            prices[{shop, movie}] = price;
            available_movies[movie].insert({price, shop});
        }
    }

    /**
     * @brief Finds the cheapest 5 shops for an unrented movie.
     */
    vector<int> search(int movie) {
        vector<int> result;
        if (available_movies.count(movie)) {
            auto& shops = available_movies.at(movie);
            int count = 0;
            for (const auto& p : shops) {
                if (count >= 5) break;
                result.push_back(p.second); // p.second is shop_id
                count++;
            }
        }
        return result;
    }

    /**
     * @brief Rents a movie from a specific shop.
     */
    void rent(int shop, int movie) {
        int price = prices.at({shop, movie});
        
        // Move from available to rented
        available_movies.at(movie).erase({price, shop});
        rented_movies.insert({price, shop, movie});
    }

    /**
     * @brief Drops off a rented movie at a shop.
     */
    void drop(int shop, int movie) {
        int price = prices.at({shop, movie});

        // Move from rented back to available
        rented_movies.erase({price, shop, movie});
        available_movies.at(movie).insert({price, shop});
    }

    /**
     * @brief Reports the cheapest 5 rented movies.
     */
    vector<vector<int>> report() {
        vector<vector<int>> result;
        int count = 0;
        for (const auto& t : rented_movies) {
            if (count >= 5) break;
            // Report contains {shop, movie}
            result.push_back({get<1>(t), get<2>(t)});
            count++;
        }
        return result;
    }
};