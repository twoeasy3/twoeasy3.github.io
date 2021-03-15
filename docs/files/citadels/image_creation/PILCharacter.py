from PIL import Image, ImageDraw, ImageFont

dataset = open('characterImageList','r')
newline = dataset.readline().strip('\n').split('|')
while len(newline) != 0:
    print(newline)
    imgname = 'characterArt/' + newline[3]
    print("imgname:", imgname)
    img = Image.open(imgname, 'r')
    img_w, img_h = img.size
    background = Image.new('RGBA', (430, 738), (255, 255, 255, 255))
    bg_w, bg_h = background.size
    offset = ((0,0))
    background.paste(img, offset,img)
    bordername = 'borderCharacter_' + newline[2] + '.png'
    border = Image.open(bordername, 'r')
    textbox = Image.open('Charactertextbox.png', 'r')
    waxstamp = Image.open('waxstamp.png','r')
    waxoffset = (15,15)
    background.paste(textbox, offset,textbox)
    background.paste(border, offset,border)
    background.paste(waxstamp,waxoffset , waxstamp)
    outputname = 'character_' + newline[0] + '.png'
    background.save(outputname)
    newline = dataset.readline().strip('\n').split('|')
dataset.close()
