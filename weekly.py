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
from scripts import stats

#### commonswiki_p.page
def main():
    tasks = [
        {
            "sqlnum":1,
            "sql":
            "select distinct log_id, user_name, CONCAT(':{{ns:', ar_namespace, '}}:', ar_title) as link, log_comment, str_to_date(left(log_timestamp, 8), '%Y%m%d'), 'حذف تصویر' as issue from logging join user_groups on log_user = ug_user join user on log_user = user_id join archive on log_page = ar_page_id where ug_group = 'eliminator' and log_type = 'delete' and ar_namespace = 6 and log_timestamp >= date_format(date_sub(now(), interval 30 day), '%Y%m%d000000') union select distinct log_id, u.user_name, CONCAT('کاربر:', log_title) as link, log_comment, str_to_date(left(log_timestamp, 8), '%Y%m%d'), 'بستن غیرمجاز' as issue from logging join user_groups ug on log_user = ug.ug_user join user u on log_user = u.user_id join user u2 on log_title = u2.user_name join user_groups ug2 on u2.user_id = ug2.ug_user where ug.ug_group = 'eliminator' and log_type = 'block' and ug2.ug_group in ('sysop', 'bureaucrat', 'patroller', 'autopatrol', 'rollbacker') and log_timestamp >= date_format(date_sub(now(), interval 30 day), '%Y%m%d000000') union select distinct log_id, user_name, log_title as link, log_comment, str_to_date(left(log_timestamp, 8), '%Y%m%d'), 'محافظت کامل' as issue from logging join user_groups on log_user = ug_user join user on log_user = user_id where ug_group = 'eliminator' and log_type = 'protect' and log_action = 'protect' and (log_params not like '%[edit=autoconfirmed]%' and log_params not like '%[create=autoconfirmed]%') order by log_id desc",
            "out": u'وپ:گزارش دیتابیس/گزارش عملکرد اشتباه ویکی‌بان‌ها',
            "cols": [u'شناسه', u'کاربر', u'هدف', u'توضیح', u'تاریخ', u'مشکل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین صفحه جدولی از فعالیت‌های ویکی‌بان‌ها در یک ماه گذشته را نشان می‌دهد که ممکن است ناقض [[وپ:ویکی‌بان]] باشند. مواردی که بررسی می‌کند عبارتند از:\n* حذف تصاویر (با دقت بررسی کنید چون که کاربر دسترسی جداگانه برای حذف تصاویر داشته باشد)\n* بستن کاربران دارای دسترسی گشت خودکار یا گشت یا واگردان یا مدیر\n* محافظت در سطح محافظت کامل و/یا برای بیشتر از یک هفته\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| %s || [[کاربر:%s|]] || [[%s]] || <nowiki>%s</nowiki> || {{formatnum:%s|NOSEP}} || %s',
            "sign": True
        },
    ]

    t = tasks[0]
    test = True

    test = False # Uncomment for initial page update

    if test:
        t['out'] = 'User:Huji/sandbox'
        t['sign'] = True

    bot = stats.StatsBot(t['sql'], t['out'], t['cols'], t['summary'], t['pref'], t['frmt'], t['sign'])
    bot.run()

if __name__ == "__main__":
    main()

