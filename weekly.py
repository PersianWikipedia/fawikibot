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
        'sql'     : "select distinct log_id, user_name, CONCAT('{{ns:', ar_namespace, '}}:', ar_title) as link, log_comment, str_to_date(left(log_timestamp, 8), '%Y%m%d'), 'حذف تصویر' as issue from logging join user_groups on log_user = ug_user join user on log_user = user_id join archive on log_page = ar_page_id where ug_group = 'eliminator' and log_type = 'delete' and ar_namespace = 6 and log_timestamp >= date_format(date_sub(now(), interval 30 day), '%Y%m%d000000') union select distinct log_id, u.user_name, CONCAT('کاربر:', log_title) as link, log_comment, str_to_date(left(log_timestamp, 8), '%Y%m%d'), 'بستن غیرمجاز' as issue from logging join user_groups ug on log_user = ug.ug_user join user u on log_user = u.user_id join user u2 on log_title = u2.user_name join user_groups ug2 on u2.user_id = ug2.ug_user where ug.ug_group = 'eliminator' and log_type = 'block' and ug2.ug_group in ('sysop', 'bureaucrat', 'patroller', 'autopatrol', 'rollbacker') and log_timestamp >= date_format(date_sub(now(), interval 30 day), '%Y%m%d000000') order by log_id desc",
        'out'     : u'وپ:گزارش دیتابیس/گزارش عملکرد اشتباه ویکی‌بان‌ها',
        'cols'    : [u'شناسه', u'کاربر', u'هدف', u'توضیح', u'تاریخ', u'مشکل'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین صفحه جدولی از فعالیت‌های ویکی‌بان‌ها در یک ماه گذشته را نشان می‌دهد که ممکن است ناقض [[وپ:ویکی‌بان]] باشند. به طور خاص، حذف تصاویر (چک کنید که کاربر دسترسی جداگانه برای حذف تصاویر داشته باشد) و بستن کاربران دارای دسترسی گشت خودکار یا گشت یا واگردان یا مدیر را شناسایی می‌کند \n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| %s || [[کاربر:%s|]] || [[%s]] || <nowiki>%s</nowiki> || {{formatnum:%s|NOSEP}} || {{%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title from categorylinks join page on cl_from = page_id left join imagelinks on il_to = page_title where cl_to = 'پرونده‌های_مالکیت_عمومی' and page_namespace = 6 and il_from is null",
        'out'     : 'وپ:گزارش دیتابیس/پرونده های آزاد استفاده نشده',
        'cols'    : [u'ردیف', u'پرونده'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[:File:%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, str_to_date(left(page_touched,8), '%Y%m%d') from page left join categorylinks on page_id = cl_from where page_namespace = 6 and cl_to is null",
        'out'     : 'وپ:گزارش دیتابیس/پرونده‌های رده‌بندی نشده',
        'cols'    : [u'ردیف', u'پرونده', u'تاریخ بارگذاری'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[:File:%s]] || {{formatnum:%s|NOSEP}}',
        'sign'    : True
        },
        {
        'sql'     : "select ipb_address, ipb_by_text, str_to_date(left(ipb_timestamp,8), '%Y%m%d'), ipb_reason from ipblocks where ipb_expiry = 'infinity' AND ipb_user = 0",
        'out'     : 'وپ:گزارش دیتابیس/آی‌پی‌های بی‌پایان بسته شده',
        'cols'    : [u'ردیف', u'آی‌پی', u'مدیر', u'تاریخ', u'دلیل'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[:بحث کاربر:%s|]] || [[کاربر:%s|]] || {{formatnum:%s|NOSEP}} || %s',
        'sign'    : True
        },
       {
        'sql'     : "select if(up_value = 'male', 'مرد', 'زن'), count(up_value) from user_properties where up_property = 'gender' group by up_value",
        'out'     : 'وپ:گزارش دیتابیس/ترجیحات کاربران/جنسیت',
        'cols'    : [u'جنسیت', u'تعداد'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'',
        'frmt'    : u'| %s || {{formatnum:%s}}',
        'sign'    : False
        },
        {
        'sql'     : "select (mid(up_value, 10, locate('|', mid(up_value,10))-1) / 60) as offset, count(up_value) from user_properties where up_property = 'timecorrection' group by offset order by offset asc",
        'out'     : 'وپ:گزارش دیتابیس/ترجیحات کاربران',
        'cols'    : [u'اختلاف ساعت', u'تعداد'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~\n\n==جنسیت==\n\n{{/جنسیت}}\n\n==منطقه زمانی==\n\n',
        'frmt'    : u'| {{formatnum:%s}} || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title from page left join categorylinks on page_id = cl_from where page_namespace = 0 and page_is_redirect = 0 and cl_from is null",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های رده‌بندی نشده',
        'cols'    : [u'ردیف', u'مقاله'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, str_to_date(left(rev_timestamp, 8), '%Y%m%d') from page join revision on page_latest = rev_id left join pagelinks on page_id = pl_from where page_namespace = 0 and page_is_redirect = 0 and pl_from is null",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های بدون پیوند ویکی',
        'cols'    : [u'ردیف', u'مقاله', u'آخرین ویرایش'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, pl_title from page join pagelinks on page_id = pl_from left join categorylinks on page_id = cl_from and cl_to = 'مقاله‌های_نامزد_حذف_سریع' where page_namespace = 0 and pl_namespace in (2, 3) and cl_to is null",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های دارای پیوند به صفحه کاربری',
        'cols'    : [u'ردیف', u'مقاله', u'پیوند به صفحه (بحث) کاربر'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست شامل صفحه‌هایی که برچسب حذف سریع دارند اما در ردهٔ حذف سریع قرار نگرفته‌اند نیز می‌شود\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[%s]] || [[کاربر:%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select page_namespace, page_title, page_len, str_to_date(left(rev_timestamp, 8), '%Y%m%d') from page join revision on page_latest = rev_id where page_len > 300 * 1024",
        'out'     : 'وپ:گزارش دیتابیس/صفحه‌های پرحجم',
        'cols'    : [u'ردیف', u'مقاله', u'پیوند به صفحه (بحث) کاربر'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[{{ns:%s}}:%s]] || {{formatnum:%s}} || {{formatnum:%s|NOSEP}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title from page join (select rev_page, count(distinct rev_user) as cnt from revision group by rev_page having cnt = 1) singleauth on page_id = rev_page left join pagelinks on pl_title = page_title and pl_namespace = 4 left join templatelinks on tl_title = page_title and tl_namespace = 4 where page_namespace = 4 and page_is_redirect = 0 and pl_title is null and tl_title is null",
        'out'     : 'وپ:گزارش دیتابیس/صفحه‌های پروژه یتیم تک‌نویسنده',
        'cols'    : [u'ردیف', u'صفحه'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[{{ns:4}}:%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select page_title from page join (select rev_page, count(distinct rev_user) as cnt from revision group by rev_page having cnt = 1) singleauth on page_id = rev_page left join pagelinks on pl_title = page_title and pl_namespace = 4 and pl_from <> 1171408 left join templatelinks on tl_title = page_title and tl_namespace = 4 where page_namespace = 4 and page_is_redirect = 0 and pl_title is null and tl_title is null",
        'out'     : 'وپ:گزارش دیتابیس/صفحه‌های پروژه یتیم تک‌نویسنده',
        'cols'    : [u'ردیف', u'صفحه'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[{{ns:4}}:%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select i1.img_name, i2.img_name from image i1 join image i2 on i1.img_sha1 = i2.img_sha1 and i1.img_name > i2.img_name",
        'out'     : 'وپ:گزارش دیتابیس/پرونده‌های تکراری',
        'cols'    : [u'پرونده اول', u'پرونده دوم'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[:پرونده:%s]] || [[:پرونده:%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, count(il_to) cnt from page join categorylinks on page_id = cl_from and cl_to = 'محتویات_غیر_آزاد' join imagelinks on page_title = il_to group by page_title having cnt > 10 order by cnt desc",
        'out'     : 'وپ:گزارش دیتابیس/محتویات غیرآزاد بیش از حد استفاده شده',
        'cols'    : [u'پرونده', u'تعداد کاربردها'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست پرونده‌های غیر آزادی را نشان می‌دهد که بیش از ده بار استفاده شده‌اند.\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[:پرونده:%s]] || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, page_len from page join categorylinks on page_id = cl_from and cl_to = 'همه_مقاله‌های_خرد' where page_len > 10 * 1024 order by page_len desc",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های خرد بلند',
        'cols'    : [u'ردیف', u'مقاله', u'حجم'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که برچسب خرد دارند و دست کم یک کیلوبایت حجم دارند.\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_namespace, page_title from externallinks join page on el_from = page_id where left(el_to, 7) = 'mailto:' and el_to not like '%wikimedia.org%'",
        'out'     : 'وپ:گزارش دیتابیس/صفحه‌های دارای پیوند به رایانامه',
        'cols'    : [u'ردیف', u'صفحه'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست صفحه‌هایی را نشان می‌دهد که پیوند به نشانی ایمیل دارند (اما مواردی که نشانی ایمیل مربوط به خود ویکی‌مدیا است را نشان نمی‌دهد).\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[{{ns:%s}}:%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, str_to_date(left(rev_timestamp, 8), '%Y%m%d') from page join revision on page_latest = rev_id left join categorylinks on page_id = cl_from and cl_to = 'صفحه‌های_ابهام‌زدایی' where page_namespace = 0 and page_is_redirect = 0 and rev_timestamp < concat(date_format(date_sub(now(), interval 4 year), '%Y%m%d'), '000000') and cl_to is null order by rev_timestamp asc",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های فراموش‌شده',
        'cols'    : [u'ردیف', u'صفحه', u'آخرین ویرایش'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که دست کم چهار سال  از آخرین ویرایش‌شان می‌گذرد (به جز صفحه‌های ابهام‌زدایی).\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, page_len from page where page_namespace = 0 and page_len > 20 * 1024 order by page_len desc",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های پرحجم',
        'cols'    : [u'ردیف', u'صفحه', u'حجم'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که دست کم بیست کیلوبایت حجم دارند.\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, page_len from page left join categorylinks on page_id = cl_from and cl_to = 'همه_صفحه‌های_ابهام‌زدایی' where page_namespace = 0 and page_is_redirect = 0 and cl_to is null and page_len < 500 order by page_len",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های کم‌حجم',
        'cols'    : [u'ردیف', u'مقاله', u'حجم'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که زیر پانصد بایت حجم دارند (به جز صفحه های ابهام‌زدایی).\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page.page_namespace, page.page_namespace, noredir, redir, count(page_id) tot from page join (select page_namespace, count(page_id) redir from page where page_is_redirect = 1 group by page_namespace) redir on page.page_namespace = redir.page_namespace join (select page_namespace, count(page_id) noredir from page where page_is_redirect = 0 group by page_namespace) noredir on page.page_namespace = noredir.page_namespace group by page.page_namespace",
        'out'     : 'وپ:گزارش دیتابیس/تعداد صفحه‌های هر فضای نام',
        'cols'    : [u'ردیف', u'شناسه فضای نام', u'عنوان فضای نام', u'بدون تغییرمسیر', u'تغییرمسیر', u'جمع کل'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || %s || {{ns:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_namespace, page_title, page_len from page left join categorylinks on page_id = cl_from and cl_to = 'همه_صفحه‌های_ابهام‌زدایی' join (select rev_page, count(distinct rev_user) cnt from revision group by rev_page having cnt = 1) authors on page_id = rev_page where page_namespace not in (6, 14) and page_is_redirect = 0 and cl_to is null and page_len < 10 order by page_len",
        'out'     : 'وپ:گزارش دیتابیس/صفحه‌های کوتاه تک‌نویسنده',
        'cols'    : [u'ردیف', u'مقاله', u'حجم'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که زیر ده بایت حجم و تنها یک ویرایشگر دارند (به جز صفحه های ابهام‌زدایی).\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[{{ns:%s}}:%s]] || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, il_to from page join imagelinks on il_from = page_id where page_namespace = 0 and il_to not in (select page_title from page where page_namespace = 6) and il_to not in (select page_title from commonswiki_p.page where page_namespace = 6)",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های دارای پیوند به پرونده ناموجود',
        'cols'    : [u'ردیف', u'مقاله', u'پرونده'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که زیر ده بایت حجم و تنها یک ویرایشگر دارند (به جز صفحه های ابهام‌زدایی).\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[%s]] || [[:پرونده:%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select user_name, ifnull(auto.cnt, 0) auto, ifnull(notauto.cnt, 0) noauto, count(log_id) tot from logging join user on user_id = log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'patrol' and log_params like '%auto\";i:1%' or log_params like '%1' group by log_user) auto on logging.log_user = auto.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'patrol' and log_params like '%auto\";i:0%' or log_params like '%0' group by log_user) notauto on logging.log_user = notauto.log_user left join user_groups on user_id = ug_user and ug_group = 'bot' where log_type = 'patrol' and ug_group is null group by logging.log_user order by tot desc, user_id asc",
        'out'     : 'وپ:گزارش دیتابیس/کاربران بر پایه تعداد گشت‌زنی‌ها',
        'cols'    : [u'ردیف', u'کاربر', u'گشت خودکار', u'گشت', u'جمع کل'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nکاربرانی که در حال حاضر برچسب ربات دارند را شامل نمی‌شود.\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select user_name, count(wll_id) gotlove, ifnull(gavelove, 0) from user join wikilove_log on user_id = wll_receiver left join (select wll_sender, count(wll_id) gavelove from wikilove_log group by wll_sender) gavelove on user_id = gavelove.wll_sender group by wll_receiver order by gotlove desc",
        'out'     : 'وپ:گزارش دیتابیس/کاربران بر پایه قدردانی‌ها',
        'cols'    : [u'ردیف', u'کاربر', u'قدردانی از او', u'قدردانی او از دیگران'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nکاربرانی که در حال حاضر برچسب ربات دارند را شامل نمی‌شود.\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select log_title, count(log_id) cnt, ifnull(thankback, 0) from logging left join (select user_name, count(log_id) thankback from logging join user on user_id = log_user where log_type = 'thanks' group by user_name) back on back.user_name = log_title where log_type = 'thanks' group by log_title order by cnt desc",
        'out'     : 'وپ:گزارش دیتابیس/کاربران بر پایه تعداد تشکر',
        'cols'    : [u'ردیف', u'کاربر', u'تشکرها از او', u'تشکرهای او از دیگران'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nکاربرانی که در حال حاضر برچسب ربات دارند را شامل نمی‌شود.\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select user_name, ifnull(del.cnt, 0), ifnull(res.cnt, 0), ifnull(revdel.cnt, 0), ifnull(logdel.cnt, 0), ifnull(prot.cnt, 0), ifnull(unprot.cnt, 0), ifnull(editprot.cnt, 0), ifnull(block.cnt, 0), ifnull(unblock.cnt, 0), ifnull(editblock.cnt, 0), ifnull(renames.cnt, 0), ifnull(rights.cnt, 0), (ifnull(del.cnt, 0) + ifnull(res.cnt, 0) + ifnull(revdel.cnt, 0) + ifnull(logdel.cnt, 0) + ifnull(prot.cnt, 0) + ifnull(unprot.cnt, 0) + ifnull(editprot.cnt, 0) + ifnull(block.cnt, 0) + ifnull(unblock.cnt, 0) + ifnull(editblock.cnt, 0) + ifnull(renames.cnt, 0) + ifnull(rights.cnt, 0)) tot from user join user_groups on user_id = ug_user and ug_group = 'sysop' left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='delete' group by log_user) del on user_id = del.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='restore' group by log_user) res on user_id = res.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='revision' group by log_user) revdel on user_id = revdel.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action = 'event' group by log_user) logdel on user_id = logdel.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'protect' group by log_user) prot on user_id = prot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'unprotect' group by log_user) unprot on user_id = unprot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'modify' group by log_user) editprot on user_id = editprot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'block' group by log_user) block on user_id = block.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'unblock' group by log_user) unblock on user_id = unblock.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'reblock' group by log_user) editblock on user_id = editblock.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'renameuser' group by log_user) renames on user_id = renames.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'rights' and log_action = 'rights' group by log_user) rights on user_id = rights.log_user order by tot desc",
        'out'     : 'وپ:گزارش دیتابیس/فعالیت‌ مدیران کنونی',
        'cols'    : [u'ردیف', u'کاربر', u'حذف', u'احیا', u'حذف نسخه', u'حذف سیاهه', u'محافظت', u'رفع محافظت', u'تغییر محافظت', u'بستن', u'باز کردن', u'تغییر بندایش', u'تغییر نام', u'تغییر اختیارات', u'جمع کل'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select * from (select distinct user_name, ifnull(del.cnt, 0), ifnull(res.cnt, 0), ifnull(revdel.cnt, 0), ifnull(logdel.cnt, 0), ifnull(prot.cnt, 0), ifnull(unprot.cnt, 0), ifnull(editprot.cnt, 0), ifnull(block.cnt, 0), ifnull(unblock.cnt, 0), ifnull(editblock.cnt, 0), ifnull(renames.cnt, 0), ifnull(rights.cnt, 0), (ifnull(del.cnt, 0) + ifnull(res.cnt, 0) + ifnull(revdel.cnt, 0) + ifnull(logdel.cnt, 0) + ifnull(prot.cnt, 0) + ifnull(unprot.cnt, 0) + ifnull(editprot.cnt, 0) + ifnull(block.cnt, 0) + ifnull(unblock.cnt, 0) + ifnull(editblock.cnt, 0) + ifnull(renames.cnt, 0) + ifnull(rights.cnt, 0)) tot from user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='delete' group by log_user) del on user_id = del.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='restore' group by log_user) res on user_id = res.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='revision' group by log_user) revdel on user_id = revdel.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action = 'event' group by log_user) logdel on user_id = logdel.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'protect' group by log_user) prot on user_id = prot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'unprotect' group by log_user) unprot on user_id = unprot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'modify' group by log_user) editprot on user_id = editprot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'block' group by log_user) block on user_id = block.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'unblock' group by log_user) unblock on user_id = unblock.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'reblock' group by log_user) editblock on user_id = editblock.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'renameuser' group by log_user) renames on user_id = renames.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'rights' and log_action = 'rights' group by log_user) rights on user_id = rights.log_user) withzeros where tot > 0 order by tot desc",
        'out'     : 'وپ:گزارش دیتابیس/فعالیت‌های مدیران از ابتدا',
        'cols'    : [u'ردیف', u'کاربر', u'حذف', u'احیا', u'حذف نسخه', u'حذف سیاهه', u'محافظت', u'رفع محافظت', u'تغییر محافظت', u'بستن', u'باز کردن', u'تغییر بندایش', u'تغییر نام', u'تغییر اختیارات', u'جمع کل'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, cnt from enwiki_p.page join (select ll_from, count(ll_lang) cnt from enwiki_p.langlinks group by ll_from having cnt >= 40 and max(ll_lang='fa') = 0) highll on page_id = ll_from where page_namespace = 0 order by cnt desc",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های مهم ایجادنشده بر پایه دیگر میان‌ویکی‌ها',
        'cols'    : [u'ردیف', u'مقاله', u'میان‌ویکی‌ها'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[:en:%s]] || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select page_title, page_len from enwiki_p.page join (select ll_from, count(ll_lang) cnt from enwiki_p.langlinks group by ll_from having max(ll_lang='fa') = 0) highll on page_id = ll_from where page_namespace = 0 and page_len > 150 * 1024 order by page_len desc",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های مهم ایجادنشده بر پایه حجم',
        'cols'    : [u'ردیف', u'مقاله', u'حجم'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست طولانی‌ترین مقاله‌های ویکی‌پدیای انگلیسی را نشان می‌دهد که در ویکی‌پدیای فارسی معادل ندارند (یا دست کم پیوند میان‌ویکی داده نشده‌است).\n\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d}} || [[:en:%s]] || {{formatnum:%s}}',
        'sign'    : True
        },
        {
        'sql'     : "select distinct page_title from page join iwlinks on page_id = iwl_from left join langlinks on page_id = ll_from where page_namespace = 0 and ll_from is null and iwl_prefix not in ('b', 'n', 'q', 's', 'm', 'commons')",
        'out'     : 'وپ:گزارش دیتابیس/مقاله‌های دارای پیوند به ویکی که میان‌ویکی ندارند',
        'cols'    : [u'ردیف', u'الگو'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[%s]]',
        'sign'    : True
        },
        {
        'sql'     : "select cl_to from categorylinks join page on cl_from = page_id where page_title = cl_to and page_namespace = 14",
        'out'     : 'وپ:گزارش دیتابیس/رده‌های حلقوی',
        'cols'    : [u'ردیف', u'رده'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[:رده:%s]]',
        'sign'    : True
        },
        {
        'sql'     : "SELECT page_title FROM page_restrictions JOIN page ON page_id = pr_page AND page_namespace = 0 AND pr_type = 'edit' AND pr_level = 'sysop' AND pr_expiry = 'infinity';",
        'out'     : 'ویکی‌پدیا:گزارش دیتابیس/مقاله‌های دارای محافظت کامل بی‌پایان',
        'cols'    : [u'ردیف', u'مقاله'],
        'summary' : u'به روز کردن آمار',
        'pref'    : u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
        'frmt'    : u'| {{formatnum:%d|NOSEP}} || [[%s]] ',
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

