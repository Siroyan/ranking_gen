# -*- coding: utf-8 -*-
# 画像の編集
from PIL import Image, ImageDraw, ImageFont
import textwrap
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
# スクレイピング
import requests
from bs4 import BeautifulSoup
import re

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
        
        # Yahooニュースのトップ記事を取得
        url = 'https://news.yahoo.co.jp/ranking/access/news'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        elems = soup.find_all(href=re.compile("headlines.yahoo.co.jp"))
        
        # トレンドの文字を貼り付け
        # No1
        font = ImageFont.truetype("./assets/fonts/MPLUSRounded1c-Regular.ttf", size=35)
        wrap_list = textwrap.wrap(elems[0].get_text()[1:], 22)  # テキストを20文字で改行しリストwrap_listに代入
        line_counter = 0  # 行数のカウンター
        for line in wrap_list:  # wrap_listから1行づつ取り出しlineに代入
            y = line_counter * 40 + 250  # y座標をline_counterに応じて下げる
            draw.multiline_text((300, y),line, fill=(9, 64, 103), font=font)  # 1行分の文字列を画像に描画
            line_counter = line_counter + 1  # 行数のカウンターに1
        # No2
        wrap_list = textwrap.wrap(elems[1].get_text()[1:], 22)  # テキストを20文字で改行しリストwrap_listに代入
        line_counter = 0  # 行数のカウンター
        for line in wrap_list:  # wrap_listから1行づつ取り出しlineに代入
            y = line_counter * 40 + 420  # y座標をline_counterに応じて下げる
            draw.multiline_text((300, y),line, fill=(9, 64, 103), font=font)  # 1行分の文字列を画像に描画
            line_counter = line_counter + 1  # 行数のカウンターに1
        # No3
        wrap_list = textwrap.wrap(elems[2].get_text()[1:], 22)  # テキストを20文字で改行しリストwrap_listに代入
        line_counter = 0  # 行数のカウンター
        for line in wrap_list:  # wrap_listから1行づつ取り出しlineに代入
            y = line_counter * 40 + 590  # y座標をline_counterに応じて下げる
            draw.multiline_text((300, y),line, fill=(9, 64, 103), font=font)  # 1行分の文字列を画像に描画
            line_counter = line_counter + 1  # 行数のカウンターに1

        # ランキングの王冠を貼り付け
        # No1
        tmp_no1_image = Image.open('./assets/images/1.png')
        no1_image = tmp_no1_image.resize((tmp_no1_image.width // 3, tmp_no1_image.height // 3), resample=Image.LANCZOS)
        twitter_ranking_image.paste(no1_image, (100, 240))
        # No2
        tmp_no2_image = Image.open('./assets/images/2.png')
        no2_image = tmp_no2_image.resize((tmp_no2_image.width // 3, tmp_no2_image.height // 3), resample=Image.LANCZOS)
        twitter_ranking_image.paste(no2_image, (100, 410))
        # No3
        tmp_no3_image = Image.open('./assets/images/3.png')
        no3_image = tmp_no3_image.resize((tmp_no3_image.width // 3, tmp_no3_image.height // 3), resample=Image.LANCZOS)
        twitter_ranking_image.paste(no3_image, (100, 580))

        image_filepath = './assets/images/yahoo_news_ranking.jpg'
        twitter_ranking_image.save(image_filepath, quality=100)
        await message.channel.send(file=discord.File(image_filepath))

# Botの起動とDiscordサーバーへの接続
client.run(credentials.DISCORD_TOKEN)