from PIL import Image, ImageDraw, ImageFont

dataset = open('imagelist.txt','r')
newline = dataset.readline()
newline = dataset.readline().strip('\n').split('|')
while len(newline) != 0:
    print(newline)
    imgname = 'cardArt/' + newline[3]
    print("imgname:", imgname)
    img = Image.open(imgname, 'r')
    img_w, img_h = img.size
    background = Image.new('RGBA', (430, 600), (255, 255, 255, 255))
    bg_w, bg_h = background.size
    offset = ((0,0))
    background.paste(img, offset,img)
    bordername = 'border_' + newline[1] + '.png'
    border = Image.open(bordername, 'r')
    textbox = Image.open('textbox.png', 'r')
    pearlname = 'pearl_' + newline[1] + '.png'
    pearl = Image.open(pearlname,'r')
    pearloffset = (15,360)
    background.paste(textbox, offset,textbox)
    background.paste(border, offset,border)
    background.paste(pearl, pearloffset,pearl)

    cost = int(newline[2])
    gold = Image.open('gold.png','r')
    goldoffsety = 15
    

    for i in range(0,cost):
        background.paste(gold, (15,goldoffsety) ,gold)
        goldoffsety += 40
    

    number_of_spaces = newline[0].count(' ')
    text_offset = (100,355)
    if number_of_spaces == 0:
        fontsize = 62
    elif number_of_spaces == 1:
        fontsize = 56
        text_offset = (100,360)
    elif number_of_spaces == 2:
        fontsize = 40
        text_offset = (100,365)
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("BLKCHCRY.ttf", fontsize)
    draw.text(text_offset,newline[0],(255,255,255),font=font)
    outputname = 'card_' + newline[0] + '.png'
    background.save(outputname)
    newline = dataset.readline().strip('\n').split('|')
dataset.close()
