# -*- coding: utf-8 -*-
# Module: default
# Author: MathsGrinds
# Created on: 03.04.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
# --------------------------------------------------------------------------------
# IMPORT
# --------------------------------------------------------------------------------
import os
import sys
import csv
import xbmcaddon
import xbmcgui
import xbmcplugin
import urllib
import requests
import urlparse
from urlparse import parse_qsl
import urllib2
import re
import cookielib
from time import gmtime, strftime
import json
from urllib2 import urlopen
import random
# --------------------------------------------------------------------------------
# Settings
# --------------------------------------------------------------------------------
addon = xbmcaddon.Addon()
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
path = sys.path[0]+"/"
quality = str(addon.getSetting('quality'))
if quality=="SD":
    quality=1
if quality=="HD":
    quality=4
path = sys.path[0]+"/"
# --------------------------------------------------------------------------------
# Scraper
# --------------------------------------------------------------------------------
def Ustvnow(username, password):
    station = {}
    title = {}
    try:
        #xbmc.executebuiltin('Notification(Login, Trying username and password)')
        with requests.Session() as s:
            ### Get CSRF Token ###       
            url="https://watch.ustvnow.com/account/signin"
            r = s.get(url)
            html = r.text
            html = ' '.join(html.split())
            ultimate_regexp = "(?i)<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)\/?>"
            for match in re.finditer(ultimate_regexp, html):
                i = repr(match.group())
                if '<input type="hidden" name="csrf_ustvnow" value="' in i:
                    csrf = i.replace('<input type="hidden" name="csrf_ustvnow" value="','').replace('">','')
                    csrf = str(csrf).replace("u'","").replace("'","")
            ### Get Token ###
            url = "https://watch.ustvnow.com/account/login"
            payload = {'csrf_ustvnow': csrf, 'signin_email': username, 'signin_password':password, 'signin_remember':'1'}
            r = s.post(url, data=payload)
            html = r.text
            html = ' '.join(html.split())
            html = html[html.find('var token = "')+len('var token = "'):]
            html = html[:html.find(';')-1]
            token = str(html)
            ### Get Stream ###
            device = "gtv"        
            url = "http://m-api.ustvnow.com/"+device+"/1/live/login"
            payload = {'username': username, 'password': password, 'device':device}
            r = s.post(url, data=payload)
            html = r.text
            j = json.loads(html)
            result = j['result']
            url = "http://m-api.ustvnow.com/gtv/1/live/playingnow?token="+token
            r = s.get(url)
            html = r.text
            j = json.loads(html)
            n = 0
            while True:
                scode = j['results'][n]['scode']
                stream_code = j['results'][n]['stream_code']
                title[stream_code] = str(j['results'][n]['title'])
                url = "http://m.ustvnow.com/stream/1/live/view?scode="+scode+"&token="+token+"&br_n=Firefox&pr=ec&tr=expired&pl=vjs&pd=1&br_n=Firefox&br_v=54&br_d=desktop"
                r = s.get(url)
                html = r.text
                try:
                    i = json.loads(html)
                except:
                    break
                
                if(quality != "4"):
                    station[stream_code] = (i['stream']).replace("USTVNOW1","USTVNOW"+quality)

                if(quality == "4"):
                    station[stream_code] = (i['stream']).replace("xxx","xxe").replace("USTVNOW1","USTVNOW4")

                if(stream_code == "My9" and quality == "4"):
                    station[stream_code] = (i['stream']).replace("xxe","xxx").replace("USTVNOW4","USTVNOW3")

                n += 1
        return [station, title]
    except:
        xbmc.executebuiltin('Notification(Login Failed, username and/or password is incorrect.)')
        return ""
# --------------------------------------------------------------------------------
# Streams
# --------------------------------------------------------------------------------
def streams():
    username = str(addon.getSetting('email'))
    password = str(addon.getSetting('password'))
    if(username==""):
        #no username given, try predefined username and password
        usernames = usernames = ["jabt@mailed.ro","cslr@kotsu01.info","wdbt@pagamenti.tk","subt@o.cfo2go.ro","tbbt@kusrc.com","libt@uacro.com","cfbt@dfg6.kozow.com","ffbt@phpbb.uu.gl","nulr@at.mycamx.com","mcbt@fls4.gleeze.com","scbt@drivetagdev.com","uhbt@adrianou.gq","idbt@pagamenti.tk","kbbt@kazelink.ml","lcbt@inclusiveprogress.com","uvlr@at.mycamx.com","hbbt@4tb.host","wcbt@hukkmu.tk","jemt@w.0w.ro","pomr@aas.mycamx.com","jcbt@eqiluxspam.ga","adbt@fls4.gleeze.com","nbbt@4tb.host","nbbt@kusrc.com","ebbt@freemail.tweakly.net","rsp@themail.krd.ag","ecbt@hukkmu.tk","rcbt@kusrc.com","gfbt@urfey.com","ucbt@kusrc.com","ndbt@o.spamtrap.ro","cdbt@inclusiveprogress.com","hbbt@caseedu.tk","xgbt@117.yyolf.net","avbt@o.cfo2go.ro","pcbt@hukkmu.tk","edbt@u.dmarc.ro","adbt@eqiluxspam.ga","wdbt@drivetagdev.com","lrqr@mnode.me","ieas@mailfs.com","lebt@dff55.dynu.net","mibt@tvchd.com","qjbt@t.psh.me","cebt@hasanmail.ml","jdbt@eqiluxspam.ga","jdbt@arurgitu.gq","kebt@1clck2.com","pcbt@kusrc.com","hfbt@arur01.tk","yhbt@dfg6.kozow.com","ugbt@laoho.com","iott@szerz.com","fjlr@asm.snapwet.com","xfbt@dff55.dynu.net","wgmt@w.0w.ro","okbt@uacro.com","apps@wierie.tk","ahbt@rudymail.ml","ifbt@yordanmail.cf","bfas@mailfs.com","ffbt@getnowtoday.cf","cdbt@kusrc.com","sfbt@lpo.ddnsfree.com","eebt@cobarekyo1.ml","xdbt@c.andreihusanu.ro","lfbt@pagamenti.tk","zdbt@c.andreihusanu.ro","nfbt@pagamenti.tk","zfbt@lpo.ddnsfree.com","mhbt@rudymail.ml","mzut@oing.cf","lwbt@o.cfo2go.ro","rgbt@getnowtoday.cf","wdbt@bdmuzic.pw","ifbt@s.proprietativalcea.ro","gfbt@lpo.ddnsfree.com","ndbt@mailed.ro","egbt@ppetw.com","lgbt@xing886.uu.gl","lgbt@itmtx.com","dawt@lordsofts.com","cjbt@psles.com","ogbt@cutout.club","vdx@penoto.tk","spor@aw.kikwet.com","yfbt@barryogorman.com","dfbt@kazelink.ml","cjbt@hackersquad.tk","nylr@at.mycamx.com","hjbt@furusato.tokyo","ugbt@nezzart.com","qhbt@fls4.gleeze.com","ilbt@tvchd.com","apor@aw.kikwet.com","fibt@zhcne.com","ygbt@smallker.tk","zgbt@hukkmu.tk","bhbt@o.spamtrap.ro","zibt@itmtx.com","dibt@xing886.uu.gl","tlbt@psles.com","ngbt@e.milavitsaromania.ro","sibt@getnowtoday.cf","jgbt@arurgitu.gq","skbt@rudymail.ml","gibt@itmtx.com","scut@oing.cf","mpor@aw.kikwet.com","twbt@reddit.usa.cc","phbt@cutout.club","ifbt@freemail.tweakly.net","yex@penoto.tk","dmbt@tvchd.com","kijr@morriesworld.ml","qobt@uacro.com","cgbt@4tb.host","fjbt@laoho.com","tibt@p.9q.ro","nlmu@xww.ro","yibt@o.spamtrap.ro","ajbt@poliusraas.tk","wibt@lpo.ddnsfree.com","kkbt@hackersquad.tk","fzbt@o.cfo2go.ro","ikbt@glubex.com","xjbt@ppetw.com","fkbt@rkomo.com","qkmt@w.0w.ro","bhbt@i.xcode.ro","djbt@itmtx.com","hmbt@adrianou.gq","swlr@dwse.edu.pl","uhbt@4tb.host","uibt@e.milavitsaromania.ro","tkbt@zhcne.com","cibt@mail.ticket-please.ga","nibt@lpo.ddnsfree.com","rrpr@aw.kikwet.com","xkbt@zhcne.com","ahbt@kusrc.com","afx@penoto.tk","erut@toon.ml","wkbt@xing886.uu.gl","ngbt@taglead.com","hjbt@dff55.dynu.net","arpr@aw.kikwet.com","klbt@sroff.com","rmbt@phpbb.uu.gl","nlbt@sroff.com","munr@aas.mycamx.com","klbt@117.yyolf.net","xkjr@morriesworld.ml","skbt@e.blogspam.ro","yobt@tvchd.com","ulbt@vssms.com","npbt@uacro.com","ugx@penoto.tk","sbbt@o.cfo2go.ro","aobt@t.psh.me","zjbt@e.milavitsaromania.ro","tibt@mailed.ro","dkbt@dff55.dynu.net","wkbt@s.proprietativalcea.ro","csut@cetpass.com","qlbt@itmtx.com","egx@penoto.tk","bmbt@rkomo.com","mmbt@sroff.com","ribt@caseedu.tk","uomu@xww.ro","ljbt@cobarekyo1.ml","clbt@isdaq.com","fkbt@hasanmail.ml","unbt@dfg6.kozow.com","ijbt@smallker.tk","mnmt@v.0v.ro","albt@pagamenti.tk","rkbt@ucupdong.ml","xmbt@hezll.com","dobt@psles.com","stpr@aw.kikwet.com"]
        random.shuffle(usernames)
        for username in usernames:
            try:
                password = username
                results = Ustvnow(username, password)
                station = results[0]
                title = results[1]
                break
                #success
            except:
                next
                #try again
    else:
        #username given
        results = Ustvnow(username, password)
        station = results[0]
        title = results[1]
    #return streams
    return [
{'name': "ABC - "+title["ABC"], 'thumb': path+'resources/logos/ABC.png', 'link': station["ABC"]},
{'name': "CBS - "+title["CBS"], 'thumb': path+'resources/logos/CBS.png', 'link': station["CBS"]},
{'name': "CW - "+title["CW"], 'thumb': path+'resources/logos/CW.png', 'link': station["CW"]},
{'name': "FOX - "+title["FOX"], 'thumb': path+'resources/logos/FOX.png', 'link': station["FOX"]},
{'name': "NBC - "+title["NBC"], 'thumb': path+'resources/logos/NBC.png', 'link': station["NBC"]},
{'name': "PBS - "+title["PBS"], 'thumb': path+'resources/logos/PBS.png', 'link': station["PBS"]},
{'name': "My9 - "+title["My9"], 'thumb': path+'resources/logos/My9.png', 'link': station["My9"]}
]
# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------
def router(paramstring):
    params = dict(parse_qsl(paramstring[1:]))
    if params:
        if params['mode'] == 'play':
            play_item = xbmcgui.ListItem(path=params['link'])
            xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item)
    else:
        for stream in streams():
            list_item = xbmcgui.ListItem(label=stream['name'], thumbnailImage=stream['thumb'])
            list_item.setProperty('fanart_image', stream['thumb'])
            list_item.setProperty('IsPlayable', 'true')
            url = '{0}?mode=play&link={1}'.format(__url__, stream['link'])
            xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=False)
        xbmcplugin.endOfDirectory(__handle__)
# --------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    router(sys.argv[2])
