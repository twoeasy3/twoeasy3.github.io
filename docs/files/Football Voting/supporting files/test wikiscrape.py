import requests

url = 'https://en.wikipedia.org/wiki/Lionel_Messi'
r = requests.get(url)
page_source = r.text
print(page_source) 

url = 
