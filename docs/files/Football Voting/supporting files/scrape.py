data = open("futhead.txt",'r')
line = data.readline()
players = []
while '</html>' not in line:
    if '<span class="player-name">' in line:
        line = line[46:-8]
        players.append(line)
        print(line)
    try:
        line = data.readline()
    except:
        print('error')

print(players)
