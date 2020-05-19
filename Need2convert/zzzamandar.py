#!/usr/bin/python
# -*- coding: utf-8 -*-
# BY: رضا (User:reza1615 on fa.wikipedia)
# Distributed under the terms of the CC-BY-SA 3.0.
import wikipedia
import pagegenerators
from datetime import timedelta,datetime
def NumToPersian(b):
    b=b.replace(u"01",u"ژانویه")
    b=b.replace(u"02",u"فوریه")
    b=b.replace(u"03",u"مارس")
    b=b.replace(u"04",u"آوریل")
    b=b.replace(u"05",u"مه")
    b=b.replace(u"06",u"ژوئن")
    b=b.replace(u"07",u"ژوئیه")
    b=b.replace(u"08",u"اوت")
    b=b.replace(u"09",u"سپتامبر")
    b=b.replace(u"10",u"اکتبر")
    b=b.replace(u"11",u"نوامبر")
    b=b.replace(u"12",u"دسامبر")
    return b

now = str(datetime.now())
my_year=now.split(u'-')[0]
my_month=NumToPersian(now.split(u'-')[1])
my_day=now.split(u'-')[2].split(u' ')[0]
my_date=u'رده:صفحه‌های حذف زمان‌دار در '+my_day+u" "+my_month+u" "+my_year
count=-1
for i in u'۰۱۲۳۴۵۶۷۸۹':
    count+=1
    my_date=my_date.replace(u'0123456789'[count],i)

fapage=wikipedia.Page(wikipedia.getSite("fa"),my_date)
fapage.put(u"{{جا:الگو:شروع حذف زمان‌دار}}",u'ربات:ساخت رده حذف زمان‌دار')