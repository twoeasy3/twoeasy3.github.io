import random
import time
##hot potato

def potato():
    gamemodeSelectCheck = 0
    while gamemodeSelectCheck == 0:
        gamemode = input('Classic (C), Gauntlet (G), Battle Royale (B) or Team Battle (T) ')
        if gamemode.capitalize() == 'C' :
            gamemode = 'potato'
            gamemodeSelectCheck = 1
        elif gamemode.capitalize() == 'G':
            gamemode = 'potatogauntlet'
            gamemodeSelectCheck = 1
        elif gamemode.capitalize() == 'B':
            gamemode = 'potatoroyale'
            gamemodeSelectCheck = 1
        elif gamemode.capitalize() == 'T':
            gamemode = 'potatoteam'
            gamemodeSelectCheck = 1
        else:
            print('Please type in valid selection.')
            
    if gamemode == 'potatoroyale':
        print('----------------------------------------------------')
        print("A truly huge battle with 100 players.")
        print("Aim for the highest score by being the last one standing.")
        player = input("Please enter a name: ")

        royale_roster = ['Gregory', 'Spaz', 'Toxic Mankey', 'Gordini', 'Gianni','Tarquini', 'Seb', 'Hairy Beast', 'Whale', 'Gabrielle', 'Nakumura', 'Czechmate', 'Steine',  'Giovanni', 'Defender', 'Thunder' , 'Snake Eyes', 'Marcello', 'Champion', 'Looney', 'KC', 'Gullwing', 'The Forgotten' , 'Prototyp', 'Louis', 'AJ', 'Rover Patrol', 'Bow-Wow', 'BigDogge', 'Bubba' , 'Testarossa', 'Kerpelmann', 'Andrew', 'Krissten' , 'Charli', 'THRICE' , 'Leopard' , 'Gerrard' , 'Viper' , 'Partisan', 'Hitman', 'Test Dummy', 'Mountaineer', 'Crystal Castle', 'Peterbuilt', 'Long Face' ,'Threefiddy' , 'Alexis', 'Edisni', 'Davidson' , 'Naghavi', 'Jo', 'MelB' , 'Mushimoto', 'Cunningham', 'Droopy', 'Aint Skeerd','Mary-Jane', 'XCX' , 'Grundo' , 'Hippopotamus', 'Tarmogoyf' , 'Kreger', 'Fernando', 'Grave Digger', 'Metroholic' , 'Hariyama', 'twoeasy3', 'M500' , 'Boomz', 'Spacey', 'Saheeli' , 'JiSoo' , 'Jace', 'type_23' ,'Dreamshatterer', 'Heath', 'Snapcaster' ,'DTR_Cage', 'Lowe' , 'Panzerkampfwagen', 'Competizione' , 'Giulietta', 'KatEyes', 'Keller' , 'Skreli', 'Chandra', 'Bulroth' , 'Randezvous' , "D'zongo", 'Stave', 'Terry', 'Button', 'Guardian', 'Fforde', 'Duncan', 'Andrea', 'Byron Lightning', 'GoodNews', 'Nissa', 'Rossolini' , 'Johnny', 'Oh Cock', 'Masked Admirer']
        active_order = random.sample(royale_roster, 100)


        if player == 'sim' or player == 'Sim':
            pass
        elif player != 'sim' or player != 'Sim':
            user_order = random.randint(0,99)
            active_order[user_order] = player
        
        active_order_copy = list(active_order)
        
        print('The players are:')
        for i in range(0,len(active_order)):
            print(active_order[i])
        if player == 'sim' or player == 'Sim':
            print('You are spectating this match.')
        elif player != 'sim' or player != 'Sim':
            print('You are number' , user_order + 1 , 'in the queue.')

        player_team = [''] * 100

    if gamemode == 'potatogauntlet':
        print('----------------------------------------------------')
        print("This gamemode never ends, survive as long as you can.")
        print("Each time an opponent is eliminated, another challenger takes their place.")
        print("When you get blown up, the game is over.")
        print("Score as many points and kills as possible.")

        player = input("Please enter a name: ")

        active_roster1 = ['Gregory', 'Spaz', 'Toxic Mankey', 'Gordini', 'Gianni','Tarquini', 'Seb', 'Hairy Beast', 'Whale', 'Gabrielle', 'Nakumura', 'Czechmate', 'Steine', ]
        active_roster2 = ['Giovanni', 'Defender', 'Thunder' , 'Snake Eyes', 'Marcello', 'Champion', 'Looney', 'KC', 'Gullwing', 'The Forgotten' , 'Prototyp', 'Louis', 'AJ']
        active_roster3 = ['Rover Patrol', 'Bow-Wow', 'BigDogge', 'Bubba' , 'Testarossa', 'Kerpelmann', 'Andrew', 'Bing Bong' , 'Charli', 'THRICE' , 'Leopard' , 'Gerrard' , 'Viper']
        active_roster4 = ['Partisan', 'Hitman', 'Test Dummy', 'Mountaineer', 'Crystal Castle', 'Peterbuilt', 'Long Face' ,'Threefiddy' , 'Alexis', 'Edisni', 'Davidson' , 'Naghavi', 'Jo']
        active_roster5 = ['MelB' , 'Mushimoto', 'Cunningham', 'Droopy', 'Aint Skeerd','Mary-Jane', 'XCX' , 'Grundo' , 'Hippopotamus', 'Tarmogoyf' , 'Kreger', 'Fernando', 'Grave Digger']
        active_roster6 = ['Metroholic' , 'Hariyama', 'twoeasy3', 'M500' , 'Boomz', 'Spacey', 'Saheeli' , 'JiSoo' , 'Jace', 'type_23' ,'Dreamshatterer', 'Heath', 'Snapcaster' ]
        active_roster7 = ['DTR_Cage', 'Lowe' , 'Panzerkampfwagen', 'Competizione' , 'Giulietta', 'KatEyes', 'Keller' , 'Skreli', 'Chandra', 'Bulroth' , 'Randezvous' , "D'zongo", 'Stave']
        active_roster8 = ['Terry', 'Button', 'Guardian', 'Fforde', 'Duncan', 'Andrea', 'Byron Lightning', 'GoodNews', 'Nissa', 'Rossolini' , 'Johnny', 'Oh Cock', 'Masked Admirer']

        select1 = random.randint(0,len(active_roster1)-1)
        player1 = (active_roster1[select1])
        active_roster1[select1] = 0
        select2 = random.randint(0,len(active_roster2)-1)
        player2 = (active_roster2[select2])
        active_roster2[select2] = 0
        select3 = random.randint(0,len(active_roster3)-1)
        player3 = (active_roster3[select3])
        active_roster3[select3] = 0
        select4 = random.randint(0,len(active_roster4)-1)
        player4 = (active_roster4[select4])
        active_roster4[select4] = 0
        select5 = random.randint(0,len(active_roster5)-1)
        player5 = (active_roster5[select5])
        active_roster5[select5] = 0
        select6 = random.randint(0,len(active_roster6)-1)
        player6 = (active_roster6[select6])
        active_roster6[select6] = 0
        select7 = random.randint(0,len(active_roster7)-1)
        player7 = (active_roster7[select7])
        active_roster7[select7] = 0
        select8 = random.randint(0,len(active_roster8)-1)
        player8 = (active_roster8[select8])
        active_roster8[select8] = 0

        active_order = [player1,player2,player3,player4,player5,player6,player7,player8]

        user_order = random.randint(0,8)
        active_order[user_order] = player
        player_team = [''] * 8

        print('The players are:')
        
        for i in range(0,len(active_order)):
            print(active_order[i])

    if gamemode == 'potato' or gamemode == 'potatoteam':
        player = input("Please input a name or type 'sim' to watch the AI play: ")

        roster1 = ['Gregory', 'Spaz', 'Toxic Mankey', 'Gordini', 'Gianni','Tarquini', 'Seb', 'Hairy Beast', 'Whale', 'Gabrielle', 'Nakumura', 'Czechmate', 'Steine']
        roster2 = ['Giovanni', 'Defender', 'Thunder' , 'Snake Eyes', 'Marcello', 'Champion', 'Looney', 'KC', 'Gullwing', 'The Forgotten' , 'Prototyp', 'Louis', 'AJ']
        roster3 = ['Rover Patrol', 'Bow-Wow', 'BigDogge', 'Bubba' , 'Testarossa', 'Kerpelmann', 'Andrew', 'Krissten' , 'Charli', 'THRICE' , 'Leopard' , 'Gerrard' , 'Viper']
        roster4 = ['Partisan', 'Hitman', 'Test Dummy', 'Mountaineer', 'Crystal Castle', 'Peterbuilt', 'Long Face' ,'Threefiddy' , 'Alexis', 'Edisni', 'Davidson' , 'Naghavi', 'Jo']
        roster5 = ['MelB' , 'Mushimoto', 'Cunningham', 'Droopy', 'Aint Skeerd','Mary-Jane', 'XCX' , 'Grundo' , 'Hippopotamus', 'Tarmogoyf' , 'Kreger', 'Fernando', 'Grave Digger']
        roster6 = ['Metroholic' , 'Hariyama', 'twoeasy3', 'M500' , 'Boomz', 'Spacey', 'Saheeli' , 'JiSoo' , 'Jace', 'type_23' ,'Dreamshatterer', 'Heath', 'Snapcaster' ]
        roster7 = ['DTR_Cage', 'Lowe' , 'Panzerkampfwagen', 'Competizione' , 'Giulietta', 'KatEyes', 'Keller' , 'Skreli', 'Chandra', 'Bulroth' , 'Randezvous' , "D'zongo", 'Stave']
        roster8 = ['Terry', 'Button', 'Guardian', 'Fforde', 'Duncan', 'Andrea', 'Byron Lightning', 'GoodNews', 'Nissa', 'Rossolini' , 'Johnny', 'Oh Cock', 'Masked Admirer']

        active_order = [random.choice(roster1),random.choice(roster2),random.choice(roster3),random.choice(roster4),random.choice(roster5),random.choice(roster6),random.choice(roster7),random.choice(roster8)]

        if player == 'sim' or player == 'Sim':
            pass

        elif player != 'sim' or player != 'Sim':
            user_order = random.randint(0,8)
            active_order[user_order] = player
            
        print('The players are:')
            
        if gamemode == 'potatoteam':
            R = '[Red Team] '
            B = '{Blue Team} '
            player_team = [R,B,R,B,R,B,R,B]
            for i in range(0,len(active_order)):
                print(active_order[i] , player_team[i] )
            red_alive = 4
            blue_alive = 4

        else:       
            for i in range(0,len(active_order)):
                print(active_order[i])
            player_team = [''] * 8

       
        active_order_copy = list(active_order)       

        
    print('')      
    print('=====A new game has started!=====')
    if gamemode == 'potatoroyale':
        players_remaining = 100
    if gamemode == 'potato' or gamemode == 'potatogauntlet' or gamemode == 'potatoteam':
        players_remaining = 8   
    user_score = 0
    user_kills = 0
    gauntlet_blowups = 0
    gauntlet_time = 0
    red_win_token = 0
    blue_win_token = 0
    time.sleep(1) ##############time
    a = 1
    b = 0
    current_potato = 0
    first_turn = 1
    potato_coeff = (random.random() + random.random())/2
    if gamemode == 'potatoroyale' or gamemode == 'potato' or gamemode == 'potatoteam':
        potato_time = int(1+potato_coeff*60)
    if gamemode == 'potatogauntlet' :
        potato_time = int(1+potato_coeff*50)
    if gamemode == 'potatogauntlet' or gamemode == 'potato' or gamemode == 'potatoteam':        
        player_score = [0,0,0,0,0,0,0,0]
        player_kills = [0,0,0,0,0,0,0,0]
        player_death_order = [0,0,0,0,0,0,0,0]
    if gamemode == 'potatoroyale':
        player_score = [0] * 100
        player_kills = [0] * 100
        player_death_order = [0] * 100
    recent_explode = 0
    while a ==1:
        num_eliminated = 0
        if gamemode == 'potatoroyale':
            if b == 100:
                b = 0
        elif gamemode == 'potatogauntlet' or gamemode == 'potato' or gamemode == 'potatoteam':
            if b == 8:
                b = 0
            
        if recent_explode == 1 and active_order[b] != 0:
            print('')
            print('~~~A new potato is in play!~~~')
            time.sleep(1) ##############time
        
        if active_order[b] == player:
            if gamemode == 'potatoroyale':
                time.sleep(0.1)
            elif gamemode == 'potatogauntlet' or gamemode == 'potato' or gamemode == 'potatoteam':
                time.sleep(0.5)
            playerholdtimecheck = 0
            while playerholdtimecheck == 0:
                player_holdtime = input('How long do you want to hold the potato? (1-9 seconds)')
                
                try:
                    player_holdtime = int(player_holdtime)
                    if player_holdtime > 0 and player_holdtime < 10:
                        playerholdtimecheck +=1
                        potato_time = potato_time - player_holdtime
                        if potato_time  > 0:
                            print("<" + player + player_team[b] + ' held the potato for', player_holdtime, 'seconds and earned' ,player_holdtime, 'points!>')
                            player_score[b] = player_score[b] + player_holdtime
                            user_score = user_score + player_holdtime
                            gauntlet_time = gauntlet_time + player_holdtime
                            b = b+1
                            recent_explode = 0
                            current_poato = current_potato + player_holdtime
                               
                        elif potato_time <= 0:
                            print('<The potato explodes on you! You are eliminated!>')
                            print('<'+ player + player_team[b] + ' ends the game with', player_score[b],'points.>')
                            player_death_order[b] = players_remaining
                            players_remaining = players_remaining - 1
                            time.sleep(1) ##############time
                            if gamemode == 'potatogauntlet':
                                gauntlet_blowups +=1
                                a = 999999
                            else:
                                potato_coeff = (random.random() + random.random())/2
                                if gamemode == 'potatoroyale':
                                    potato_time = round(1+potato_coeff*60,0)
                                if gamemode == 'potato':
                                    potato_time = round(1+potato_coeff*(20+5*(players_remaining)),0)
                            active_order[b] = 0
                            current_potato = 0
                            kill_check = 0
                            k = b - 1
                            while kill_check == 0:
                                if k <0:
                                    if gamemode == 'potatogauntlet' or gamemode == 'potato' or gamemode == 'potatoteam':
                                        k = 7
                                        pass
                                    if gamemode == 'potatoroyale':
                                        k = 99
                                        pass
                                elif active_order[k] == 0:
                                    k = k - 1
                                else:
                                    if recent_explode == 1:  
                                        kill_check = 1
                                        print('Nobody earns a kill as', player, 'blew up on a new potato.')
                                    else:
                                        player_kills[k] +=1
                                        kill_check = 1
                                        print(active_order[k] + player_team[k] + " earns a kill!")
                            recent_explode = 1
                            b = b+1
                            if gamemode == 'potato' or gamemode == 'potatoroyale' or gamemode == 'potatoteam':
                                print(players_remaining ,'players remain!')
                                if gamemode == 'potatoteam':
                                    if player_team[b] == R:
                                        red_alive -=1
                                    elif player_team[b] == B:
                                        blue_alive -=1
                                    print(red_alive, "red|" ,blue_alive, "blue")
                        else:
                            print('Please input an integer from 1 to 9.')
                except ValueError:
                    print('Please input an integer from 1 to 9.')

        elif active_order[b] == 0:
            b = b +1
            pass                        

        else:
            if gamemode == 'potatoroyale':
                pass
                time.sleep(0.1) ##############time
            elif gamemode == 'potatogauntlet' or gamemode == 'potato' or gamemode == 'potatoteam':
                time.sleep(0.5) ##############time
                pass
            if first_turn == 1:
                AI_holdtime = random.randint(7,9)
            elif recent_explode == 1:
                AI_holdtime = random.randint(7,9)
            else:
                if gamemode == 'potatoroyale':
                    if current_potato > 20:
                        AI_holdtime = random.randint(1,4)                        
                    else:
                        AI_holdtime = random.randint(3,9)
                elif gamemode == 'potatogauntlet':
                    if current_potato > 17:
                        AI_holdtime = random.randint(1,4)                        
                    else:
                        AI_holdtime = random.randint(3,9)
                elif gamemode == 'potato' or gamemode == 'potatoteam':
                    if num_eliminated < 4:
                        if current_potato > (players_remaining)*3 + 2:
                            AI_holdtime = random.randint(1,4)                        
                        else:
                            AI_holdtime = random.randint(3,9)
                    elif num_eliminated == 4:
                        if current_potato > (players_remaining)*3 + 3:
                            AI_holdtime = random.randint(1,4)
                        else:
                            AI_holdtime = random.randint(3,9)
                    elif num_eliminated == 5:
                        if current_potato > (players_remaining)*3 + 4:
                            AI_holdtime = random.randint(1,4)
                        else:
                            AI_holdtime = random.randint(3,9)
                    elif num_eliminated == 6:
                        if current_potato > (players_remaining)*3 + 5:
                            AI_holdtime = random.randint(1,4)
                        else:
                            AI_holdtime = random.randint(3,9)
                    else:
                        AI_holdtime = random.randint(1,9) ##incase something goes wrong
                    

                                           
            potato_time = potato_time - AI_holdtime
            if potato_time > 0:
                print(active_order[b] + player_team[b] + ' held the potato for', AI_holdtime, 'seconds and earned' , AI_holdtime, 'points!')
                player_score[b] = player_score[b] + AI_holdtime
                b = b+1
                current_potato = current_potato + AI_holdtime
                recent_explode = 0
            elif potato_time <=0:
                print('The potato explodes on ' + active_order[b] + player_team[i] + '! They are eliminated!')
                print(active_order[b]+ player_team[i] + ' ends the game with', player_score[b],'points and' , player_kills[b], 'kills.')
                player_death_order[b] = players_remaining
                time.sleep(1) ################time
                potato_coeff = (random.random() + random.random())/2
                if gamemode == 'potatoroyale':
                    potato_time = round(1+potato_coeff*60,0)
                elif gamemode == 'potato' or gamemode == 'potatoteam':
                    potato_time = round(1+potato_coeff*(20+5*(players_remaining)),0)
                elif gamemode == 'potatogauntlet':
                    potato_time = int(1+potato_coeff*50)
                current_potato = 0                
                kill_check = 0
                k = b - 1
                while kill_check == 0:
                    if k <0:
                        if gamemode == 'potatoroyale':
                            k = 99
                        elif gamemode == 'potato' or gamemode == 'potatogauntlet' or gamemode == 'potatoteam':
                            k = 7
                            pass
                    elif active_order[k] == 0:
                        k = k - 1
                    else:
                        if recent_explode == 1:
                            kill_check = 1
                            print('Nobody earns a kill as', active_order[b], 'blew up on a new potato.')
                        else:
                            player_kills[k] +=1
                            kill_check = 1
                            if active_order[k] == player:
                                print("<" + player + player_team[k] + " earns a kill!>")
                            else:
                                print(active_order[k] + player_team[k]+ " earns a kill!")

                if gamemode == 'potatogauntlet':
                    player_score[b] = 0
                    player_kills[b] = 0
                    available_player_check = 0
                    while available_player_check == 0:
                        if b == 0:
                            select_player = random.randint(0,len(active_roster1)-1)
                            if active_roster1[select_player] == 0:
                                pass
                            else:
                                active_order[b] = active_roster1[select_player]
                                active_roster1[select_player] = 0
                                available_player_check = 1
                        elif b == 1:
                            select_player = random.randint(0,len(active_roster2)-1)
                            if active_roster2[select_player] == 0:
                                pass
                            else:
                                active_order[b] = active_roster2[select_player]
                                active_roster2[select_player] = 0
                                available_player_check = 1
                        elif b == 2:
                            select_player = random.randint(0,len(active_roster3)-1)
                            if active_roster3[select_player] == 0:
                                pass
                            else:
                                active_order[b] = active_roster3[select_player]
                                active_roster3[select_player] = 0
                                available_player_check = 1
                        elif b == 3:
                            select_player = random.randint(0,len(active_roster4)-1)
                            if active_roster4[select_player] == 0:
                                pass
                            else:
                                active_order[b] = active_roster4[select_player]
                                active_roster4[select_player] = 0
                                available_player_check = 1
                        elif b == 4:
                            select_player = random.randint(0,len(active_roster5)-1)
                            if active_roster5[select_player] == 0:
                                pass
                            else:
                                active_order[b] = active_roster5[select_player]
                                active_roster5[select_player] = 0
                                available_player_check = 1
                        elif b == 5:
                            select_player = random.randint(0,len(active_roster6)-1)
                            if active_roster6[select_player] == 0:
                                pass
                            else:
                                active_order[b] = active_roster6[select_player]
                                active_roster6[select_player] = 0
                                available_player_check = 1
                        elif b == 6:
                            select_player = random.randint(0,len(active_roster7)-1)
                            if active_roster7[select_player] == 0:
                                pass
                            else:
                                active_order[b] = active_roster7[select_player]
                                active_roster7[select_player] = 0
                                available_player_check = 1
                        elif b == 7:
                            select_player = random.randint(0,len(active_roster8)-1)
                            if active_roster8[select_player] == 0:
                                pass
                            else:
                                active_order[b] = active_roster8[select_player]
                                active_roster8[select_player] = 0
                                available_player_check = 1
                

                    time.sleep(1) ###############time
                    print(active_order[b], 'has entered the game in place of the exploded player!')
                players_remaining = players_remaining - 1
                if gamemode == 'potato' or gamemode == 'potatoroyale' or gamemode == 'potatoteam':
                    active_order[b] = 0
                    print(players_remaining ,'players remain!')
                    if gamemode == 'potatoteam':
                        if player_team[b] == R:
                            red_alive -=1
                        elif player_team[b] == B:
                            blue_alive -=1
                        print(red_alive, "red|" , blue_alive , "blue")
                recent_explode = 1
                b = b+1
        c = 0
        first_turn = 0
        if gamemode == 'potatoroyale' and players_remaining < 2:
            while c<100:            
                if active_order[c] == 0:
                    num_eliminated = num_eliminated + 1
                    c = c+1
                else:
                    last_man = active_order[c]
                    c = c+1
                if num_eliminated == 99:
                    a = 99999
        elif gamemode == 'potato' and players_remaining < 2:
            while c<8:            
                if active_order[c] == 0:
                    num_eliminated = num_eliminated + 1
                    c = c+1
                else:
                    last_man = active_order[c]
                    c = c+1
                if num_eliminated == 7:
                    a = 99999
        elif gamemode == 'potatoteam':
            red_alive = 0
            blue_alive = 0
            while c<8:
                if active_order[c] == 0:
                    num_eliminated = num_eliminated + 1
                    c = c+1
                else:
                    last_man = active_order[c]
                    if player_team[c] == R:
                      red_alive +=1
                    elif player_team[c] == B:
                      blue_alive +=1
                    c = c+1
            if red_alive == 0:
                a = 999999
                blue_win_token = 1                
            elif blue_alive == 0:
                a = 999999
                red_win_token = 1
            
    print('')
    if gamemode == 'potato' or gamemode == 'potatoroyale' or gamemode == 'potatoteam':
        if gamemode != 'potatoteam':
            print("Game over! Last player standing is", last_man + "!")

            player_death_order, active_order_copy, player_score, player_kills, player_team = zip(*sorted(zip(player_death_order, active_order_copy, player_score, player_kills, player_team)))
            player_death_order, active_order_copy, player_score, player_kills, player_team = (list(t) for t in zip(*sorted(zip(player_death_order, active_order_copy, player_score, player_kills, player_team))))

            if active_order[i] !=0:
                print(active_order_copy[i], ":", player_score[i], "points, " , player_kills[i], "kills, ", player_team[i],"Survived")
            if red_win_token == 1:
                print("Red team wins!")
            if blue_win_token == 1:
                print("Blue team wins!")
                          
        else:              
            for i in range(0,len(active_order_copy)):
                if player_death_order[i] == 0:
                    print(active_order_copy[i], ":", player_score[i], "points, " , player_kills[i], "kills, ",  "Survived")
                else:
                    if str(player_death_order[i])[-1] == '1' and player_death_order[i] !=11 :
                        print(active_order_copy[i], ":", player_score[i], "points," , player_kills[i], "kills,", str(player_death_order[i]) +  "st standing")
                    elif str(player_death_order[i])[-1] == '2' and player_death_order[i] !=12 :
                        print(active_order_copy[i], ":", player_score[i], "points," , player_kills[i], "kills,", str(player_death_order[i]) +  "nd standing")
                    elif str(player_death_order[i])[-1] == '3' and player_death_order[i] !=13:
                        print(active_order_copy[i], ":", player_score[i], "points," , player_kills[i], "kills,", str(player_death_order[i]) +  "rd standing")
                    else:
                        print(active_order_copy[i], ":", player_score[i], "points," , player_kills[i], "kills,", str(player_death_order[i]) +  "th standing")
        d = 0
        z = 0
        print('')
        if gamemode != 'potatoteam':
            while z == 0:
                if player_score[d] == max(player_score):
                    print(active_order_copy[d], "is the winner!")
                    z = 1
                else:
                    d = d+1
        print('====================')
    elif gamemode == 'potatogauntlet':
        print("Game over! You got blown up :(")
        print("The Gauntlet claimed" , gauntlet_blowups , "players and a total of", gauntlet_time, "points were scored!")
        print('')
        print('You scored', user_score , 'points and got' ,user_kills , 'kills!')
        print('===========================')

    gamemodeSelectCheck = 0
    while gamemodeSelectCheck == 0:
        print('Select a gamemode to play again:')        
        potato()


print('This is a python version of Hot Potato by yuxiang :)')
print('8 players gather in a circle and pass a hot potato clockwise.')
print('After a certain number of seconds, the hot potato will explode!')
print('Any player holding onto the potato when it explodes will be eliminated.')
print('That player scores no points for the round and play resumes.')
print('Your score will be the total number of seconds holding the potato.')
print('Play for the highest score amongst your opponents :) Good luck!')
print('')
print('Select a gamemode to play:')
potato()
        

                
    
