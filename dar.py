#!/usr/bin/python
# -*- coding: utf-8  -*-
# Reza (User:reza1615)
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
import pywikibot
from pywikibot import pagegenerators
import sys
import json
import codecs
from scripts import category
from pywikibot import config
resultdata = u'\n'
faSite = pywikibot.Site('fa')
f = codecs.open("/data/project/dexbot/cache_dar.txt", "r", "utf-8")
cache = json.loads(f.read())
f.close()


def check_user(username):
    username = username.replace(u' ', u'_')
    if cache.get(username):
        return True
    params = {
        'action': 'query',
        'list': 'users',
        'ususers': username,
        'usprop': 'editcount'
    }
    try:
        req = pywikibot.data.api.Request(site=faSite, **params)
        usernamequery = req.submit()
        if usernamequery[u'query'][u'users'][0][u'editcount'] > 3000:
            cache[username] = True
            f = codecs.open("/data/project/dexbot/cache_dar.txt", "w", "utf-8")
            f.write(json.dumps(cache))
            f.close()
            return True
        else:
            return False
    except:
        return False


def move(oldCatTitle, newCatTitle, Last_user):
    comment = u'[[وپ:دار|ربات:انتقال رده]] > [[:رده:%s]] به [[:رده:%s]] به درخواست %s' % (oldCatTitle, newCatTitle, Last_user)
    if Last_user == 'Leyth':
        comment += u'-- با عذرخواهی از ایشان'
    cat = category.CategoryMoveRobot(
        u'رده:' + oldCatTitle, u'رده:' + newCatTitle, batch=True,
        comment=comment, inplace=False, move_oldcat=True,
        delete_oldcat=True, title_regex=None, history=False)
    cat.run()
    #res = {"page_content": "Done"}
    # print json.dumps(res)


def runn(text, Last_user):
    errors = u'\n'
    text = text.replace(u'\r', u'').replace(u']]', u'').replace(u'[[', u'').replace(u'*', u'').replace(u'==>', u'@').replace(u'=>', u'@').replace(u'-->', u'@').replace(
        u'->', u'@').replace(u'>>', u'@').replace(u'>', u'@').replace(u'رده:', u'').replace(u'category:', u'').replace(u'Category:', u'').replace(u'#', u'').strip()
    lines = text.split(u'\n')
    secondsecList = []
    for line in lines:
        if line.strip():
            # print line
            if line.find(u'@') != -1 and line.find(u'کاربر:') == -1 and line.find(u'}}') == -1 and line.find(u'{{') == -1:
                firstsec = line.split(u'@')[0].strip().lstrip(":")
                secondsec = line.split(u'@')[1].strip().lstrip(":")
                # pywikibot.output(u'-----------------------------------')
                #pywikibot.output(u'\03{lightred}'+firstsec+u' > '+secondsec+u'\03{default}')
                facat = pywikibot.Page(faSite, u'رده:' + firstsec)
                if facat:
                    try:
                        facat_text = facat.get()
                    except:
                        continue
                    facat_text = facat_text.replace(u'{{الگو:', u'{{').strip()
                    if facat_text.find(u'{{رده بهتر|') == -1:
                        pass
                        #facat.put(u'{{رده بهتر|'+secondsec+u'}}\n'+facat_text,u'ربات:برچسب رده بهتر برای جلوگیری از کار ربات‌های دیگر به درخواست  %s' % Last_user)
                    secondsec_cat = u"رده:" + secondsec
                    secondsecList.append(secondsec_cat)
                    firstsec_page = pywikibot.Page(faSite, u'رده:' + firstsec)
                    move(firstsec, secondsec, Last_user)

                    facat2 = pywikibot.Page(faSite, secondsec_cat)
                    facat2_text = facat2.get()
                    facat2_text = facat2_text.replace(
                        u'{{الگو:', u'{{').strip()
                    if facat2_text.find(u'{{رده بهتر|') != -1:
                        pass
                        #facat2.put(facat2_text.replace(u'{{رده بهتر|'+facat2_text.split(u'{{رده بهتر|')[1].split(u'}}')[0]+u'}}\n',u''),u'ربات:برداشتن برچسب رده بهتر')

                    facat = pywikibot.Page(faSite, u'رده:' + firstsec)
                    try:
                        pass
                        # facat_text=facat.get()
                        # facat_text=facat_text.replace(u'{{الگو:',u'{{').replace(u'{{template:',u'{{').strip()
                        #facat.put(u"{{حذف سریع|{{قلم رنگ|قرمز تیره|ربات:انتقال‌یافته به [[:رده:"+secondsec+u"]] . '''مدیر محترم:'''}}اگر این رده تغییرمسیر نامناسب است، رده را حذف نمائید. در غیراین صورت برچسب حذف را بردارید تا {{الگو|رده بهتر}} بماند.}}\n{{رده بهتر|"+secondsec+u"}}",u"ربات:افزودن برچسب حذف سریع به ردهٔ انتقال‌یافته. به درخواست  %s" % Last_user)
                        #pywikibot.output(u'\03{lightgreen}...delete tage added to رده:'+firstsec+u' !\03{default}')
                    except:
                        continue
                # except:
                #    errors+=u'*'+firstsec+u'@'+secondsec+u'\n'
    for cat in secondsecList:
        cat_page = pywikibot.Page(faSite, cat)
        text = cat_page.get()
        text = text.replace(u' |', u'|').replace(
            u'| ', u'|').replace(u'{ ', u'{').replace(u' }', u'}')
        text = text.replace(u' |', u'|').replace(
            u'| ', u'|').replace(u'{ ', u'{').replace(u' }', u'}')
        title = cat_page.title()
        res = {}
        title2 = title.replace(u'رده:', u'').replace(
            u'category:', u'').replace(u'Category:', u'')
        if text.find(title2) != -1:
            new_text = text.replace(
                u'{{رده بهتر|' + title + u'}}', u'').replace(u'{{رده بهتر|' + title2 + u'}}', u'')
            if new_text != text:
                cat_page.put(new_text, u'ربات:حذف رده بهتر نادرست')
                #res["page_content"] = "Done"
                # print json.dumps(res)
                #pywikibot.output(u'Bot:removing incorrect template')
    if errors.strip():
        fapage = pywikibot.Page(faSite, u'ویکی‌پدیا:درخواست انتقال رده')
        text = fapage.get()
        fapage.put(text + errors, u'ربات:افزودن موارد انجام نشده!')


def main():
    fapage = pywikibot.Page(faSite, u'ویکی‌پدیا:درخواست انتقال رده')
    try:
        text = fapage.get()
        page_history = fapage.getVersionHistory()
        Last_user = page_history[0][2]
    except pywikibot.IsRedirectPage:
        fapage = fapage.getRedirectTarget()
        try:
            text = fapage.get()
            page_history = fapage.getVersionHistory()
            Last_user = page_history[0][2]
        except:
            #pywikibot.output(u"requested page didn't find!")
            pywikibot.stopme()
            sys.exit()
    except:
        #pywikibot.output(u"requested page didn't find!")
        pywikibot.stopme()
        sys.exit()
    if Last_user != u'Dexbot' and check_user(Last_user):
        fapage.put(u'{{/بالا}}', u'ربات:انتقال رده انجام شد!')
        runn(text, Last_user)
        res = {'result': 'Finished'}
        print json.dumps(res)
    else:
        res = {
            'result': 'Not done. User is not allowed, less than 3000 edits are made by last editing user'}
        print json.dumps(res)
if __name__ == "__main__":
    main()

