#!/usr/bin/env python
"""
Created on 11/07/2017

@author: 'Jiezhi.G@gmail.com'

Reference: 
"""
import json
import os
import time
from urllib import parse

import requests

url = 'http://pvp.qq.com/web201605/wallpaper.shtml'


def get_kog_wallpaper(path):
    headers = {
        'Referer': 'http://pvp.qq.com/web201605/wallpaper.shtml',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'DNT': '1',
    }

    params = (
        ('activityId', '2735'),
        ('sVerifyCode', 'ABCD'),
        ('sDataType', 'JSON'),
        ('iListNum', '200'),
        ('totalpage', '0'),
        ('page', '0'),
        ('iOrder', '0'),
        ('iSortNumClose', '1'),
        ('jsoncallback', 'jQuery17106024178839309091_1568785080871'),
        ('iAMSActivityId', '51991'),
        ('_everyRead', 'true'),
        ('iTypeId', '2'),
        ('iFlowId', '267733'),
        ('iActId', '2735'),
        ('iModuleId', '2735'),
        ('_', int(time.time() * 1000)),
    )

    response = requests.get('http://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi',
                            headers=headers,
                            params=params, verify=False)
    ret = response.text
    ret = ret[ret.index('{'):ret.rindex('}') + 1]
    # print(ret)
    data = json.loads(ret)
    heros = data['List']
    # pprint(parse.unquote(heros))
    if not os.path.exists(path):
        os.mkdir(path)
    for hero in heros:
        file_path = os.path.join(path, '{0}.jpg'.format(parse.unquote(hero['sProdName'])))
        if os.path.exists(file_path):
            continue
        with open(file_path, 'wb') as image_file:
            image_url = parse.unquote(hero['sProdImgNo_6'])
            image_url = image_url.replace("/200", "/0")
            print(image_url)
            image_file.write(requests.get(image_url).content)


if __name__ == '__main__':
    file_dir = 'result/kog/'
    get_kog_wallpaper(file_dir)
