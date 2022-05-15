import threading
import time
from pynput.keyboard import Key, Listener
import csv
import authenticate
import sys
import statistics
#from authenticate import authenticate_user

frequentAlphabetsList = ['e', 'a', 'r', 'i','o','t', 'n', 's', 'h', 'l','d','g','space']
frequentAlphabets = {
                        'e': [],
                        'a': [],
                        'r': [],
                        'i': [],
                        'o': [],
                        't': [],
                        'n': [],
                        's': [],
                        'h': [],
                        'l': [],
                        'd': [],
                        'g': [],
                        'space':[]
                    }

frequentDiagraphList = ['in', 'th', 'ti','on','an', 'he', 'al', 'er','es']
frequentDiagraph = {
                    'in': [],
                    'th': [],
                    'ti': [],
                    'on': [],
                    'an': [],
                    'he': [],
                    'al': [],
                    'er': [],
                    'es': []
                    }
frequentDiagraph_DD = {
                    'in_DD': [],
                    'th_DD': [],
                    'ti_DD': [],
                    'on_DD': [],
                    'an_DD': [],
                    'he_DD': [],
                    'al_DD': [],
                    'er_DD': [],
                    'es_DD': []
    }
frequentDiagraph_UD = {
                    'in_UD': [],
                    'th_UD': [],
                    'ti_UD': [],
                    'on_UD': [],
                    'an_UD': [],
                    'he_UD': [],
                    'al_UD': [],
                    'er_UD': [],
                    'es_UD': []
    }
frequentTrigraphList = ['the','and','are','ion','ing']

frequentTrigraphs = {
                    'the': [],
                    'and': [],
                    'are': [],
                    'ion': [],
                    'ing': []
}
depressedTime = []
releaseTime = []
keycodeList = []
start_typing = []
last_type = []

row = ['name', 'e', 'a', 'r', 'i', 'o', 't', 'n', 's', 'h', 'l','d','g','space','in', 'th', 'ti', 'on', 'an', 'he', 'al', 'er','es','the',\
       'and','are','ion','ing','in_DD','th_DD','ti_DD','on_DD','an_DD','he_DD','al_DD','er_DD','es_DD','input_rate']

'''
Creating the dataset by appending to the CSV file
'''
def append_to_csv(user_rep, registration,input_ratio):
    mean = []
    mean.append(user_rep)
    std_dev =[]
    std_dev.append(user_rep)
    for key in frequentAlphabetsList:
        print(key)
        sum = 0.0
        count = 0
        try:
            for i, k in enumerate(frequentAlphabets[key]):
                print(k)
                rTime = k[1] - k[0]
                sum += rTime
                count += 1
            mean.append(sum/count)
        except BaseException as e:
            mean.append(0.0)
            print("key does not occur")
    print(mean)
    '''
    for key in frequentAlphabetsList:
        print(key)
        count = 1
        sum = 0.0
        try:
            rTime_list = []
            #print("debugging")
            for i, k in enumerate(frequentAlphabets[key]):
                #print("to know error:",k)
                #print("std dev started")
                rTime = k[1] - k[0]
                rTime_list.append(rTime)
                #print("rtime list error:",rTime_list)
                #print("debug2:",type(rTime))
                #print("debug0:",type(mean[i+1]))
            #    sum += ((rTime - mean[i+1])*(rTime - mean[i+1]))
                #print("sum is :",sum)
            #    count +=1
            #    i = i+1
            #    print(sum , count)
            #std_dev.append(math.sqrt(sum/(count-1)))
            std_dev.append((statistics.stdev(rTime_list)))
            #print("std_dev for key", std_dev)
            #print("debug1:",type(rTime))
        except BaseException as e:
           print(e)
           std_dev.append(0.0)
           print("key does not occur : ", key)
    #print("std dev not working")
    print("alpha: ", std_dev)
    print(std_dev)
    '''
    for key in frequentDiagraphList:
        sum = 0.0
        count = 0
        try:
            for i, k in enumerate(frequentDiagraph[key]):
                print(k)
                rTime = k[1] - k[0]
                print("release time :",rTime)
                sum += rTime
                count += 1
            mean.append(sum/count)
        except BaseException as e:
            mean.append(0.0)
    #mean.append(input_ratio)
    '''
    for key in frequentDiagraphList:
        count = 1
        sum = 0.0
        try:
            rTime_list = []
            for i, k in enumerate(frequentDiagraph[key]):
                rTime = k[1] - k[0]
                #sum += ((rTime - mean[i+1])*(rTime - mean[i+1]))
                #count +=1
           # std_dev.append(math.sqrt(sum)/count)
                #i = i+1
                rTime_list.append(rTime)
            std_dev.append((statistics.stdev(rTime_list)))
            #    print(sum , count)
            #std_dev.append(math.sqrt(sum/(count-1)))
        except BaseException as e:
           std_dev.append(0.0)
           print("key does not occur")
    #print("std dev not working")
    print("diagraph ---",std_dev)
    '''
    for key in frequentTrigraphList:
        #print("checking tri:" , key)
        sum = 0.0
        count = 0
        try:
            #print("trigraph:", frequentTrigraphs[key])
            for i, k in enumerate(frequentTrigraphs[key]):
                #print(k)
                rTime = k[1] - k[0]
                #print("release time :",rTime)
                sum += rTime
                count += 1
            mean.append(sum/count)
        except BaseException as e:
            mean.append(0.0)
    #print("debugging 0:",frequentDiagraph_DD)
    for key in frequentDiagraphList:
        sum = 0.0
        count = 0
        key = key + "_DD"
        try:
            for i, k in enumerate(frequentDiagraph_DD[key]):
                #print(k)
                rTime = k[1] - k[0]
                #print("release time :",rTime)
                sum += rTime
                count += 1
            #print("down down 2:",key)
            mean.append(sum/count)
        except BaseException as e:
            mean.append(0.0)

    '''
    for key in frequentDiagraphList:
        sum = 0.0
        count = 0
        key = key + "_UD"
        try:
            for i, k in enumerate(frequentDiagraph_UD[key]):
                print(k)
                rTime = k[1] - k[0]
                print("release time :",rTime)
                sum += rTime
                count += 1
            print("up down 2:",key)
            mean.append(sum/count)
        except BaseException as e:
            mean.append(0.0)
    '''
    mean.append(input_ratio)

    if registration:
        csv_file = "reg_dataset.csv"
        mode = "a"
    else:
        csv_file = "auth_dataset.csv"
        mode = "w"

    with open(csv_file, mode,newline='\n') as data:
        writer = csv.writer(data)
        if not registration:
            writer.writerow(row)
        #print("mean is:",mean)
        #mean.append(input_ratio)
        writer.writerow(mean)

'''
def input_rate (key, depressedTime, releaseTime):
    if key == Key.esc:
        total_typ_time = releaseTime[-1] - depressedTime[0]
    input_ratio = total_typ_time / len(releaseTime)
    print("ratio:", input_rate)
'''

def create_diagraph(p, r, k):
    frequentAlphabetCount = {'e':0, 'a':0, 'r':0, 'i':0, 'o':0, 't':0, 'n':0, 's':0, 'h':0, 'l':0}
    #print(p, r, k)
    #print(k)
    #print("create diagraph")
    for i, key in enumerate(k):
        try:
            frequentAlphabetCount[key.char] = frequentAlphabetCount.get(key.char) + 1
            twoKeys = key.char + k[i+1].char
            #print("Two keys",twoKeys, key, k[i+1])
            index_0 = frequentAlphabetCount.get(key.char)
            index_1 = frequentAlphabetCount.get(k[i+1].char)
            #print("index : ",index_0, index_1)
            #print("------",frequentAlphabets[key.char][index_0-1][0], frequentAlphabets[k[i+1].char][index_1-1][1])
            frequentDiagraph[twoKeys].append((frequentAlphabets[key.char][index_0-1][0], frequentAlphabets[k[i+1].char][index_1][1]))
        except BaseException as e:
            #print(e)
            pass

def create_diagraph_DD(p, r, k):
    frequentAlphabetCount = {'e':0, 'a':0, 'r':0, 'i':0, 'o':0, 't':0, 'n':0, 's':0, 'h':0, 'l':0}
    #print(p, r, k)
    #print(k)
    #print("create diagraph_DD")
    for i, key in enumerate(k):
        try:
            frequentAlphabetCount[key.char] = frequentAlphabetCount.get(key.char) + 1
            twoKeys = key.char + k[i+1].char + "_DD"
            #print("Two keys",twoKeys, key, k[i+1])
            index_0 = frequentAlphabetCount.get(key.char)
            index_1 = frequentAlphabetCount.get(k[i+1].char)
            #print("index : ",index_0, index_1)
            #print("------",frequentAlphabets[key.char][index_0-1][0], frequentAlphabets[k[i+1].char][index_1-1][0])
            frequentDiagraph_DD[twoKeys].append((frequentAlphabets[key.char][index_0-1][0], frequentAlphabets[k[i+1].char][index_1][0]))
        except BaseException as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)

def create_diagraph_UD(p, r, k):
    frequentAlphabetCount = {'e':0, 'a':0, 'r':0, 'i':0, 'o':0, 't':0, 'n':0, 's':0, 'h':0, 'l':0}
    #print(p, r, k)
    print(k)
    print("create diagraph_UD")
    for i, key in enumerate(k):
        try:
            frequentAlphabetCount[key.char] = frequentAlphabetCount.get(key.char) + 1
            twoKeys = key.char + k[i+1].char + "_UD"
            print("Two keys",twoKeys, key, k[i+1])
            index_0 = frequentAlphabetCount.get(key.char)
            index_1 = frequentAlphabetCount.get(k[i+1].char)
            print("index : ",index_0, index_1)
            print("------",frequentAlphabets[key.char][index_0-1][1], frequentAlphabets[k[i+1].char][index_1-1][0])
            frequentDiagraph_UD[twoKeys].append((frequentAlphabets[key.char][index_0-1][1], frequentAlphabets[k[i+1].char][index_1][0]))
        except BaseException as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)

def create_trigraph(p, r, k):
    frequentAlphabetCount = {'e':0, 'a':0, 'r':0, 'i':0, 'o':0, 't':0, 'n':0, 's':0, 'h':0, 'l':0, 'd':0, 'g':0}
    #print(p, r, k)
    #print(k)
    #print("create trigraph")
    for i, key in enumerate(k):
        try:
            frequentAlphabetCount[key.char] = frequentAlphabetCount.get(key.char) + 1
            threeKeys = key.char + k[i+1].char + k[i+2].char
            #print("Three keys",threeKeys, key, k[i+2])
            index_0 = frequentAlphabetCount.get(key.char)
            index_1 = frequentAlphabetCount.get(k[i+2].char)
            #print("index : ",index_0, index_1)
            #print("------",frequentAlphabets[key.char][index_0-1][0])
            #print("11111",frequentAlphabets[k[i+2].char][index_1][1])
            frequentTrigraphs[threeKeys].append((frequentAlphabets[key.char][index_0-1][0], frequentAlphabets[k[i+2].char][index_1][1]))
        except BaseException as e:
            #print(key,e)
            pass

def on_press(key):
    try:
        #global start_typing
        #start_typing=[]
        #global started
        #started = start_typing[0]
        start_typing.append(time.time())
        #if (key.char or Key.space or Key.enter) in para1:
            #print(key)
        global start
            #start_typing = []
        start = time.time()
            #if (keycodeList == list()):
            #start_typing.append(start)
            #print("to know start time:", start)
            #frequentAlphabets[key.char].append(time.time())
        depressedTime.append(time.time())
        keycodeList.append(key)
    except BaseException as e:
        #print(key)
        if (Key.space):
            start = time.time()
            keycodeList.append(key)
        depressedTime.append(time.time())


last_type = []

def on_release(key):
    if key == Key.esc:
        global input_ratio
        total_typ_time = last_type[-1] - start_typing[0]
        input_ratio = total_typ_time / (len(last_type))
        #print("length , total_time:",(len(last_type)-1),total_typ_time)
        #print("start,last list:", start_typing,last_type)
        return False
    try:
        #last_type = []
        last_type.append(time.time())
        #last = last_type[-1]
        #length = len(last_type)
        #if key == Key.esc:
        #if key.char in para1:
        frequentAlphabets[key.char].append((start,time.time()))
        releaseTime.append(time.time())
            #keycodeList.append(key)
    except BaseException as e:
        releaseTime.append(time.time())
        if (Key.space):
           frequentAlphabets['space'].append((start,time.time()))
        #if(Key.enter):
        #   frequentAlphabets['enter'].append((start,time.time()))

def run():
        #user_rep = user + "_" + str(para_count)
        global user_rep
        global registration
        #print(registration,"  ", user_rep)
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        #print(frequentAlphabets)
        create_diagraph(depressedTime, releaseTime, keycodeList)
        create_diagraph_DD(depressedTime, releaseTime, keycodeList)
        #create_diagraph_UD(depressedTime, releaseTime, keycodeList)
        create_trigraph(depressedTime, releaseTime, keycodeList)
        #print(frequentDiagraph)
        append_to_csv(user_rep, registration,input_ratio)

        for key in frequentAlphabets.keys():
            frequentAlphabets[key].clear()
        for key in frequentDiagraph.keys():
            frequentDiagraph[key].clear()
        for key in frequentDiagraph_DD.keys():
            frequentDiagraph_DD[key].clear()
        for key in frequentTrigraphs.keys():
            frequentTrigraphs[key].clear()
        keycodeList.clear()
        #print("alpha",frequentAlphabets)
        #print("digraph",frequentDiagraph)
        if not registration:
            authenticate.authenticate_user()
        #para -= 1
        #para_count += 1

registration = True
user_rep = None
#main_thread = threading.Thread(target=run)



#if __name__ == "__main__":
    #registration = True

#run(registration,user)
#if not registration:
    #authenticate_user()