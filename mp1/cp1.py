import csv
from logging import warn, error, debug
from user import User

## parse homes.txt
#  input:
#    f: filename
#  output:
#    a dict of all users from homes.txt with key=user_id, value=User object
def cp1_1_parse_homes(f):
    dictUsers_out = dict()
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            if len(i) == 4:  # Seeing if there is a home for user stored 
                user_id = int(i[0])
                home_lat = float(i[1])
                home_long = float(i[2])
                home_shared = int(i[3])

                userObject = User(user_id, home_lat, home_long, home_shared)  # User object

                if userObject.latlon_valid() == 0:  # Not valid location
                    userObject.home_lat = -999
                    userObject.home_lon = -999
                    userObject.home_shared = 0

                dictUsers_out[user_id] = userObject  # Storing object in dictionary
            else:  # User exists but has no home info
                user_id = int(i[0])
                home_lat = -999
                home_long = -999
                home_shared = 0

                userObject = User(user_id, home_lat, home_long, home_shared)  # User object
                dictUsers_out[user_id] = userObject  # Storing object in dictionary

    return dictUsers_out


## parse friends.txt
#  input:
#    f: filename
#    dictUsers: dictionary of users, output of cp1_1_parse_homes()
#  no output, modify dictUsers directly
def cp1_2_parse_friends(f, dictUsers):
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            if len(i) == 2:  # Making sure there is a pair of friends
                user1_id = int(i[0])
                user2_id = int(i[1])

            if user1_id in dictUsers and user2_id in dictUsers:  # Making sure both are in dict
                # Adding each other to friend set
                dictUsers[user1_id].friends.add(user2_id)  
                dictUsers[user2_id].friends.add(user1_id)

# return all answers to Checkpoint 1.3 of MP Handout in variables
# order is given in the template
def cp1_3_answers(dictUsers):
    u_cnt = 0  # 1. How many users are there in dataset 1?
    u_noloc_cnt = 0  # 2. How many users in dataset 1 have unknown locations?
    u_noloc_nofnds_cnt = 0  # 3. How many users in dataset 1 have unknown locations and no friends?
    p_b = 0  # 4. What is the baseline accuracy (pb) (accuracy of incorrectly predicting all unknown locations) for dataset 1?
    p_u1 = 0  # 5. What is the upper bound on inference accuracy (pu1) for dataset 1 if we assume that for a given user, we can correctly infer location if unknown UNLESS that user has NO friends.
    p_u2 = 0  # 6. What is the upper bound on inference accuracy (pu2) for dataset 1 if we assume that for a given user, we can correctly infer location if unknown UNLESS that user has NO friends who shared their locations.

    user_has_friends_count = 0
    user_has_shared_friends_count = 0

    for user in dictUsers.values():
        u_cnt += 1  # 1

        if user.home_shared == 0:
            u_noloc_cnt += 1  # 2

            if len(user.friends) == 0:
                u_noloc_nofnds_cnt += 1  # 3
            else:
                user_has_friends_count += 1

                if any(dictUsers[friend_id].home_shared == 1 for friend_id in user.friends):
                    user_has_shared_friends_count += 1

    p_b = (u_noloc_cnt / u_cnt)  # 4

    p_u1 = (u_cnt - u_noloc_nofnds_cnt) / u_cnt  # 5

    p_u2 = (u_cnt - (u_noloc_cnt - user_has_shared_friends_count)) / u_cnt  # 6

    # TODO: return your answers as variables in the given order
    return u_cnt, u_noloc_cnt, u_noloc_nofnds_cnt, p_b, p_u1, p_u2

# for testing
# if __name__ == "__main__":
#     homes_file = "dataset1/homes.txt"
#     friends_file = "dataset1/friends.txt"
#     users_dict = cp1_1_parse_homes(homes_file)
#     cp1_2_parse_friends(friends_file, users_dict)
#     print(cp1_3_answers(users_dict))