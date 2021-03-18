import requests

data = open("footballers list.txt",'r')
lista = data.readlines()
data.close()

for player in lista:
    name = player.replace(' ','_')
    name = name[:-1]
    url = 'https://en.wikipedia.org/wiki/' + name
    print(url)
    r = requests.get(url)
    page_source = r.text
    filename = name + '.txt'
    newfile = open(filename,'w',errors='ignore')
    print(page_source, file=newfile)
    newfile.close()


    
