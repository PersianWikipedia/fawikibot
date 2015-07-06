# -*- coding: utf-8 -*-
# Distributed under the terms of MIT License (MIT)
import pywikibot
import re
from pywikibot import pagegenerators
from pywikibot import config
import MySQLdb as mysqldb

def numbertopersian(a):
    a = str(a)
    a = a.replace(u'0', u'۰')
    a = a.replace(u'1', u'۱')
    a = a.replace(u'2', u'۲')
    a = a.replace(u'3', u'۳')
    a = a.replace(u'4', u'۴')
    a = a.replace(u'5', u'۵')
    a = a.replace(u'6', u'۶')
    a = a.replace(u'7', u'۷')
    a = a.replace(u'8', u'۸')
    a = a.replace(u'9', u'۹')
    a = a.replace(u'.', u'٫')
    return a

savetext = u"{{#switch:{{{1|fa}}}"

# sql part
for lang in ["fa", "ar", "cs", "tr", "en", "fr", "de", "it", "az", "fi", "ko", "hu", "he"]:
    site = pywikibot.Site(lang)
    query = "select /* SLOW_OK */ count(rc_title),0 from recentchanges join page on rc_cur_id=page_id where rc_new=1 and rc_namespace=0 and page_is_redirect=0 and page.page_len>70 and rc_deleted=0 and DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY)<rc_timestamp;"

    conn = mysqldb.connect(lang + "wiki.labsdb", db=site.dbName()+ '_p',
                           read_default_file="~/replica.my.cnf")
    cursor = conn.cursor()

    pywikibot.output(u'Executing query:\n%s' % query)
    query = query.encode(site.encoding())
    cursor.execute(query)

    wikinum, numb = cursor.fetchone()
    if wikinum:
        savetext = savetext + u"|" + lang + u"=" + numbertopersian(wikinum)
    else:
        savetext = savetext + u"|" + lang + u"="

# pywikipedia part
savetext = savetext + "}}"
pywikibot.output(savetext)
site = pywikibot.Site()
page = pywikibot.Page(site, u"الگو:سردر تغییرات اخیر/سایر ویکی‌ها")
page.put(savetext, u"ربات: به‌روز رسانی آمار دیگر ویکی‌ها")

