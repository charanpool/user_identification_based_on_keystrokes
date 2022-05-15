__author__ = 'tchauhan'
import pandas as pd
import collections

result_user = "None"

def authenticate_user():
    global result_user1
    global result_user2
    global result_user3
    global tieFlag
    print("Authentication")
    d = collections.defaultdict(dict)
    #print("check 1:",d)
    diff = {}
    count = collections.defaultdict(dict)
    frequentAlphabetsList = ['e', 'a', 'r', 'i', 't', 'n', 's', 'h', 'l','d','g','space','in','th','ti','on','an','he',\
                             'al','er','es','the','and','are','ion','ing','in_DD','th_DD','ti_DD','on_DD','an_DD','he_DD',\
                             'al_DD','er_DD','es_DD','input_rate']
    registerd_data = pd.read_csv("reg_dataset.csv")
    reg_user_names = list(registerd_data['name'])
    #print(reg_user_names)
    authenticate_data = pd.read_csv("auth_dataset.csv")
    #print("check 2:",authenticate_data)
    #print(authenticate_data.loc[0,'a'])
    for i, user in enumerate(reg_user_names):
        #print(user)
        user_id = str(user).split("_")[0]
        print(user_id)
        for alpha in frequentAlphabetsList:
            if alpha not in d[user_id]:
                d[user_id][alpha] = 0
            d[user_id][alpha] += registerd_data[alpha][i]

    for user in d.keys():
        #print("check 3:",user)
        for alpha in d[user].keys():
            d[user][alpha]/=3   # /=2 is changed to /=3 because 3 paragraphs are there.
    print("total dictionary:",d)

    for alpha in frequentAlphabetsList:
        for reg_user in enumerate(d):
            diff[reg_user[1]] = (abs(d[reg_user[1]][alpha] - authenticate_data.loc[0,alpha]))
        sorted_dict = sorted(diff.values())
        #first = sorted_dict[0]
        #print(first)
        #if diff != 0:
        for name , differ in diff.items():
            if sorted_dict[0] == differ:
                person = name
        #print(diff[first])
                if person not in count.keys():
                    count[person] = 0
                count[person] +=  1
        print(count)

    max_count = 0
    for key in count.keys():
        if(count[key] > max_count):
            result_user1 = key
            max_count = count[key]

    tempResKeys = []
    for key in count.keys():
        if(count[key] == count[result_user1]):
            tempResKeys.append(key)

    if(len(tempResKeys) == 1):
        tieFlag = 0

    if(len(tempResKeys) == 2):
        result_user2 = tempResKeys[1]
        tieFlag = 1

    if(len(tempResKeys) == 3):
        result_user2 = tempResKeys[1]
        result_user3 = tempResKeys[2]
        tieFlag = 2


if __name__ == "__main__":
    authenticate_user()
