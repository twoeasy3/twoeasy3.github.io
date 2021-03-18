from PIL import Image
import os
path1 = os.path.join(os.getcwd(),"images",'AAA.png')
path2 = os.path.join(os.getcwd(),"images",'BBB.jpg')
im1 = Image.open(path1)
im2 = Image.open(path2)
im_list =[]
im_list.append(im1)
im_list.append(im2)
im_list.append(im1)
im_list.append(im2)

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


get_concat_h_multi_blank([im1, im2, im1,im2]).save('save.jpg')
