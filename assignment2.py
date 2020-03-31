from __future__ import unicode_literals

import configparser
import os
import sys
from argparse import ArgumentParser

import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# (
#   MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, FileMessage, StickerMessage, StickerSendMessage,
#  VideoSendMessage,TemplateSendMessage,ConfirmTemplate,PostbackTemplateAction,MessageTemplateAction
# )
# from bs4 import BeautifulSoup

app = Flask(__name__)

# ref. https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read("config.ini")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET','c15ac0aa957a0eb2c158fb66dbf70b72' ) 
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'nd3QnT44stVAGwLunsHIB8b2h81FXaToEQ7Dr4GmgJPm8blYvdWx1ptq8mWOLU23ER80P3WctDUwyS2nf8lEXYJMThKR+qFKftNmmmco3asMSA6wuqu9N8NKLr1Mu/wj5aavT9RhTeNnrJBf0Wc4VAdB04t89/1O/w1cDnyilFU=')#

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

#AMAP_API_KEY
AMAP_API_KEY = 'b5b581b926e1a908f35f09094bcf413c'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage(event)
        if isinstance(event.message, ImageMessage):
            handle_ImageMessage(event)
        if isinstance(event.message, VideoMessage):
            handle_VideoMessage(event)
        if isinstance(event.message, FileMessage):
            handle_FileMessage(event)
        if isinstance(event.message, StickerMessage):
            handle_StickerMessage(event)

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'




# Handler function for Sticker Message
def handle_StickerMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

# Handler function for Image Message
def handle_ImageMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Nice image!")
    )

# Handler function for Video Message
def handle_VideoMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Nice video!")
    )

# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Nice file!")
    )

# Self check process
def get_news():
    resp = requests.get('https://interface.sina.cn/news/wap/fymap2020_data.d.json')
    jresp = resp.json()
    result_title = jresp['results']['title']  #这里是个关于title的数组？
    result_summary = jresp['results']['summary']
    result_sourceUrl = jresp['results']['sourceUrl']
    content = ""
    content = f'{result_title}'
    #for index,rs in result_title:
    #    if index == 4:
    #       return content
    #    content += f'{rs}\n\n'
    return content

def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 4:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return content

     


# Handler function for Text Message
def handle_TextMessage(event):
    print(event.message.text)
    
    if 'vedio' in event.message.text:
        message = VideoSendMessage(
            original_content_url='https://youtu.be/mOV1aBVYKGA',
            preview_image_url='https://cdn.mos.cms.futurecdn.net/ssZGg3at5Tad2PpEyUCKh3-320-80.jpg'
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif 'call' in event.message.text:
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Are you sure to call for help?',
                actions=[
                    URIAction(
                        label='yes',
                        text='yes',
                        uri='tel:000000'
                    ),
                    MessageTemplateAction(
                        label='no',
                        text='no'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif 'news' in event.message.text:
        resp = requests.get('https://interface.sina.cn/news/wap/fymap2020_data.d.json')
        jresp = resp.json()
        result_title = jresp['results']['title']  #这里是个关于title的数组？
        result_summary = jresp['results']['summary']
        result_sourceUrl = jresp['results']['sourceUrl']

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'Title :{result_title},\n Summary :{result_summary},\n Source Url :{result_sourceUrl}'  ))

    elif event.message.text == "apple news":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))

    elif 'location' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,LocationSendMessage(
                title='Hospital location', 
                address='Hong Kong Baptist Hospital', 
                latitude=22.342483, 
                longitude=114.191687
            )
        )

    elif 'nearest hospitals to' in event.message.text:
        if event.message.text[20:-1] == "":
            address = "香港浸会大学"
        else:
            address = event.message.text[20:-1]

        addurl = 'https://restapi.amap.com/v3/geocode/geo?address={}&output=JSON&key={}'.format(address, AMAP_API_KEY)
        addressReq = request.get(addurl)
        addressDoc = addressReq.json()
        location = addressDoc['geocodes']['location']

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(location)
        )


    elif 'real time data' in event.message.text:
        resp = requests.get('https://interface.sina.cn/news/wap/fymap2020_data.d.json')
        jresp = resp.json()
        data_gntotal = jresp['data']['gntotal']  
        data_deathtotal = jresp['data']['deathtotal']
        data_curetotal = jresp['data']['curetotal']

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'Total infected persons number in China :{data_gntotal},\n Death total :{data_deathtotal},\n Cure total :{data_curetotal}'  ))

    elif event.message.text == "Hello":
        buttons_template = TemplateSendMessage(
            alt_text='start template',
            template=ButtonsTemplate(
                title='Services',
                text='Hi, I am firegod~ What can I help you?',
                thumbnail_image_url='https://cdn.dribbble.com/users/1144347/screenshots/4479125/baymax_dribble.png',
                actions=[
                    MessageTemplateAction(
                        label='Self check',
                        text='self check'
                    ),
                    MessageTemplateAction(
                        label='Real time data',
                        text='real time data'
                    ),
                    MessageTemplateAction(
                        label='Hospital location',
                        text='hospital'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        
    else: 
        msg = 'You said: "' + event.message.text + '" '
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
        )

        
    



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)



