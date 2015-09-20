#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
weekly.py - a wrapper for stats.py to be called every week.

usage:

    python pwb.py weekly
"""
#
# (C) Pywikibot team, 2006-2014
# (C) w:fa:User:Huji, 2015
#
# Distributed under the terms of the MIT license.
#
from __future__ import unicode_literals

#

import pywikibot
import sys
from scripts import stats


def main():
    tasks = [
        {
        'sql'     : "select /* SLOW_OK */ page_title, cat_pages, cat_subcats, cat_files from page join category on page_title = cat_title left join categorylinks on page_id = cl_from where page_namespace = 14 and cl_from is null",
        'out'     : 'وپ:گزارش دیتابیس/رده‌های رده‌بندی نشده',
        'cols'    : [u'ردیف', u'رده', u'تعداد صفحه‌ها', u'تعداد زیررده‌ها', u'تعداد پرونده‌ها'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[:رده:%s]] || %s || %s || %s',
        'sign'    : True
        },
        {
        'sql'     : "select /* SLOW_OK */ page_title, str_to_date(left(rev_timestamp,8), '%Y%m%d') from page join revision on page_latest = rev_id left join categorylinks on page_id = cl_from where page_namespace = 10 and cl_to is null and page_is_redirect = 0",
        'out'     : 'وپ:گزارش دیتابیس/الگوهای رده‌بندی نشده',
        'cols'    : [u'ردیف', u'الگو', u'آخرین ویرایش'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| %d || [[الگو:%s]] || %s',
        'sign'    : True
        },
        {
        'sql'     : "select /* SLOW OK */ user_name, count(rev_id) cnt from revision join user on rev_user = user_id left join user_groups on rev_user = ug_user and ug_group = 'bot' where ug_group is null group by rev_user order by cnt desc limit 500",
        'out'     : 'وپ:گزارش دیتابیس/کاربران بر اساس تعداد ویرایش‌ها',
        'cols'    : [u'ردیف', u'کاربر', u'تعداد ویرایش'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست ۵۰۰ کاربر دارای بیشترین ویرایش در ویکی‌پدیای فارسی را نشان می‌دهد (شامل ربات‌ها نمی‌شود).\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select user_name, sum(if(page_namespace = 0, 1, 0)) article, sum(if(page_namespace=10, 1, 0)) tpl, sum(if(page_namespace=12, 1, 0)) helppage, sum(if(page_namespace=14, 1, 0)) cat, sum(if(page_namespace=100, 1, 0)) portal, count(rev_first) tot from revision r join (select min(rev_id) rev_first, rev_page from revision group by rev_page) f on r.rev_id = f.rev_first join page on page_id = r.rev_page join user on rev_user = user_id left join user_groups on rev_user = ug_user and ug_group = 'bot' where rev_user > 0 and ug_group is null and page_namespace in (0, 10, 12, 14, 100) group by rev_user order by tot desc limit 200",
        'out'     : 'وپ:گزارش دیتابیس/کاربران ویکی‌پدیا بر پایه تعداد ایجاد صفحه‌ها',
        'cols'    : [u'ردیف', u'کاربر', u'مقاله جدید', u'الگوی جدید', u'راهنمای جدید', u'رده جدید', u'درگاه جدید', u'جمع کل'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
        'sign'    : True
        },
    ]
    ]

    for t in tasks:
        bot = stats.StatsBot(t['sql'], t['out'], t['cols'], t['summary'], t['pref'], t['frmt'], t['sign'])
        try:
            bot.run()
        except:
            print sys.exc_info()[0]

if __name__ == "__main__":
    main()

