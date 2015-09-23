__version__ = "0.2"
__author__ = "Sriram Sundarraj"
__email__ = "ssundarraj@gmail.com"

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import glob
import operator


config = {'id_width': 827, 'id_height': 1165,
          'font': 'assets/kenyan_coffee.ttf',
          'name_coords': (400, 890),'name_font_size': 80, 
          'desig_coords':(20, 880), 'desig_font_size': 40,
          'team_coords':(20, 950), 'team_font_size': 40,
          'overlay':{'2':'assets/blue-2ndyears.png', '3':'assets/green--3rd-years.png', '4':'assets/black-4th-years.png', '5':'assets/black-4th-years.png'},
          'desig':{'2':'Coordinator', '3':'Deputy Manager', '4':'Manager', '5':'Manager'}}


def center_crop(original):
    max_res = max(config['id_width'], config['id_height'])
    resize_size = max_res+600, max_res+600
    original.thumbnail(resize_size, Image.ANTIALIAS)

    width, height = original.size
    left = width / 2 - config['id_width'] / 2
    right = width / 2 + config['id_width'] / 2
    top = height / 2 - config['id_height'] / 2
    bottom = height / 2 + config['id_height'] / 2
    cropped_image = original.crop((left, top, right, bottom))
    return cropped_image


def paste_overlay(cropped_img, overlay_img):
    new_image = cropped_img
    new_image.paste(overlay_img, (0, 0), overlay_img)
    return new_image


def write_text(new_img, text, position=(0, 0), color=(0, 0, 0), font_size=10):
    font = ImageFont.truetype(config['font'], font_size)
    test_img = ImageDraw.Draw(new_img)
    test_img.text(position, text, color, font=font)


def join(image_list, max_x=4, max_y=4):
    full_image_size = (config['id_width'] * max_x, config['id_height'] * max_y)
    full_image = Image.new("RGBA", full_image_size, (256, 256, 256))
    x, y = 0, 0
    for i, img in enumerate(image_list):
        full_image.paste(img, (x, y))
        x += config['id_width']
        if i % max_x == max_x - 1:
            x = 0
            y += config['id_height']
    return full_image


def get_full_list():
    g = glob.glob("images/**/**/*")
    print g
    g = sorted(g) 
    full_list = []
    for i in g:
        path = i
        i = i.split('/')
        full_list.append({'team_name':i[1], 'year':i[2], 'name':i[3].split(".")[0], 'file_path': path})
    return full_list


def pad_field(text, length):
    while len(text) < length:
        text = " " +  text + " "
    return text


# test_img = Image.open("images/Content/2/SANDEEP.JPG")
# cropped_img = center_crop(test_img)
# overlay_img = Image.open("blue-2ndyears.png")
# new_img = paste_overlay(cropped_img, overlay_img)
# write_text(new_img, "This is a test", (0, 0),


full_list = get_full_list()

page_number = 1
while len(full_list):
    page_list = []
    for i in full_list[0:16]:
        test_img = Image.open(i['file_path'])
        overlay_img = Image.open(config['overlay'][i['year']])
        cropped_img = center_crop(test_img)
        new_img = paste_overlay(cropped_img, overlay_img)
        if i['year']=='2':
            font_color = (0, 0, 0)
        else:
            font_color = (256, 256, 256)
        dude_designation = pad_field(config['desig'][i['year']], 20)
        dude_team_name = pad_field(i['team_name'], 20)
        dude_name = pad_field(i['name'], 10)
        print i
        write_text(new_img, dude_designation, config['desig_coords'], font_color, config['desig_font_size'])
        write_text(new_img, dude_team_name, config['team_coords'], font_color, config['team_font_size'])
        write_text(new_img, dude_name, config['name_coords'], font_color, config['name_font_size'])
        page_list.append(new_img)
    page = join(page_list)
    page.show()
    page.save("output/page{0}.jpg".format(page_number))
    page_number += 1
    full_list = full_list[16:]

