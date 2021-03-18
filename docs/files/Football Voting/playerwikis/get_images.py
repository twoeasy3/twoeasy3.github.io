import os
import urllib.request
for filename in os.listdir(os.getcwd()):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        if filename != 'get_images.py':
            found1 = False
        while found1 == False:
            newline = f.readline()
            newline.strip('/n')
            if '<title>' in newline:
                name = newline[7:-21]
                print(name)
            if '<meta property="og:image"' in newline:
                url = newline[35:-4]
                print(url)
                urllib.request.urlretrieve(url,name+'.jpg')
                found1 = True
