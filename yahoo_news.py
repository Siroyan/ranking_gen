# -*- coding: utf-8 -*-
# 画像の編集
from PIL import Image, ImageDraw, ImageFont
import discord
import asyncio
# 資格情報
import credentials
# 時間系色々（適当）
import time
import datetime
import dateutil
from dateutil.relativedelta import relativedelta
from datetime import timedelta
# twitterの検索API
import tweepy

# APIの認証
auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

# OAuth認証
api = tweepy.API(auth)

#検索周期の指定(仮に3minに設定)
sincetime = 3

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

@client.event
async def on_message(message):
    if message.content=="$yah-rank":

        # background color : cream
        twitter_ranking_image = Image.new("RGB", (1200, 800), (255, 255, 254))
        draw = ImageDraw.Draw(twitter_ranking_image)
        # title
        font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-ExtraBold.ttf", size=80)
        draw.text((130, 50), 'Yahoo! News ランキング', fill=(255, 0, 39), font=font)
        
        # 日本のトレンドを取得
        woeid = 23424856
        trend = api.trends_place(woeid)[0]
        trends = trend['trends']
        
        # トレンドの文字を貼り付け
        # No1
        font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-Regular.ttf", size=60)
        draw.text((360, 260), trend['trends'][0]['name'], fill=(9, 64, 103), font=font)
        # No2
        font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-Regular.ttf", size=60)
        draw.text((360, 430), trend['trends'][1]['name'], fill=(9, 64, 103), font=font)
        # No3
        font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-Regular.ttf", size=60)
        draw.text((360, 600), trend['trends'][2]['name'], fill=(9, 64, 103), font=font)

        # ランキングの王冠を貼り付け
        # No1
        tmp_no1_image = Image.open('./assets/images/1.png')
        no1_image = tmp_no1_image.resize((tmp_no1_image.width // 3, tmp_no1_image.height // 3), resample=Image.LANCZOS)
        twitter_ranking_image.paste(no1_image, (180, 240))
        # No2
        tmp_no2_image = Image.open('./assets/images/2.png')
        no2_image = tmp_no2_image.resize((tmp_no2_image.width // 3, tmp_no2_image.height // 3), resample=Image.LANCZOS)
        twitter_ranking_image.paste(no2_image, (180, 410))
        # No3
        tmp_no3_image = Image.open('./assets/images/3.png')
        no3_image = tmp_no3_image.resize((tmp_no3_image.width // 3, tmp_no3_image.height // 3), resample=Image.LANCZOS)
        twitter_ranking_image.paste(no3_image, (180, 580))

        image_filepath = './assets/images/yahoo_news_ranking.jpg'
        twitter_ranking_image.save(image_filepath, quality=100)
        await message.channel.send(file=discord.File(image_filepath))

# Botの起動とDiscordサーバーへの接続
client.run(credentials.DISCORD_TOKEN)