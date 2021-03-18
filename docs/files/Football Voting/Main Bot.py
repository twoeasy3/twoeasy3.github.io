import telebot
from telebot import types
from PIL import Image
import os
import random
from io import BytesIO
global namesList
global matchup
global mode
mode = "singles"
bot = telebot.TeleBot("token_removed")

class player(object):
    def __init__(self,name,elo,folder,multi,count):
        self.name = name
        self.elo = elo
        self.folder = folder
        self.multi = multi
        self.count = count



playerdata = []
multinames = ["Center-back","Full-Back","Winger","Striker","D. Midfielder","A. Midfielder","Super Sub"]
playerRatings = open("playerRatings.dat",'r')
newline = playerRatings.readline()
newline = playerRatings.readline()
while "End of File" not in newline:
    newline = newline.strip('\n')
    newline = newline.split('|')
    tempname = newline.pop(0)
    tempelo = eval(newline.pop(0))
    tempcount = int(newline.pop(-1))
    tempfolder = newline.pop(0)
    for i in range(0,len(newline)):
        newline[i] = float(newline[i])
    playerdata.append(player(tempname,tempelo,tempfolder,newline,tempcount))
    newline = playerRatings.readline()
playerRatings.close()

markup_next = types.ReplyKeyboardMarkup(one_time_keyboard = True)
itembtnNext = types.KeyboardButton("Next Vote")
markup_next.row(itembtnNext)

def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_h_multi_blank(im_list):
    _im = im_list.pop(0)
    for im in im_list:
        _im = get_concat_h_blank(_im, im)
    return _im

def matchmake(chatID):
    global mode
    namesList = []
    matchlist = []
    matchup = []
    roll = random.randint(1,10)

    if roll >8: 
        mode = 'doubles'
    elif roll >5: 
        mode = 'situational'
    else:
        mode = 'singles'

    if mode == 'singles':
        for item in playerdata:
            multip = random.randint(0,6) ##denotes which multiplier is used
            entry = [0,item.name,item.elo,item.multi[multip],multip,item]
            entry[0] = int(entry[2]*entry[3])
            matchlist.append(entry)
    elif mode == 'doubles':
        for item in playerdata:
            entry = [item.elo,item.name,item.elo,None,None,item] ##mirroring format for singles
            matchlist.append(entry)
    elif mode == 'situational':
        for item in playerdata:
            multip = random.randint(4,6) ##denotes which multiplier is used
            entry = [0,item.name,item.elo,item.multi[multip],multip,item]
            entry[0] = int(entry[2]*entry[3])
            matchlist.append(entry)

    matchlist.sort()
    pullInt = random.randint(-3,len(matchlist)) ##close matchup
    if pullInt <0:
        pullInt = 0
    if pullInt > len(matchlist)-4:
        pullInt = len(matchlist)-4

    for i in range(pullInt,pullInt + 4):
        matchup.append([matchlist[i][-1],matchlist[i][-2]])
    random.shuffle(matchup)
    path = []
    for i in range(0,4):
        filecount = next(os.walk(os.path.join(os.getcwd(),"images",matchup[i][0].folder)))[2]
        files = len(filecount)
        picPick = str(random.randint(1,files))+ '.png'
        path.append(os.path.join(os.getcwd(),"images",matchup[i][0].folder,picPick))
    im1 = Image.open(path[0])
    im2 = Image.open(path[1])
    im3 = Image.open(path[2])
    im4 = Image.open(path[3])
    im_list = [im1,im2,im3,im4]
    grid = get_concat_h_multi_blank([im1, im2, im3,im4])
    bio = BytesIO()
    bio.name = 'grid.jpeg'
    grid.save(bio, 'JPEG')
    bio.seek(0)
    bot.send_photo(chatID, photo=bio)



    if mode == 'singles':
        replytxt = str("You have to pick one player for the listed position in your team. Who is going in?")
        bot.send_message(text = replytxt, chat_id = chatID)
        for i in range(0,4):
            namesList.append(matchup[i][0].name)
        for item in matchup:
            replytxt = str(item[0].name + ' (' + multinames[item[-1]] + ')')
            bot.send_message(text = replytxt, chat_id = chatID)

        textA = matchup[0][0].name
        textB = matchup[1][0].name
        textC = matchup[2][0].name
        textD = matchup[3][0].name
        markup_Normal = types.ReplyKeyboardMarkup(one_time_keyboard = True)
        itembtnA = types.KeyboardButton(textA)
        itembtnB = types.KeyboardButton(textB)
        itembtnC = types.KeyboardButton(textC)
        itembtnD = types.KeyboardButton(textD)
        markup_Normal.row(itembtnA, itembtnB)
        markup_Normal.row(itembtnC, itembtnD)
        bot.send_message(text = 'Take your pick', reply_markup = markup_Normal, chat_id = chatID)
    elif mode == 'doubles':
        replytxt = str("You have to pick one pair for your team. Who is going in?")
        bot.send_message(text = replytxt, chat_id = chatID)
        for i in range(0,4,2):
            replytxt = str(matchup[i][0].name + " & " + matchup[i+1][0].name)
            bot.send_message(text = replytxt, chat_id = chatID)
        textE = str(matchup[0][0].name + " & " + matchup[1][0].name)
        textF = str(matchup[2][0].name + " & " + matchup[3][0].name)
        namesList = [textE,textF]
        markup_Doubles = types.ReplyKeyboardMarkup(one_time_keyboard = True)
        itembtnE = types.KeyboardButton(textE)
        itembtnF = types.KeyboardButton(textF)
        markup_Doubles.row(itembtnE)
        markup_Doubles.row(itembtnF)
        bot.send_message(text = 'Take your pick', reply_markup = markup_Doubles, chat_id = chatID)

    elif mode == 'situational':
        replytxt = str(matchup[0][0].name + " has needs to be subbed due to injury. Who would you sub in?")
        bot.send_message(text = replytxt, chat_id = chatID)
        for i in range(1,4):
            replytxt = str(matchup[i][0].name + ' ' + multinames[matchup[i][-1]])
            bot.send_message(text = replytxt, chat_id = chatID)
        textG = matchup[1][0].name
        textH = matchup[2][0].name
        textI = matchup[3][0].name
        namesList = [None,textG,textH,textI]
        itembtnG = types.KeyboardButton(textG)
        itembtnH = types.KeyboardButton(textH)
        itembtnI = types.KeyboardButton(textI)
        markup_situational = types.ReplyKeyboardMarkup(one_time_keyboard = True)
        markup_situational.row(itembtnG, itembtnH, itembtnI)
        bot.send_message(text = 'Take your pick', reply_markup = markup_situational, chat_id = chatID)


    return(namesList,matchup)

def updateElo(matchup,winner,chatID):
    global mode
    if mode == 'singles':
        winnerElo = matchup[winner][0].elo * (matchup[winner][0].multi[matchup[winner][-1]])
        matchup[winner][0].multi[matchup[winner][-1]] += 0.15 ##increase multiplier rating
        matchup[winner][0].multi[matchup[winner][-1]] = round(matchup[winner][0].multi[matchup[winner][-1]],3)
        matchup[winner][0].count += 1
        for i in range(0,len(matchup)):
            if i != winner:
                expected = 1/(1+10**((matchup[i][0].elo * (matchup[i][0].multi[matchup[i][-1]]) - winnerElo)/400))
                matchup[i][0].multi[matchup[i][-1]] -= 0.05
                matchup[i][0].multi[matchup[i][-1]] = round(matchup[i][0].multi[matchup[i][-1]],3)
                if matchup[i][0].multi[matchup[i][-1]] < 0.2: ##multiplier cannot fall below 0.2
                   matchup[i][0].multi[matchup[i][-1]] = 0.2
                difference = 11*(1-expected)
                matchup[i][0].elo = int(matchup[i][0].elo - difference)
                matchup[winner][0].elo = int(matchup[winner][0].elo + difference)
    elif mode == 'doubles':
        if winner == 0:
            matchup[0][0].count += 1
            matchup[1][0].count += 1
            for i in range(0,2):
                for f in range(2,4):
                    expected = 1/(1+10**((matchup[f][0].elo - matchup[i][0].elo)/400))
                    difference = 5*(1-expected)
                    matchup[f][0].elo = int(matchup[f][0].elo - difference)
                    matchup[i][0].elo = int(matchup[i][0].elo + difference)
        elif winner == 1:
            matchup[2][0].count += 1
            matchup[3][0].count += 1
            for i in range(2,4):
                for f in range(0,2):
                    expected = 1/(1+10**((matchup[f][0].elo - matchup[i][0].elo)/400))
                    difference = 5*(1-expected)
                    matchup[f][0].elo = int(matchup[f][0].elo - difference)
                    matchup[i][0].elo = int(matchup[i][0].elo + difference)
    elif mode == 'situational':
        winnerElo = matchup[winner][0].elo * (matchup[winner][0].multi[matchup[winner][-1]])
        matchup[winner][0].multi[matchup[winner][-1]] += 0.15 ##increase multiplier rating
        matchup[winner][0].multi[matchup[winner][-1]] = round(matchup[winner][0].multi[matchup[winner][-1]],3)
        matchup[winner][0].count += 1
        for i in range(1,len(matchup)):
            if i != winner:
                expected = 1/(1+10**((matchup[i][0].elo * (matchup[i][0].multi[matchup[i][-1]]) - winnerElo)/400))
                matchup[i][0].multi[matchup[i][-1]] -= 0.05
                matchup[i][0].multi[matchup[i][-1]] = round(matchup[i][0].multi[matchup[i][-1]],3)
                if matchup[i][0].multi[matchup[i][-1]] < 0.2: ##multiplier cannot fall below 0.2
                   matchup[i][0].multi[matchup[i][-1]] = 0.2
                difference = 15*(1-expected)
                matchup[i][0].elo = int(matchup[i][0].elo - difference)
                matchup[winner][0].elo = int(matchup[winner][0].elo + difference)


    ##for item in matchup:
        ##print(item[0].name,item[0].elo)
    playerRatings = open("playerRatings.dat",'w')
    print('playername|elo|folder|m1|m2|m3|m4|m5|m6|m7|count',file=playerRatings)
    for item in playerdata:
        newline = item.name + '|' + str(item.elo) + '|' + str(item.folder) + '|' + '|'.join(map(str, item.multi))
        newline = newline + '|' + str(item.count)
        print(newline,file=playerRatings)
    print('End of File',file=playerRatings)
    bot.send_message(text = 'Your choice has been logged.', reply_markup = markup_next, chat_id = chatID)
    

def statistics(chatID):
    summarylist = []
    for item in playerdata:
        summarylist.append([item.elo,item.name,item.count])
    summarylist.sort()
    summarytext = 'Current standings \n'
    for i in range(len(summarylist)-1,-1,-1):
        summarytext += summarylist[i][1] + '   ' + str(summarylist[i][0]) + "  " + str(summarylist[i][2]) + '\n'
    bot.send_message(text = summarytext, chat_id = chatID)




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "The bot is up and running :)", reply_markup = markup_next)
    a = message.chat.id
namesList = []
matchup = []
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global namesList
    global matchup
    global mode
    if message.text in namesList:
        for i in range(0,len(namesList)):
            if message.text == namesList[i]:
                winner = i
                updateElo(matchup,winner,message.chat.id)
                print("updated")
    elif message.text == "Next Vote":
        namesList,matchup = matchmake(message.chat.id)
        print("NAMES",namesList)
    elif message.text == 'stats':
        statistics(message.chat.id)
    else:
        pass

bot.polling()
