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
        'sql'     : "select /* SLOW_OK */ page_title, str_to_date(left(rev_timestamp,8), '%Y%m%d') from page join revision on page_latest = rev_id left join categorylinks on page_id = cl_from where page_namespace = 10 and cl_to is null",
        'out'     : 'وپ:گزارش دیتابیس/الگوهای رده‌بندی نشده',
        'cols'    : [u'ردیف', u'الگو', u'آخرین ویرایش'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| %d || [[الگو:%s]] || %s',
        'sign'    : True
        }
    ]

    for t in tasks:
        bot = stats.StatsBot(t['sql'], t['out'], t['cols'], t['summary'], t['pref'], t['frmt'], t['sign'])
        try:
            bot.run()
        except:
            print sys.exc_info()[0]

if __name__ == "__main__":
    main()

