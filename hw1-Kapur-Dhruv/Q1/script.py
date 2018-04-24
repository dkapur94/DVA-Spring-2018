import csv
import json
import time
import tweepy


# You must use Python 2.7.x

# 1 point
def loadKeys(key_file):
    jsonkey=open(key_file)
    json_key = json.load(jsonkey)
    api_key = json_key['api_key']
    api_secret = json_key['api_secret']
    token = json_key['token']
    token_secret = json_key['token_secret']
    return api_key,api_secret,token,token_secret
    print api_key,api_secret,token,token_secret
# 4 points

def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    #Add code here to populate primary_friends
    user = api.get_user(root_user,count = no_of_friends)

    for user in user.friends():
         #print (root_user,user.screen_name)
         #print(root_user,user.screen_name.decode('unicode_escape').encode('ascii','ignore'))
         primary_friends.append([root_user,str(user.screen_name)])


    
    
    return primary_friends
    

# 4 points
def getNextLevelFriends(api, users_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each user in users_list
    # rtype: list containing entries in the form of a tuple (user, friend)
    next_level_friends = []
    # Add code here to populate next_level_friends
    #print  users_list
    for i in range(len(users_list)):
        
        next_user_friend = api.get_user(users_list[i])
        
        for next_user_friend in next_user_friend.friends():
            #print (root_user,user.screen_name)
            #print(users_list[i],next_user_friend.screen_name.decode('unicode_escape').encode('ascii','ignore'))
            next_level_friends.append([users_list[i],str(next_user_friend.screen_name)])


    


    


    
    return next_level_friends

# 4 points
def getNextLevelFollowers(api, users_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each user in users_list
    # rtype: list containing entries in the form of a tuple (follower, user)    
    next_level_followers = []
    # Add code here to populate next_level_followers
     
    for i in range(len(users_list)):
        
        next_user_followers = api.get_user(users_list[i],count = no_of_followers)
        
        for next_user_followers in next_user_followers.followers():
            #print (root_user,user.screen_name)
            print(users_list[i],next_user_followers.screen_name.decode('unicode_escape').encode('ascii','ignore'))
            next_level_followers.append([str(next_user_followers.screen_name),users_list[i]])




    return next_level_followers

# 3 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the 
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends. 
    all_edges = [] 
    #Add code here to populate all_edges
    
    api.wait_on_rate_limit = True
    primary_friends = getPrimaryFriends(api,root_user,no_of_neighbours)
    nextusers = [x[1] for x in primary_friends] 
    next_level_friends = getNextLevelFriends(api,nextusers,no_of_neighbours)
    next_level_followers = getNextLevelFollowers(api,nextusers,no_of_neighbours)
    all_edges = primary_friends+next_level_friends+next_level_followers
    return all_edges


# 2 points
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    with open(output_file,"w") as output:
    
      writer = csv.writer(output,lineterminator = '\n')
      writer.writerows(data)
    
    pass




"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposess
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 3
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)
    print api_key,api_secret,token,token_secret
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)

    writeToFile(edges, OUTPUT_FILE_GRAPH)
    

if __name__ == '__main__':
    testSubmission()

