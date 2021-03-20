# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

# APIからデータをもらう

# background color : cream
twitter_ranking_image = Image.new("RGB", (1200, 800), (255, 255, 254))
draw = ImageDraw.Draw(twitter_ranking_image)
# title
font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-ExtraBold.ttf", size=80)
draw.text((60, 50), 'Twitter トレンドランキング', fill=(61, 169, 252), font=font)
# No1
font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-Regular.ttf", size=60)
draw.text((360, 260), '#あいうえおかきくけこ', fill=(9, 64, 103), font=font)
tmp_no1_image = Image.open('./assets/images/no1.png')
no1_image = tmp_no1_image.resize((tmp_no1_image.width // 3, tmp_no1_image.height // 3), resample=Image.LANCZOS)
twitter_ranking_image.paste(no1_image, (180, 240))
# No2
font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-Regular.ttf", size=60)
draw.text((360, 430), '#さしすせそたちつてと', fill=(9, 64, 103), font=font)
tmp_no2_image = Image.open('./assets/images/no2.png')
no2_image = tmp_no2_image.resize((tmp_no2_image.width // 3, tmp_no2_image.height // 3), resample=Image.LANCZOS)
twitter_ranking_image.paste(no2_image, (180, 410))
# No3
font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-Regular.ttf", size=60)
draw.text((360, 600), '#なにぬねのはひふへほ', fill=(9, 64, 103), font=font)
tmp_no3_image = Image.open('./assets/images/no3.png')
no3_image = tmp_no3_image.resize((tmp_no3_image.width // 3, tmp_no3_image.height // 3), resample=Image.LANCZOS)
twitter_ranking_image.paste(no3_image, (180, 580))

twitter_ranking_image.save('./assets/images/hoge.png', quality=100)

# 画像