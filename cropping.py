from PIL import Image

im = Image.open('./assets/ranking_number.png')

im.crop((0, 0, 227, 227)).save('no1.png', quality=95)
im.crop((343, 0, 343 + 227, 227)).save('no2.png', quality=95)
im.crop((343 + 343, 0, 343 + 343 + 227, 227)).save('no3.png', quality=95)