from user import User
from utils import distance_km

def cp2_1_simple_inference(dictUsers):
    dictUsersInferred = dict()  # dict to return, store inferred results here
    # you should keep everything in dictUsers as is / read-only
    
    # Going through each user
    for user in dictUsers.values():
        if user.home_shared == 1:  # User shared location
            dictUsersInferred[user.id] = User(user.id, user.home_lat, user.home_lon, user.home_shared)  # Keeping original values
        else:  # User did not share location
            # Checking for friends with shared location
            friends_who_shared_location = set()

            for friend in user.friends:
                if dictUsers[friend].home_shared == 1:
                    friends_who_shared_location.add(dictUsers[friend])

            if len(friends_who_shared_location) == 0:  # No friends have shared location so no inference can be made
                dictUsersInferred[user.id] = User(user.id, user.home_lat, user.home_lon, user.home_shared)  # Keeping original values
            else:  # can use inference to decide user location based on friends location
                total_lat = 0
                total_lon = 0

                for friend in friends_who_shared_location:
                    total_lat += friend.home_lat
                    total_lon += friend.home_lon

                centroid_lat = total_lat / len(friends_who_shared_location)
                centroid_lon = total_lon / len(friends_who_shared_location)

                dictUsersInferred[user.id] = User(user.id, centroid_lat, centroid_lon, user.home_shared)

    return dictUsersInferred


# everything after this is until the accuracy function is for cp2_2_improved_inference function
import copy
import numpy as np

# Used in cp2_2_improved_inference to calculate distance between locations
def haversine_distance(coord1, coord2):
    # Using Haversine distance between two coordinates since it is meant for spheres and long and lat coordinates
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Use numpy for radians
    lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    # Computing distance between coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Applying Haversine formula
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # Calculating distance and returning it
    distance = R * c
    return distance

# K-means functions which will be used for clustering
def initialize_centroids(X, k):
    return X[np.random.choice(X.shape[0], k, replace=False)]

def assign_clusters(X, centroids):
    distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
    return np.argmin(distances, axis=1)

def update_centroids(X, labels, k):
    return np.array([X[labels == i].mean(axis=0) for i in range(k)])

def kmeans(X, k, max_iters=100):
    centroids = initialize_centroids(X, k)
    for _ in range(max_iters):
        labels = assign_clusters(X, centroids)
        new_centroids = update_centroids(X, labels, k)
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    return centroids, labels

# Used friends of friends, clustering, weighted average and better distance calculation for better inferencing
def cp2_2_improved_inference(dictUsers1):
    dictUsers = copy.deepcopy(dictUsers1)  # Making a deep copy of the dictionary
    dictUsersInferred = dict()

    # Masking locations of users who are not sharing location
    for user in dictUsers.values():
        if user.home_shared == 0:
            user.home_lat = -999
            user.home_lon = -999

    # Going through each user
    for user in dictUsers.values():
        if user.home_shared == 1:  # User shared location, so no inference needed
            dictUsersInferred[user.id] = User(user.id, user.home_lat, user.home_lon, user.home_shared)  # Keeping original values
        else:
            friends_who_shared_location = set()

            # Store friends who shared locations
            for friend in user.friends:
                if dictUsers[friend].home_shared == 1:
                    friends_who_shared_location.add(dictUsers[friend])

            # If no direct friends have location shared, store friends of friends who shared locations
            if len(friends_who_shared_location) == 0:
                friends_of_friends_who_shared_location = set()

                for user_direct_friend in user.friends:
                    user_friend = dictUsers[user_direct_friend]
                    for user_friend_friend in user_friend.friends:
                        if dictUsers[user_friend_friend].home_shared == 1:
                            friends_of_friends_who_shared_location.add(dictUsers[user_friend_friend])

                friends_who_shared_location = friends_of_friends_who_shared_location  # To reduce redundant code later

            # No friends or friends of friends have shared location so no inference can be made
            if len(friends_who_shared_location) == 0:
                dictUsersInferred[user.id] = User(user.id, user.home_lat, user.home_lon, user.home_shared)
            else:  # Can use inference to decide user location based on friends location
                friends_lat_lon = np.array([(friend.home_lat, friend.home_lon) for friend in friends_who_shared_location])

                # Performing K-means clustering on friends locations
                if len(friends_lat_lon) >= 3:  # At least 3 points for clustering
                    k = min(3, len(friends_lat_lon))  # Setting k as 3 or fewer if there are not enough friends
                    centroids, labels = kmeans(friends_lat_lon, k)

                    # Choosing the largest cluster centroid as the inferred location
                    largest_cluster = np.argmax([np.sum(labels == i) for i in range(k)])
                    centroid_lat, centroid_lon = centroids[largest_cluster]
                else:
                    # Using weighted average if K-means won't work as well
                    total_lat = 0
                    total_lon = 0
                    total_weight = 0

                    # Going throgh friends to calculate weights to infer user location
                    for friend in friends_who_shared_location:
                        distance = haversine_distance((user.home_lat, user.home_lon), (friend.home_lat, friend.home_lon))
                        distance_weight = np.exp(-distance / 50)  # More influence if closer

                        shared_friends_count = sum(1 for f in user.friends if f in friend.friends)
                        weight = (shared_friends_count + 1) * distance_weight  # Combining distance and shared friends to get weight

                        total_lat += friend.home_lat * weight
                        total_lon += friend.home_lon * weight
                        total_weight += weight

                    centroid_lat = total_lat / total_weight if total_weight > 0 else user.home_lat
                    centroid_lon = total_lon / total_weight if total_weight > 0 else user.home_lon

                dictUsersInferred[user.id] = User(user.id, centroid_lat, centroid_lon, user.home_shared)

    return dictUsersInferred


def cp2_calc_accuracy(truth_dict, inferred_dict):
    # distance_km(a,b): return distance between a and be in km
    # recommended standard: is accuate if distance to ground truth < 25km
    if len(truth_dict) != len(inferred_dict) or len(truth_dict)==0:
        return 0.0
    sum = 0
    for i in truth_dict:
        if truth_dict[i].home_shared:
            sum += 1
        elif truth_dict[i].latlon_valid() and inferred_dict[i].latlon_valid():
            if distance_km(truth_dict[i].home_lat, truth_dict[i].home_lon, inferred_dict[i].home_lat,
                           inferred_dict[i].home_lon) < 25.0:
                sum += 1
    return sum * 1.0 / len(truth_dict)

# for testing
# from cp1 import cp1_1_parse_homes, cp1_2_parse_friends
# from cp2 import cp2_1_simple_inference, cp2_calc_accuracy
# from utils import distance_km
# if __name__ == "__main__":
#     homes_file = "dataset1/homes.txt"
#     friends_file = "dataset1/friends.txt"
#     users_dict = cp1_1_parse_homes(homes_file)
#     cp1_2_parse_friends(friends_file, users_dict)
#     dict_users_inferred = cp2_1_simple_inference(users_dict)
#     # Step 3: Calculate the accuracy of the inference algorithm
#     accuracy = cp2_calc_accuracy(users_dict, dict_users_inferred)
#     print(f"Inference accuracy: {accuracy * 100:.2f}%")
#     inferred_dict = cp2_2_improved_inference(users_dict)
#     accuracy = cp2_calc_accuracy(users_dict, inferred_dict)
#     print("Improved Inference Accuracy:", accuracy)