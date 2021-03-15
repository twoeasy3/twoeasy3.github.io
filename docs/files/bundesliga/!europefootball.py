import numpy
import random
import os
from tkinter import *

from PIL import Image, ImageTk

def create_balanced_round_robin(players):
    """ Create a schedule for the players in the list and return it"""
    s = []
    if len(players) % 2 == 1: players = players + [None]
    # manipulate map (array of indexes for list) instead of list itself
    # this takes advantage of even/odd indexes to determine home vs. away
    n = len(players)
    map = list(range(n))
    mid = n // 2
    for i in range(n-1):
        l1 = map[:mid]
        l2 = map[mid:]
        l2.reverse()
        round = []
        for j in range(mid):
            t1 = players[l1[j]]
            t2 = players[l2[j]]
            if j == 0 and i % 2 == 1:
                # flip the first match only, every other round
                # (this is because the first match always involves the last player in the list)
                round.append((t2, t1))
            else:
                round.append((t1, t2))
        s.append(round)
        # rotate list by n/2, leaving last element at the end
        map = map[mid:-1] + map[:mid] + map[-1:]
    return s

class team(object):
    def __init__(self,name,shortname,coeff,logo):
        self.name = name
        self.shortname = shortname
        self.coeff = coeff
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.points = 0
        self.goalsfor = 0
        self.goalsagainst = 0
        self.lastFive = ['','','','','']
        self.formstring = ''
        self.logo = os.path.join(os.getcwd(),logo)
    def reportGame(self,goalsfor,goalsagainst):
        self.played += 1
        self.goalsfor += goalsfor
        self.goalsagainst += goalsagainst
        if goalsfor > goalsagainst:
            self.wins += 1
            self.points += 3
            self.form("＋")
            self.coeff -= 10
        elif goalsfor < goalsagainst:
            self.losses += 1
            self.form("－")
            self.coeff += 50
        elif goalsfor == goalsagainst:
            self.draws += 1
            self.points += 1
            self.form("＝")
            self.coeff += 10
            
    def form(self,result):
        for i in range(len(self.lastFive)-2,-1,-1):
            self.lastFive[i+1] = self.lastFive[i]
        self.lastFive[0] = result
        self.formstring = ''.join(self.lastFive)
        
            
            

def getTeams():
    teams = [[],[],[]]
    file = open("TEAMS.txt",'r')
    newline = file.readline().strip("\n")
    index = -1
    while len(newline) != 0:
        if "#" in newline:
            index += 1
        else:
            data = newline.split(";")
            teams[index].append(team(data[0],data[1],int(data[2]),data[3]))
        newline = file.readline().strip("\n")
    file.close()
    return(teams)

def simGame(team1,team2):
    team1_performance = numpy.random.normal(team1.coeff,team1.coeff*0.20) + 50 ##home advantage
    team2_performance = numpy.random.normal(team2.coeff,team2.coeff*0.20)
    perform_diff = abs(team1_performance-team2_performance)
    if perform_diff > 300:
        if perform_diff < 650:
            score_diff = int(abs(numpy.random.normal(1.8,2)))
            score_bonus = 0
        else:
            score_diff = int(abs(numpy.random.normal(3,1.5)))
            if team1_performance > team2_performance:
                score_bonus = int(numpy.random.normal(team1.coeff/2000,team1.coeff/2000*0.5))
            else:
                score_bonus = int(numpy.random.normal(team2.coeff/2000,team2.coeff/2000*0.5))
        if team1_performance > team2_performance:
            team1_score = int(numpy.random.normal(2,1.5)) + score_bonus
            if team1_score < 1:
                team1_score = 1
            team2_score = team1_score - score_diff
            if team2_score <0:
                team2_score = 0
            if team2_score == team1_score:
                team2_score = team1_score - 1
        elif team2_performance > team1_performance:
            team2_score = int(numpy.random.normal(2,1.5)) + score_bonus
            if team2_score < 1:
                team2_score = 1
            team1_score = team2_score - score_diff
            if team1_score <0:
                team1_score = 0
            if team1_score == team2_score:
                team1_score = team2_score -1
    else:
        team1_score = int(numpy.random.normal(2,1.5))
        if team1_score < 0:
            team1_score = 0 
        team2_score = team1_score
    team1.reportGame(team1_score,team2_score)
    team2.reportGame(team2_score,team1_score)
    return(team1_score,team2_score)

def matchday():
    global mday
    global schedules
    global matchresults
    global matches
    global active_league
    mday +=1

    if mday > 38:
        return
    labeltexts = ['']*18
    for f in range(len(schedules)):
        if mday >34 and f == 0:
            pass
        else:
            for i in range(0,len(schedules[f][mday-1])):
                results = simGame(schedules[f][mday-1][i][0],schedules[f][mday-1][i][1])
                matchresults[f][((i+1)*2)-1] = results[0]
                matchresults[f][((i+1)*2)] = results[1]


            for i in range(1,len(teams[f])):
                last = teams[f][i]
                j = i-1
                while j >= 0 and teams[f][j].points < last.points:
                    teams[f][j+1] = teams[f][j]
                    j -= 1
                while j >= 0 and teams[f][j].points == last.points and (teams[f][j].goalsfor - teams[f][j].goalsagainst) < (last.goalsfor - last.goalsagainst):
                    teams[f][j+1] = teams[f][j]
                    j -= 1
                while j >= 0 and teams[f][j].points == last.points and (teams[f][j].goalsfor - teams[f][j].goalsagainst) == (last.goalsfor - last.goalsagainst) and teams[f][j].goalsfor < last.goalsfor:
                    teams[f][j+1] = teams[f][j]
                    j -= 1
                teams[f][j+1] = last
    updateDisplay(active_league)


    
def updateDisplay(f):
    global mday
    global schedules
    global teams
    global labels
    global logos
    global matchresults
    global matches
    global matchlogos
    global upcomingmatches
    global upcomingmatchlogos
    

    umday = mday
    if f == 0 and umday > 34:
        umday = 34
    if umday > 38:
        umday = 38
    
    n=0
    for m in range(1,int(len(teams[f])/2)+1):
        matchlogos[f][(m*2-1)].config(file = schedules[f][umday-1][m-1][0].logo)
        matches[f][n].config(image = matchlogos[f][(m*2)-1])
        matches[f][n+1].config(text = matchresults[f][(m*2)-1])
        matches[f][n+2].config(text = ":")
        matches[f][n+3].config(text = matchresults[f][(m*2)])
        matchlogos[f][(m*2)].config(file = schedules[f][umday-1][m-1][1].logo)
        matches[f][n+4].config(image = matchlogos[f][(m*2)])
        n += 5

        
    upday = umday
    if f == 0 and upday >= 34:
        upday = 33
    elif upday >= 37:
        upday = 37
    n=0        
    for m in range(1,int(len(teams[f])/2)+1):
        upcomingmatchlogos[f][(m*2-1)].config(file = schedules[f][upday][m-1][0].logo)
        upcomingmatches[f][n].config(image = upcomingmatchlogos[f][(m*2)-1])
        upcomingmatches[f][n+2].config(text = "vs")
        upcomingmatchlogos[f][(m*2)].config(file = schedules[f][upday][m-1][1].logo)
        upcomingmatches[f][n+4].config(image = upcomingmatchlogos[f][(m*2)])
        n += 5

    n=0
    for r in range(1,len(teams[f])+1):
        logos[f][r-1].config(file = teams[f][r-1].logo)
        labels[n].config(text = r)
        labels[n+1].config(image = logos[f][r-1])
        labels[n+2].config(text = teams[f][r-1].name)
        labels[n+3].config(text = teams[f][r-1].played)
        labels[n+4].config(text = teams[f][r-1].wins)
        labels[n+5].config(text = teams[f][r-1].draws)
        labels[n+6].config(text = teams[f][r-1].losses)
        labels[n+7].config(text = teams[f][r-1].goalsfor)
        labels[n+8].config(text = teams[f][r-1].goalsagainst)
        labels[n+9].config(text = teams[f][r-1].goalsfor - teams[f][r-1].goalsagainst)
        labels[n+10].config(text = teams[f][r-1].points)
        labels[n+11].config(text = teams[f][r-1].formstring)
        n += 12
        
    

    root.update()
    
def updateGER():
    global active_league
    for i in range(216,215+25):
        labels[i].grid_remove()
    for label in matches[active_league]:
        label.grid_remove()
    for label in upcomingmatches[active_league]:
        label.grid_remove()

    active_league = 0
    for label in matches[0]:
        label.grid()
    for label in upcomingmatches[0]:
        label.grid()
        
    updateDisplay(active_league)
def updateENG():
    global active_league
    if active_league == 0:
        for i in range(216,215+25):
            labels[i].grid()        
    for label in matches[active_league]:
        label.grid_remove()
    for label in upcomingmatches[active_league]:
        label.grid_remove()
    active_league = 1        
    for label in matches[1]:
        label.grid()
    for label in upcomingmatches[1]:
        label.grid()
        
    updateDisplay(active_league)
def updateSPN():
    global active_league
    if active_league == 0:
        for i in range(216,215+25):
            labels[i].grid()        
    for label in matches[active_league]:
        label.grid_remove()
    for label in upcomingmatches[active_league]:
        label.grid_remove()
    active_league = 2      
    for label in matches[2]:
        label.grid()
    for label in upcomingmatches[2]:
        label.grid()
    updateDisplay(active_league)
    

    
    

active_league = 0    
teams = getTeams()

schedules = [[]for i in range(len(teams))]
for i in range(len(teams)):
    schedules[i] = create_balanced_round_robin(teams[i])
    schedule2 = schedules[i].copy()
    for item in schedule2:
        temp = item[1]
        item[1] = item[0]
        item[0] = temp
    schedules[i] += schedule2

mday = 0
root = Tk()
frame = Frame(root)
labels = []


Label(root, text = "Rank",font=('Monospace',14)).grid(row=0,column=0)
Label(root, text = "Team",font=('Monospace',14)).grid(row=0,column=1,columnspan = 2)
Label(root, text = "P",font=('Monospace',14)).grid(row=0,column=3)
Label(root, text = "W",font=('Monospace',14)).grid(row=0,column=4)
Label(root, text = "D",font=('Monospace',14)).grid(row=0,column=5)
Label(root, text = "L",font=('Monospace',14)).grid(row=0,column=6)
Label(root, text = "GF",font=('Monospace',14)).grid(row=0,column=7)
Label(root, text = "GA",font=('Monospace',14)).grid(row=0,column=8)
Label(root, text = "GD",font=('Monospace',14)).grid(row=0,column=9)
Label(root, text = "Pt",font=('Monospace',14)).grid(row=0,column=10)
Label(root, text = "{0:^14}".format("Form"),font=('Monospace',14)).grid(row=0,column=11)

labels = []
logos = [[]for i in range(len(teams))]

for i in range(0,len(teams)):
    for team in teams[i]:
        logos[i].append(PhotoImage(file = team.logo))


for r in range(1,19):
    labels.append(Label(root,text = r,font=('Monospace',13)))
    labels.append(Label(image = logos[0][r-1]))
    labels.append(Label(root,text = teams[0][r-1].name,font=('Monospace',13)))
    labels.append(Label(root,text = teams[0][r-1].played,font=('Monospace',13)))
    labels.append(Label(root,text = teams[0][r-1].wins,font=('Monospace',13)))
    labels.append(Label(root,text = teams[0][r-1].draws,font=('Monospace',13)))
    labels.append(Label(root,text = teams[0][r-1].losses,font=('Monospace',13)))
    labels.append(Label(root,text = teams[0][r-1].goalsfor,font=('Monospace',13)))
    labels.append(Label(root,text = teams[0][r-1].goalsagainst,font=('Monospace',13)))    
    labels.append(Label(root,text = teams[0][r-1].goalsfor - teams[0][r-1].goalsagainst,font=('Monospace',13)))
    labels.append(Label(root,text = teams[0][r-1].points,font=('Monospace',13,'bold')))
    labels.append(Label(root,text = teams[0][r-1].formstring,font=('Monospace',13)))
for r in range(19,21):
    labels.append(Label(root,text = None,font=('Monospace',13)))
    labels.append(Label(image = None))
    labels.append(Label(root,text = None,font=('Monospace',13)))
    labels.append(Label(root,text = None,font=('Monospace',13)))
    labels.append(Label(root,text = None,font=('Monospace',13)))
    labels.append(Label(root,text = None,font=('Monospace',13)))
    labels.append(Label(root,text = None,font=('Monospace',13)))
    labels.append(Label(root,text = None,font=('Monospace',13)))
    labels.append(Label(root,text = None,font=('Monospace',13)))    
    labels.append(Label(root,text = None,font=('Monospace',13)))
    labels.append(Label(root,text = None,font=('Monospace',13,'bold')))
    labels.append(Label(root,text = None,font=('Monospace',13)))



n=0
for r in range(1,21):
    for c in range(0,12):
        labels[n].grid(row=r,column=c)
        n+=1

matches = [[]for i in range(len(teams))]
matchlogos = [[0] for i in range(len(teams))]
matchresults = [[" - "]*21 for i in range(len(teams))]
for i in range(len(matches)):
    for m in range(1,int((len(teams[i])/2)+1)):
        matchlogos[i].append(PhotoImage(file = schedules[i][mday-1][m-1][0].logo))
        matches[i].append(Label(image = matchlogos[i][(m*2)-1]))
        matches[i].append(Label(root,text = matchresults[i][(m*2)-1]))
        matches[i].append(Label(root,text = ":"))
        matches[i].append(Label(root,text = matchresults[i][(m*2)]))
        matchlogos[i].append(PhotoImage(file = schedules[i][mday-1][m-1][1].logo))
        matches[i].append(Label(image = matchlogos[i][(m*2)]))
n = 0




for i in range(1,len(teams)):
    n=0
    for r in range(1,11):
        for c in range(12,17):
            matches[i][n].grid(row=r, column = c)
            matches[i][n].grid_remove()
            n +=1

upcomingmatches = [[]for i in range(len(teams))]
upcomingmatchlogos = [[0] for i in range(len(teams))]

for i in range(len(upcomingmatches)):
    for m in range(1,int((len(teams[i])/2)+1)):
        upcomingmatchlogos[i].append(PhotoImage(file = schedules[i][mday-1][m-1][0].logo))
        upcomingmatches[i].append(Label(image = upcomingmatchlogos[i][(m*2)-1]))
        upcomingmatches[i].append(Label(root,text = ""))
        upcomingmatches[i].append(Label(root,text = "vs"))
        upcomingmatches[i].append(Label(root,text = ""))
        upcomingmatchlogos[i].append(PhotoImage(file = schedules[i][mday-1][m-1][1].logo))
        upcomingmatches[i].append(Label(image = upcomingmatchlogos[i][(m*2)]))


for i in range(0,len(teams)):
    n=0
    for r in range(int((len(teams[i])/2)) + 1 ,int((len(teams[i]))) +1):
        for c in range(12,17):
            upcomingmatches[i][n].grid(row=r, column = c)
            upcomingmatches[i][n].grid_remove()
            n +=1


n = 0
for r in range(1,10):
    for c in range(12,17):
        matches[0][n].grid(row=r, column = c)
        n+=1
        

button_adv = Button(root,text="Click to advance matchday",command= matchday).grid(row = 21,columnspan = 10)
button_bundesliga = Button(root,text = "GER",command = updateGER).grid(row=22,column = 0)
button_EPL = Button(root,text = "ENG",command = updateENG).grid(row=22,column = 1)
button_LaLiga = Button(root,text = "SPN",command = updateSPN).grid(row=22,column  = 2)
updateGER()
root.mainloop()




