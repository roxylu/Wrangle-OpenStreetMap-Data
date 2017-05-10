#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib
import md5
import urllib
import random
import json
from utils import set_cache, get_cache


httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
salt = random.randint(32768, 65536)


def make_translation(q, appid, secretKey, fromLang='en', toLang='zh'):

    # try getting the cached translated result from mongodb
    result = get_cache(q)
    if result:
        return result

    # otherwise call baidu tranlste api
    myurl = '/api/trans/vip/translate'
    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.quote(q) + \
        '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + \
        '&sign=' + sign

    try:
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        result = json.loads(response.read())
        value = result['trans_result'][0]['dst']
        set_cache(q, value)
        return value
    except Exception, e:
        print e
