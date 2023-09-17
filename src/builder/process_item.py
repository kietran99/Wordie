from PIL import Image, ImageFont, ImageDraw, ImageShow
import os
from random import shuffle
from functools import reduce

def make_image_file_group(group:list[dict], dir_path:str) -> None:
    for i, item in enumerate(group):
        make_image_file(f'{i:02d}', item, dir_path)

    make_res_image_file([item['word'] for item in group], dir_path)

def make_image_file(file_name:str, item:dict, dir_path:str) -> Image.Image:
    bg_color = (255, 255, 255)
    image_size = (1920, 1080)
    font_size:int = 96
    word_pos = (image_size[0] * 0.5, image_size[1] * 0.5)
    word_color = (0, 0, 0)
    hint_pos = (word_pos[0], word_pos[1] + 240)
    font_color = (0, 0, 0)

    image = Image.new('RGBA', image_size, bg_color)
    font = ImageFont.truetype(os.path.join(os.getcwd(), '..', 'res', "CascadiaCode.ttf"), font_size)
    drawer = ImageDraw.Draw(image)
    scrambled_word:str = scramble_word(item['word'])
    drawer.text(word_pos, text=scrambled_word, fill=word_color, anchor='mm', font=font)
    drawer.text(hint_pos, text=item['hint'], fill=font_color, anchor='mm', font=font)
    image.save(os.path.join(dir_path, f'{file_name}.png'))
    return image

def make_res_image_file(words:list[str], dir_path:str) -> Image.Image:
    bg_color = (255, 255, 255)
    image_size = (1920, 1080)
    font_size:int = 96
    word_gap = 240
    word_pos_list = [
        (image_size[0] * 0.5, image_size[1] * 0.5 - word_gap),
        (image_size[0] * 0.5, image_size[1] * 0.5),
        (image_size[0] * 0.5, image_size[1] * 0.5 + word_gap),
    ]
    word_color = (0, 0, 0)

    image = Image.new('RGBA', image_size, bg_color)
    font = ImageFont.truetype(os.path.join(os.getcwd(), '..', 'res', "CascadiaCode.ttf"), font_size)
    drawer = ImageDraw.Draw(image)
    for i, word in enumerate(words):
        drawer.text(word_pos_list[i], text=word, fill=word_color, anchor='mm', font=font)

    image.save(os.path.join(dir_path, f'res.png'))
    return image

def scramble_word(word:str) -> str:
    chars:list[str] = list(word)
    shuffle(chars)
    slashed_inserted_word:list[str] = reduce(lambda acc, next: f'{acc}/{next}', chars, '')
    scrambled_word = slashed_inserted_word
    return scrambled_word

def log_item(group:list[dict], dir_path:str) -> None:
    print(f"{dir_path} -> {group}")