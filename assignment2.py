from __future__ import unicode_literals

import configparser
import os
import sys
import redis
from argparse import ArgumentParser

import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

HOST = "redis-15288.c16.us-east-1-3.ec2.cloud.redislabs.com"
PWD = "TE7ntZzxOTUByAsEbINMBAKVtBq8oROi"
PORT = "15288"
redis1 = redis.Redis(host=HOST, password=PWD, port=PORT)

app = Flask(__name__)

# ref. https://docs.python.org/3/library/configparser.html
config = configparser.ConfigParser()
config.read("config.ini")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', 'c15ac0aa957a0eb2c158fb66dbf70b72')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN',
                                 'nd3QnT44stVAGwLunsHIB8b2h81FXaToEQ7Dr4GmgJPm8blYvdWx1ptq8mWOLU23ER80P3WctDUwyS2nf8lEXYJMThKR+qFKftNmmmco3asMSA6wuqu9N8NKLr1Mu/wj5aavT9RhTeNnrJBf0Wc4VAdB04t89/1O/w1cDnyilFU=')  #

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

# AMAP_API_KEY
AMAP_API_KEY = 'b5b581b926e1a908f35f09094bcf413c'

# Global Count
Count = 0

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
        if isinstance(event, PostbackEvent):
            handle_PosbackEvent(event)
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



# Handler function for PostbackEvent
def handle_PosbackEvent(event):
    global Count

    if "action=question1" in event.postback.data:
        if "ansYes" in event.postback.data:
            Count += 1

        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Question2?',
                actions=[
                    PostbackAction(
                        label='yes',
                        display_text='yes',
                        data='action=question2&ansYes'
                    ),
                    PostbackAction(
                        label='no',
                        display_text='no',
                        data='action=question2&ansNo'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif "action=question2" in event.postback.data:
        if "ansYes" in event.postback.data:
            Count += 1

        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Question3?',
                actions=[
                    PostbackAction(
                        label='yes',
                        display_text='yes',
                        data='action=question3&ansYes'
                    ),
                    PostbackAction(
                        label='no',
                        display_text='no',
                        data='action=question3&ansNo'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif "action=question3" in event.postback.data:
        if "ansYes" in event.postback.data:
            Count += 1

        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Question4?',
                actions=[
                    PostbackAction(
                        label='yes',
                        display_text='yes',
                        data='action=question4&ansYes'
                    ),
                    PostbackAction(
                        label='no',
                        display_text='no',
                        data='action=question4&ansNo'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif "action=question4" in event.postback.data:
        if "ansYes" in event.postback.data:
            Count += 1
            
        msg = f'Postback temCount:：\n {Count}'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg))


    else:
        msg = f'question2 postback temCount:：\n {Count}'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg))


'''
    if "action=question1" in event.postback.data:

        if "Yes" in event.postback.data:
            tempCount += 1

        else:
            tempCount = 100

        TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Question2?',
                actions=[
                    PostbackAction(
                        label='yes',
                        text='yes',
                        data='action=question2&ansYes'
                    ),
                    PostbackAction(
                        label='no',
                        text='no',
                        data='action=question2&ansNo'
                    )
                ]
            )
        )

    elif "action=question2" in event.postback.data:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="TempCount : "+tempCount)
        )

'''









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


def get_news():
    resp = requests.get('https://interface.sina.cn/news/wap/fymap2020_data.d.json')
    jresp = resp.json()
    result_title = jresp['results']['title']  # 这里是个关于title的数组？
    result_summary = jresp['results']['summary']
    result_sourceUrl = jresp['results']['sourceUrl']
    content = ""
    content = f'{result_title}'
    # for index,rs in result_title:
    #    if index == 4:
    #       return content
    #    content += f'{rs}\n\n'
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
        resp = requests.get(
            'https://raw.githubusercontent.com/BlankerL/DXY-COVID-19-Data/master/json/DXYNews-TimeSeries.json')
        jresp = resp.json()

        result_title = []
        result_infoSource = []
        result_sourceUrl = []

        for index, item in enumerate(jresp):
            result_title.append(item['title'])
            result_infoSource.append(item['infoSource'])
            result_sourceUrl.append(item['sourceUrl'])
            if index == 3:
                break

        Carousel_template = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        # http://www.nftitalia.com/wp-content/uploads/2017/07/news-1-1600x429.jpg; https://9auileboys-flywheel.netdna-ssl.com/wp-content/uploads/2019/03/news.jpg
                        thumbnail_image_url='https://9auileboys-flywheel.netdna-ssl.com/wp-content/uploads/2019/03/news.jpg',
                        title=result_title[0],
                        text='Source From: ' + result_infoSource[0],
                        actions=[
                            URITemplateAction(
                                label='Read More',
                                uri='' + result_sourceUrl[0]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://9auileboys-flywheel.netdna-ssl.com/wp-content/uploads/2019/03/news.jpg',
                        title=result_title[1],
                        text='Source From: ' + result_infoSource[1],
                        actions=[
                            URITemplateAction(
                                label='Read More',
                                uri='' + result_sourceUrl[1]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://9auileboys-flywheel.netdna-ssl.com/wp-content/uploads/2019/03/news.jpg',
                        title=result_title[2],
                        text='Source From: ' + result_infoSource[2],
                        actions=[
                            URITemplateAction(
                                label='Read More',
                                # uri='https://www.baidu.com/'
                                uri='' + result_sourceUrl[2]
                            )
                        ]
                    )

                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, Carousel_template)



    elif 'location' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token, LocationSendMessage(
                title='Hospital location',
                address='Hong Kong Baptist Hospital',
                latitude=22.342483,
                longitude=114.191687
            )
        )

    elif 'nearest hospital to' in event.message.text:
        if event.message.text[20:] == "":
            address = "香港浸会大学"
        else:
            address = event.message.text[20:-1]

        addurl1 = 'https://restapi.amap.com/v3/geocode/geo?address={}&output=JSON&key={}'.format(address, AMAP_API_KEY)
        addressReq = requests.get(addurl1)
        addressDoc = addressReq.json()
        location = addressDoc['geocodes'][0]['location']

        addurl2 = 'https://restapi.amap.com/v3/place/around?key={}&location={}&radius=10000&types=090100&extensions=base&offset=3'.format(
            AMAP_API_KEY, location)
        addressReq = requests.get(addurl2)
        addressDoc = addressReq.json()
        sugName0 = addressDoc['pois'][0]['name']
        sugAddress0 = addressDoc['pois'][0]['address']
        sugLocation0 = addressDoc['pois'][0]['location']
        sugName1 = addressDoc['pois'][1]['name']
        sugAddress1 = addressDoc['pois'][1]['address']
        sugLocation1 = addressDoc['pois'][0]['location']
        sugName2 = addressDoc['pois'][2]['name']
        sugAddress2 = addressDoc['pois'][2]['address']
        sugLocation2 = addressDoc['pois'][0]['location']

        l0 = sugLocation0.split(",")
        sloc0Lon = l0[0]
        sloc0Lat = l0[1]
        l1 = sugLocation1.split(",")
        sloc1Lon = l1[0]
        sloc1Lat = l1[1]

        msg = f'为您找到最近的的三家医院及地址：\n 1. {sugName0}  {sugAddress0}\n 2. {sugName1}  {sugAddress1}\n 3. {sugName2}  {sugAddress2}'
        line_bot_api.reply_message(
            event.reply_token,
            # TextSendMessage(msg),
            LocationSendMessage(
                title=f'{sugName0}',
                address=f'{sugAddress0}',
                latitude=sloc0Lat,
                longitude=sloc0Lon),
        )
        '''
        line_bot_api.reply_message(
            event.reply_token,
            #TextSendMessage(msg),
            LocationSendMessage(
                title=f'{sugName1}',
                address=f'{sugAddress1}',
                latitude=sloc1Lat,
                longitude=sloc1Lon)
        )'''




    elif 'real time data' in event.message.text:
        resp = requests.get('https://interface.sina.cn/news/wap/fymap2020_data.d.json')
        jresp = resp.json()
        data_gntotal = jresp['data']['gntotal']
        data_deathtotal = jresp['data']['deathtotal']
        data_curetotal = jresp['data']['curetotal']

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f'Total infected persons number in China :{data_gntotal},\n Death total :{data_deathtotal},\n Cure total :{data_curetotal}'))

    elif event.message.text == "Hello":

        buttons_template = TemplateSendMessage(
            alt_text='start template',
            template=ButtonsTemplate(
                title='Services',
                text='Hi, I am firegod~ What can I help you?',
                thumbnail_image_url='https://cdn.dribbble.com/users/1144347/screenshots/4479125/baymax_dribble.png',
                actions=[
                    MessageTemplateAction(
                        label='Real time news',
                        text='news'
                    ),
                    MessageTemplateAction(
                        label='Real time data',
                        text='real time data'
                    ),
                    MessageTemplateAction(
                        label='Hospital location',
                        text='nearest hospital to'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    elif event.message.text == "redis":
        # Add your code here
        msg = event.message.text
        ans = 'You have input ' + msg
        value = redis1.get(msg)
        if value == None:
            # print('for 1 times')
            ans += ' for 1 times'
            redis1.set(msg, 2)
        else:
            value_int = int(value)
            vt = value_int + 1
            get = redis1.getset(msg, vt)
            ans += 'for ' + get.decode() + ' times'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(ans)
        )

    elif event.message.text == "user id":
        '''
        try:
            profile = line_bot_api.get_profile('<user_id>')
            msg = f'您的ID为：\n{profile.user_id}'
        except LineBotApiError as e:
            e.message
        '''
        user_id = SourceUser.sender_id
        msg = f'您的ID为：\n{user_id}'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg),
        )

    elif "add name:" in event.message.text:
        name = event.message.text[9:]
        user_id = SourceUser.sender_id
        user_id = f'{user_id}'
        redis1.set(user_id, name)
        msg = f'You have set your name as：\n{redis1.get(user_id).decode()}'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg),
        )

    elif event.message.text == "get name":
        user_id = SourceUser.sender_id
        user_id = f'{user_id}'
        msg = redis1.get(user_id)
        if msg == None:
            msg = "You haven't set name, please try add name:<YOUR NAME> first. "
        else:
            msg = msg.decode()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg),
        )

    elif "Hi" in event.message.text:
        user_id = SourceUser.sender_id
        user_id = f'{user_id}'
        msg = redis1.get(user_id)
        if msg == None:
            msg = ''
        else:
            msg = msg.decode()
            msg += "~"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('Hi,' + msg + ' what can help you?')
        )

    elif "self check" in event.message.text:

        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Question1?',
                actions=[
                    PostbackAction(
                        label='yes',
                        display_text='yes',
                        data='action=question1&ansYes'
                    ),
                    PostbackAction(
                        label='no',
                        display_text='no',
                        data='action=question2&ansNo'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)


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



