from bs4 import BeautifulSoup
import os
import pandas as pd
import collections
import re

all_messages = []
user1_msg = []
#use the name on the instagram account, not the username. the name is directly above the bio
user1_name = "James"
user2_msg = []
user2_name = "John G"

current_directory = os.path.dirname(os.path.abspath(__file__))
files = os.listdir(current_directory)
filelist = []
for file in files:
    if file.find(".html") != -1:
         filelist.append(file)

data = {'Text': [],
        'Date': [],
        'Sender': []}
filelist = filelist[::-1]

def run(file_name):
    print("Opening file: " + file_name)
    f = open(current_directory + "\\" + file_name, encoding="utf8")
    g = open(current_directory + "\\testing.txt", "a", encoding="utf8")
    soup = BeautifulSoup(f, "html.parser")#soup object
    messages = soup.findAll("div", attrs={"class":"_3-95 _a6-p"}) #the actual content of a message
    time = soup.findAll("div", attrs={"class":"_3-94 _a6-o"}) # the timestamp of a message
    sender = soup.findAll("div", attrs={"class":"_3-95 _2pim _a6-h _a6-i"}) #sender
    print("Messages length: " + str(len(messages)))
    messages = messages[::-1]
    time = time[::-1]
    sender = sender[::-1]
    val = 0 #array index of each message
    for message in messages:
        data.get('Text').append(message.text)
        data.get('Date').append((time[val]).text)
        data.get('Sender').append((sender[val]).text)
        if (sender[val].text == user1_name):
            user1_msg.append(message.text)
        else:
            user2_msg.append(message.text)
        all_messages.append(message.text)
        #print(message.text)
        g.write(message.text+","+time[val].text+","+sender[val].text+"\n")
        val+=1
    f.close()
    g.close()

for file in filelist:
    run(file)

def analyze(msg_list, user_name):
    print("Running analysis for " + user_name)
    all_msg = " ".join(msg_list)
    most_common_words = collections.Counter(re.findall(r"\b\w+\b", all_msg.lower())).most_common(250)
    print(most_common_words)

print(len(user1_msg))
print(len(user2_msg))
analyze(user1_msg, user1_name)
analyze(user2_msg, user2_name)

#uncomment below to make it into a spreadsheet

#df = pd.DataFrame(data)
#df.to_csv("messages.csv")