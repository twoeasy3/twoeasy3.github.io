import json 
import requests
import time
import urllib
import random

player_ids = []
team_names = []  ##now team ID
team_answers = []
team_score = []
answered_this_round = []
legal_answers = ["A","B","C","D","E"]
check = ["0","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
startFlag = False
acceptAns = False
question_number = 0
is_good = ["Woohoo!", "You've got it!","Excellent work :)","Well done!","Bullseye!","Correct!",
           "Big brain :)" , "Nailed it!", "Good job!", "Ka-ching!", "Ding Ding Ding!", "Correct :)",
           "Getting in the groove!","Spectacular!", "Banking some points!","Getting some more points!"]
is_bad = ["Better luck next time :(", "Aw shucks :(", "We'll get 'em next time!", "oof :(" , "isokay :(",
          "ohno :(", "Keep on trying!", "Bad luck :(", "That was a tricky one :(", "Okay time to comeback!",
          "You'll get the next one!","Maybe the next one!"]


answers = ['E','C','C','A','B','E','D','C','A','B','B','A','D','E']
question_score = [0,0,1000,2000,0,-1,-1,-1,-1,-1,1500,2500,1750,2250]
question_name = [['0','1'],['0','2'],['1','1'],['1','2'],['2','0'],['2','1'],['2','2'],['2','3'],['2','4'],['2','5'],['3','1'],['3','2'],['4','1'],['4','2']]

TOKEN = "834906418:AAEU_E5IAVBcSmlEAC1hHqYy0FqeGJSo2Vg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
def echo_all(updates):
    global player_ids
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            if chat == 270095064:
                host_options(text)                
                
            elif startFlag == False:            
                if text == "/start":
                    send_message("Please enter your team ID!",chat)

                else:
                    if chat not in player_ids:
                        validate_group(text,chat)
            else:
                
                validate_answer(text,chat)

        
        except Exception as e:
            print(e)

def validate_group(text,chat):
    global player_ids
    global team_names
    global check
    global team_score
    text = text.upper()
    lista = list(text)
    if len(text) != 4:
        send_message("This is not a valid group ID. Try again.",chat)
    elif check[(int(lista[0]) + int(lista[1]) + int(lista[2]))*2] != lista[3]:
        send_message("This is not a valid group ID. Check that you have entered the correct ID.",chat)
    else:
        player_ids.append(chat)
        team_names.append(text)
        team_score.append(0)
        team_answers.append(['','','','','','','','','','','','','',''])
        send_message("Your team "+ text + " has been entered on the bot. Please use this phone throughout the session. Thank you! :)",chat)
        print("Number of players: " + str(len(player_ids)))
        print(team_names)
    

def record_answer(text,chat):
    global player_ids
    global team_answers
    global question_number
    global answered_this_round
    for i in range(0,len(player_ids)):
        if chat == player_ids[i]:
            team_answers[i][question_number] = text
            ## send_message("You have locked in " + text + " as your answer for Round " + question_name[question_number][0] + " Question " + question_name[question_number][1] + "!",chat)            
            if team_names[i] not in answered_this_round:
                answered_this_round.append(team_names[i])
    print("Answers this round: ", len(answered_this_round))
    

def validate_answer(text,chat):
    global legal_answers
    global acceptAns
    if acceptAns == False:
        send_message("Polling is not open anymore :(",chat)
        return
    if len(text) != 1:
        send_message("Please only the letter of your selection! Your answer was not recorded.", chat)
        return
    text = text.upper()
    if text not in legal_answers:
        send_message("Sorry, that was not a legal choice. Your answer was not recorded." , chat)
        return
    record_answer(text,chat)
    
    

def host_options(text):
    global startFlag
    global question_number
    global player_ids
    global team_names
    global team_answers
    global acceptAns
    if text == "debug":
        a = 0
        while a < 10:
            send_message("debug" + str(a),270095064)
            a = a+1
    elif text == "start":
        startFlag = True
        send_message("Bowl has started.", 270095064)
        acceptAns = True
    elif text == "end":
        if acceptAns != False:
            send_message("nO type 'stop' first", 270095064)
            return
        end_bowl()
    elif text == "stop":
        acceptAns = False
        stop_question(question_number)
    elif startFlag == True:
        question_number = int(text)
        acceptAns = True
        ping_question(question_number)


def stop_question(question_number):
    global player_ids
    global team_answers
    global answers
    global team_names
    global team_score
    global question_score
    global is_good
    global is_bad
    global answers_this_round
    answers_this_round = []
    no_response = [4,5,6,7,8]
    if question_score[question_number] == -1:
        correct = 0
        incorrect = 0
        for teamAns in team_answers:
            if teamAns[question_number] == answers[question_number]:
                correct += 1
            else:
                incorrect += 1
        percent = int((correct/(correct+incorrect))*100)
        print("Percentage " + str(percent))
        print(str(((100-percent)/100)*400+100))
    else:
        count = [0,0,0,0,0]
        for teamAns in team_answers:
            if teamAns[question_number] == "A":
                count[0] +=1
            elif teamAns[question_number] == "B":
                count[1] +=1
            elif teamAns[question_number] == "C":
                count[2] +=1
            elif teamAns[question_number] == "D":
                count[3] +=1
            elif teamAns[question_number] == "E":
                count[4] +=1
        print("answers: ", count)
        for i in range(0,len(count)):
            count[i] = int(count[i]/len(player_ids))*100
        print("percentages: ",count)
    for i in range(0,len(player_ids)):
        if team_answers[i][question_number] == answers[question_number]:
            if question_score[question_number] == 0:
                send_message(random.choice(is_good) + " But unfortunately this round does not award points :(" , player_ids[i]) 
            elif question_score[question_number] != -1:
                team_score[i] += question_score[question_number]
            else:
                team_score[i] += (((100-percent)/100)*400+100)
        elif team_answers[i][question_number] != answers[question_number] and question_number not in no_response:
            send_message(random.choice(is_bad) + " Your team still sits on " + str(team_score[i]) + " points." , player_ids[i])
        if question_number == 9:
            send_message("Lightning Round has ended! Your team now has " + str(team_score[i]) + " points." , player_ids[i])

    send_message("Question ended successfully",270095064)
    for i in range(0,len(team_names)):
        print("{0:5}{1:6}".format(team_names[i],team_score[i]))
        

def ping_question(question_number):
    global questions
    global player_ids
    ##for users in player_ids:
        ##send_message("Polling for Round " + question_name[question_number][0] + " Question " + question_name[question_number][1] + " has started!" ,users)
    send_message("Polling for Round " + question_name[question_number][0] + " Question " + question_name[question_number][1] + " has started!", 270095064)

def end_bowl():
    global team_names
    global player_ids
    global team_score
    for i in range(0,len(team_names)):
        print("{0:5}{1:6}".format(team_names[i],team_score[i]))


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.1)




if __name__ == '__main__':
    main()
