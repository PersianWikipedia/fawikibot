#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
weekly.py - a wrapper for stats.py to be called every week.
usage:
    <sqlnum>: For testing specifice sql you can use it's sqlnum argument. it is optional
    python pwb.py weekly <sqlnum>
    Like:
    python pwb.py weekly 2
    or
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
import stats


def main(sqlnum):
    tasks = [
        {
            "sqlnum":1,
            "sql":
            "select distinct log_id, user_name, CONCAT(':{{ns:', ar_namespace, '}}:', ar_title) as link, log_comment, str_to_date(left(log_timestamp, 8), '%Y%m%d'), 'حذف تصویر' as issue from logging join user_groups ug on log_user = ug.ug_user and ug.ug_group = 'eliminator' join user on log_user = user_id join archive on log_page = ar_page_id left join user_groups ug2 on log_user = ug2.ug_user and ug2.ug_group = 'Image-reviewer' where log_type = 'delete' and ar_namespace = 6 and log_timestamp >= date_format(date_sub(now(), interval 30 day), '%Y%m%d000000') and ug2.ug_user is null union select distinct log_id, u.user_name, CONCAT('کاربر:', log_title) as link, log_comment, str_to_date(left(log_timestamp, 8), '%Y%m%d'), 'بستن غیرمجاز' as issue from logging join user_groups ug on log_user = ug.ug_user join user u on log_user = u.user_id join user u2 on log_title = u2.user_name join user_groups ug2 on u2.user_id = ug2.ug_user where ug.ug_group = 'eliminator' and log_type = 'block' and ug2.ug_group in ('sysop', 'bureaucrat', 'patroller', 'autopatrol', 'rollbacker') and log_timestamp >= date_format(date_sub(now(), interval 30 day), '%Y%m%d000000') union select distinct log_id, user_name, log_title as link, log_comment, str_to_date(left(log_timestamp, 8), '%Y%m%d'), 'محافظت کامل' as issue from logging join user_groups on log_user = ug_user join user on log_user = user_id where ug_group = 'eliminator' and log_type = 'protect' and log_action = 'protect' and (log_params not like '%[edit=autoconfirmed]%' and log_params not like '%[create=autoconfirmed]%') order by log_id desc",
            "out": u'وپ:گزارش دیتابیس/گزارش عملکرد اشتباه ویکی‌بان‌ها',
            "cols": [u'شناسه', u'کاربر', u'هدف', u'توضیح', u'تاریخ', u'مشکل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین صفحه جدولی از فعالیت‌های ویکی‌بان‌ها در یک ماه گذشته را نشان می‌دهد که ممکن است ناقض [[وپ:ویکی‌بان]] باشند. مواردی که چک می‌کند عبارتند از:\n* حذف تصاویر (چک کنید که کاربر دسترسی جداگانه برای حذف تصاویر داشته باشد)\n* بستن کاربران دارای دسترسی گشت خودکار یا گشت یا واگردان یا مدیر\n* محافظت در سطح محافظت کامل و/یا برای بیشتر از یک هفته\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| %s || [[کاربر:%s|]] || [[%s]] || <nowiki>%s</nowiki> || {{formatnum:%s|NOSEP}} || %s',
            "sign": True
        },
        {
            "sqlnum":2,
            "sql":
            "select page_title from categorylinks join page on cl_from = page_id left join imagelinks on il_to = page_title where cl_to = 'پرونده‌های_مالکیت_عمومی' and page_namespace = 6 and il_from is null",
            "out": 'وپ:گزارش دیتابیس/پرونده‌های آزاد استفاده نشده',
            "cols": [u'ردیف', u'پرونده'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d|NOSEP}} || [[:File:%s]]',
            "sign": True
        },
        {
            "sqlnum":3,
            "sql":
            "select page_title from categorylinks join page on cl_from = page_id left join imagelinks on il_to = page_title where cl_to = 'محتویات_غیر_آزاد' and page_namespace = 6 and il_from is null",
            "out": 'ویکی‌پدیا:گزارش_دیتابیس/پرونده‌های غیر آزاد استفاده نشده',
            "cols": [u'ردیف', u'پرونده'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d|NOSEP}} || [[:پرونده:%s|]]',
            "sign": True
        },
        {
            "sqlnum":4,
            "sql":
            "select page_title, str_to_date(left(page_touched,8), '%Y%m%d') from page left join categorylinks on page_id = cl_from where page_namespace = 6 and page_is_redirect = 0 and cl_to is null",
            "out": 'وپ:گزارش دیتابیس/پرونده‌های رده‌بندی نشده',
            "cols": [u'ردیف', u'پرونده', u'تاریخ بارگذاری'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[:File:%s]] || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":5,
            "sql":
            "select ipb_address, ipb_by_text, str_to_date(left(ipb_timestamp,8), '%Y%m%d'), ipb_reason from ipblocks where ipb_expiry = 'infinity' AND ipb_user = 0",
            "out": 'وپ:گزارش دیتابیس/آی‌پی‌های بی‌پایان بسته شده',
            "cols": [u'ردیف', u'آی‌پی', u'مدیر', u'تاریخ', u'دلیل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[:بحث کاربر:%s|]] || [[کاربر:%s|]] || {{formatnum:%s|NOSEP}} || %s',
            "sign": True
        },
        {
            "sqlnum":6,
            "sql":
            "select if(up_value = 'male', 'مرد', 'زن'), count(up_value) from user_properties where up_property = 'gender' group by up_value",
            "out": 'وپ:گزارش دیتابیس/ترجیحات کاربران/جنسیت',
            "cols": [u'جنسیت', u'تعداد'],
            "summary": u'به روز کردن آمار',
            "pref": u'',
            "frmt": u'| %s || {{formatnum:%s}}',
            "sign": False
        },
        {
            "sqlnum":7,
            "sql":
            "select (mid(up_value, 10, locate('|', mid(up_value,10))-1) / 60) as offset, count(up_value) from user_properties where up_property = 'timecorrection' group by offset order by offset asc",
            "out": 'وپ:گزارش دیتابیس/ترجیحات کاربران',
            "cols": [u'اختلاف ساعت', u'تعداد'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~\n\n==جنسیت==\n\n{{/جنسیت}}\n\n==منطقه زمانی==\n\n',
            "frmt": u'| {{formatnum:%s}} || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":8,
            "sql":
            "select page_title from page left join categorylinks on page_id = cl_from where page_namespace = 0 and page_is_redirect = 0 and cl_from is null",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های رده‌بندی نشده',
            "cols": [u'ردیف', u'مقاله'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[%s]]',
            "sign": True
        },
        {
            "sqlnum":9,
            "sql":
            "select page_title, str_to_date(left(rev_timestamp, 8), '%Y%m%d') from page join revision on page_latest = rev_id left join pagelinks on page_id = pl_from where page_namespace = 0 and page_is_redirect = 0 and pl_from is null",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های بدون پیوند ویکی',
            "cols": [u'ردیف', u'مقاله', u'آخرین ویرایش'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":10,
            "sql":
            "select page_title, pl_title from page join pagelinks on page_id = pl_from left join categorylinks on page_id = cl_from and cl_to = 'مقاله‌های_نامزد_حذف_سریع' where page_namespace = 0 and pl_namespace in (2, 3) and cl_to is null",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های دارای پیوند به صفحه کاربری',
            "cols": [u'ردیف', u'مقاله', u'پیوند به صفحه (بحث) کاربر'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست شامل صفحه‌هایی که برچسب حذف سریع دارند اما در ردهٔ حذف سریع قرار نگرفته‌اند نیز می‌شود\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[%s]] || [[کاربر:%s]]',
            "sign": True
        },
        {
            "sqlnum":11,
            "sql":
            "select page_namespace, page_title, page_len, str_to_date(left(rev_timestamp, 8), '%Y%m%d') from page join revision on page_latest = rev_id where page_len > 300 * 1024",
            "out": 'وپ:گزارش دیتابیس/صفحه‌های پرحجم',
            "cols": [u'ردیف', u'مقاله', u'پیوند به صفحه (بحث) کاربر'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[{{ns:%s}}:%s]] || {{formatnum:%s}} || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":12,
            "sql":
            "select page_title from page join (select rev_page, count(distinct rev_user) as cnt from revision group by rev_page having cnt = 1) singleauth on page_id = rev_page left join pagelinks on pl_title = page_title and pl_namespace = 4 and pl_from <> 1171408 left join templatelinks on tl_title = page_title and tl_namespace = 4 where page_namespace = 4 and page_is_redirect = 0 and pl_title is null and tl_title is null",
            "out": 'وپ:گزارش دیتابیس/صفحه‌های پروژه یتیم تک‌نویسنده',
            "cols": [u'ردیف', u'صفحه'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[{{ns:4}}:%s]]',
            "sign": True
        },
        {
            "sqlnum":13,
            "sql":
            "select i1.img_name, i2.img_name from image i1 join image i2 on i1.img_sha1 = i2.img_sha1 and i1.img_name > i2.img_name",
            "out": 'وپ:گزارش دیتابیس/پرونده‌های تکراری',
            "cols": [u'پرونده اول', u'پرونده دوم'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[:پرونده:%s]] || [[:پرونده:%s]]',
            "sign": True
        },
        {
            "sqlnum":14,
            "sql":
            "select page_title, count(il_to) cnt from page join categorylinks on page_id = cl_from and cl_to = 'محتویات_غیر_آزاد' join imagelinks on page_title = il_to group by page_title having cnt > 10 order by cnt desc",
            "out": 'وپ:گزارش دیتابیس/محتویات غیرآزاد بیش از حد استفاده شده',
            "cols": [u'پرونده', u'تعداد کاربردها'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست پرونده‌های غیر آزادی را نشان می‌دهد که بیش از ده بار استفاده شده‌اند.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[:پرونده:%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":15,
            "sql":
            "select page_title, page_len from page join categorylinks on page_id = cl_from and cl_to = 'همه_مقاله‌های_خرد' where page_len > 10 * 1024 order by page_len desc",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های خرد بلند',
            "cols": [u'ردیف', u'مقاله', u'حجم'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که برچسب خرد دارند و دست کم یک کیلوبایت حجم دارند.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":16,
            "sql":
            "select page_namespace, page_title from externallinks join page on el_from = page_id where left(el_to, 7) = 'mailto:' and el_to not like '%wikimedia.org%'",
            "out": 'وپ:گزارش دیتابیس/صفحه‌های دارای پیوند به رایانامه',
            "cols": [u'ردیف', u'صفحه'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست صفحه‌هایی را نشان می‌دهد که پیوند به نشانی ایمیل دارند (اما مواردی که نشانی ایمیل مربوط به خود ویکی‌مدیا است را نشان نمی‌دهد).\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[{{ns:%s}}:%s]]',
            "sign": True
        },
        {
            "sqlnum":17,
            "sql":
            "select page_title, str_to_date(left(rev_timestamp, 8), '%Y%m%d') from page join revision on page_latest = rev_id left join categorylinks on page_id = cl_from and cl_to = 'صفحه‌های_ابهام‌زدایی' where page_namespace = 0 and page_is_redirect = 0 and rev_timestamp < concat(date_format(date_sub(now(), interval 4 year), '%Y%m%d'), '000000') and cl_to is null order by rev_timestamp asc",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های فراموش‌شده',
            "cols": [u'ردیف', u'صفحه', u'آخرین ویرایش'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که دست کم چهار سال  از آخرین ویرایش‌شان می‌گذرد (به جز صفحه‌های ابهام‌زدایی).\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":18,
            "sql":
            "select page_title, page_len from page where page_namespace = 0 and page_len > 20 * 1024 order by page_len desc",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های پرحجم',
            "cols": [u'ردیف', u'صفحه', u'حجم'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که دست کم بیست کیلوبایت حجم دارند.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":19,
            "sql":
            "select page_title, page_len from page left join categorylinks on page_id = cl_from and cl_to in ('همه_صفحه‌های_ابهام‌زدایی', 'نام‌های_کوچک','نام‌های_خانوادگی', 'همه_مقاله‌های_مجموعه‌نمایه') where page_namespace = 0 and page_is_redirect = 0 and cl_to is null and page_len < 500 order by page_len",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های کم‌حجم',
            "cols": [u'ردیف', u'مقاله', u'حجم'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که زیر پانصد بایت حجم دارند (به جز صفحه های ابهام‌زدایی).\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":20,
            "sql":
            "select page.page_namespace, page.page_namespace, noredir, redir, count(page_id) tot from page join (select page_namespace, count(page_id) redir from page where page_is_redirect = 1 group by page_namespace) redir on page.page_namespace = redir.page_namespace join (select page_namespace, count(page_id) noredir from page where page_is_redirect = 0 group by page_namespace) noredir on page.page_namespace = noredir.page_namespace group by page.page_namespace",
            "out": 'وپ:گزارش دیتابیس/تعداد صفحه‌های هر فضای نام',
            "cols":
            [u'ردیف',
             u'شناسه فضای نام',
             u'عنوان فضای نام',
             u'بدون تغییرمسیر',
             u'تغییرمسیر',
             u'جمع کل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || %s || {{ns:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":21,
            "sql":
            "select page_namespace, page_title, page_len from page left join categorylinks on page_id = cl_from and cl_to = 'همه_صفحه‌های_ابهام‌زدایی' join (select rev_page, count(distinct rev_user) cnt from revision group by rev_page having cnt = 1) authors on page_id = rev_page where page_namespace not in (6, 14) and page_is_redirect = 0 and page_namespace in (0, 4, 12) and cl_to is null and page_len < 10 order by page_len",
            "out": 'وپ:گزارش دیتابیس/صفحه‌های کوتاه تک‌نویسنده',
            "cols": [u'ردیف', u'صفحه', u'حجم'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست صفحه‌هایی در فضای نام مقاله، ویکی‌پدیا یا راهنما را نشان می‌دهد که زیر ده بایت حجم و تنها یک ویرایشگر دارند (به جز صفحه های ابهام‌زدایی).\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[{{ns:%s}}:%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":22,
            "sql":
            "select page_title, il_to from page join imagelinks on il_from = page_id where page_namespace = 0 and il_to not in (select page_title from page where page_namespace = 6) and il_to not in (select page_title from commonswiki_p.page where page_namespace = 6) limit 10000",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های دارای پیوند به پرونده ناموجود',
            "cols": [u'ردیف', u'مقاله', u'پرونده'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست حداکثر ده‌هزارتا از مقاله‌هایی را نشان می‌دهد که زیر ده بایت حجم و تنها یک ویرایشگر دارند (به جز صفحه های ابهام‌زدایی).\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[%s]] || [[:پرونده:%s]]',
            "sign": True
        },
        {
            "sqlnum":23,
            "sql":
            "select user_name, ifnull(auto.cnt, 0) auto, ifnull(notauto.cnt, 0) noauto, count(log_id) tot from logging join user on user_id = log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'patrol' and log_params like '%auto\";i:1%' or log_params like '%1' group by log_user) auto on logging.log_user = auto.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'patrol' and log_params like '%auto\";i:0%' or log_params like '%0' group by log_user) notauto on logging.log_user = notauto.log_user left join user_groups on user_id = ug_user and ug_group = 'bot' where log_type = 'patrol' and ug_group is null group by logging.log_user order by tot desc, user_id asc",
            "out": 'وپ:گزارش دیتابیس/کاربران بر پایه تعداد گشت‌زنی‌ها',
            "cols": [u'ردیف', u'کاربر', u'گشت خودکار', u'گشت', u'جمع کل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nکاربرانی که در حال حاضر برچسب ربات دارند را شامل نمی‌شود.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":24,
            "sql":
            "select user_name, count(wll_id) gotlove, ifnull(gavelove, 0) from user join wikilove_log on user_id = wll_receiver left join (select wll_sender, count(wll_id) gavelove from wikilove_log group by wll_sender) gavelove on user_id = gavelove.wll_sender group by wll_receiver order by gotlove desc",
            "out": 'وپ:گزارش دیتابیس/کاربران بر پایه قدردانی‌ها',
            "cols":
            [u'ردیف', u'کاربر', u'قدردانی از او', u'قدردانی او از دیگران'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nکاربرانی که در حال حاضر برچسب ربات دارند را شامل نمی‌شود.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":25,
            "sql":
            "select log_title, count(log_id), ifnull(thankback, 0), count(log_id) + ifnull(thankback, 0) as cnt from logging left join (select user_name, count(log_id) thankback from logging join user on user_id = log_user where log_type = 'thanks' group by user_name) back on back.user_name = replace(log_title, '_', ' ') where log_type = 'thanks' group by log_title order by cnt desc",
            "out": 'وپ:گزارش دیتابیس/کاربران بر پایه تعداد تشکر',
            "cols":
            [u'ردیف',
             u'کاربر',
             u'تشکرها از او',
             u'تشکرهای او از دیگران',
             u'جمع کل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":26,
            "sql":
            "select user_name, ifnull(del.cnt, 0), ifnull(res.cnt, 0), ifnull(revdel.cnt, 0), ifnull(logdel.cnt, 0), ifnull(prot.cnt, 0), ifnull(unprot.cnt, 0), ifnull(editprot.cnt, 0), ifnull(block.cnt, 0), ifnull(unblock.cnt, 0), ifnull(editblock.cnt, 0), ifnull(renames.cnt, 0), ifnull(rights.cnt, 0), (ifnull(del.cnt, 0) + ifnull(res.cnt, 0) + ifnull(revdel.cnt, 0) + ifnull(logdel.cnt, 0) + ifnull(prot.cnt, 0) + ifnull(unprot.cnt, 0) + ifnull(editprot.cnt, 0) + ifnull(block.cnt, 0) + ifnull(unblock.cnt, 0) + ifnull(editblock.cnt, 0) + ifnull(renames.cnt, 0) + ifnull(rights.cnt, 0)) tot from user join user_groups on user_id = ug_user and ug_group = 'sysop' left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='delete' group by log_user) del on user_id = del.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='restore' group by log_user) res on user_id = res.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='revision' group by log_user) revdel on user_id = revdel.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action = 'event' group by log_user) logdel on user_id = logdel.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'protect' group by log_user) prot on user_id = prot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'unprotect' group by log_user) unprot on user_id = unprot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'modify' group by log_user) editprot on user_id = editprot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'block' group by log_user) block on user_id = block.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'unblock' group by log_user) unblock on user_id = unblock.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'reblock' group by log_user) editblock on user_id = editblock.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'renameuser' group by log_user) renames on user_id = renames.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'rights' and log_action = 'rights' group by log_user) rights on user_id = rights.log_user order by tot desc",
            "out": 'وپ:گزارش دیتابیس/فعالیت‌ مدیران کنونی',
            "cols": [u'ردیف', u'کاربر', u'حذف', u'احیا', u'حذف نسخه', u'حذف سیاهه', u'محافظت', u'رفع محافظت',
                     u'تغییر محافظت', u'بستن', u'باز کردن', u'تغییر بندایش', u'تغییر نام', u'تغییر اختیارات', u'جمع کل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":27,
            "sql":
            "select * from (select distinct user_name, ifnull(del.cnt, 0), ifnull(res.cnt, 0), ifnull(revdel.cnt, 0), ifnull(logdel.cnt, 0), ifnull(prot.cnt, 0), ifnull(unprot.cnt, 0), ifnull(editprot.cnt, 0), ifnull(block.cnt, 0), ifnull(unblock.cnt, 0), ifnull(editblock.cnt, 0), ifnull(renames.cnt, 0), ifnull(rights.cnt, 0), (ifnull(del.cnt, 0) + ifnull(res.cnt, 0) + ifnull(revdel.cnt, 0) + ifnull(logdel.cnt, 0) + ifnull(prot.cnt, 0) + ifnull(unprot.cnt, 0) + ifnull(editprot.cnt, 0) + ifnull(block.cnt, 0) + ifnull(unblock.cnt, 0) + ifnull(editblock.cnt, 0) + ifnull(renames.cnt, 0) + ifnull(rights.cnt, 0)) tot from user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='delete' group by log_user) del on user_id = del.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='restore' group by log_user) res on user_id = res.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action='revision' group by log_user) revdel on user_id = revdel.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'delete' and log_action = 'event' group by log_user) logdel on user_id = logdel.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'protect' group by log_user) prot on user_id = prot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'unprotect' group by log_user) unprot on user_id = unprot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'protect' and log_action = 'modify' group by log_user) editprot on user_id = editprot.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'block' group by log_user) block on user_id = block.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'unblock' group by log_user) unblock on user_id = unblock.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'block' and log_action = 'reblock' group by log_user) editblock on user_id = editblock.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'renameuser' group by log_user) renames on user_id = renames.log_user left join (select log_user, count(log_id) cnt from logging where log_type = 'rights' and log_action = 'rights' group by log_user) rights on user_id = rights.log_user) withzeros where tot > 0 order by tot desc",
            "out": 'وپ:گزارش دیتابیس/فعالیت‌های مدیران از ابتدا',
            "cols": [u'ردیف', u'کاربر', u'حذف', u'احیا', u'حذف نسخه', u'حذف سیاهه', u'محافظت', u'رفع محافظت',
                     u'تغییر محافظت', u'بستن', u'باز کردن', u'تغییر بندایش', u'تغییر نام', u'تغییر اختیارات', u'جمع کل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}} || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":28,
            "sql":
            "select page_title, cnt from enwiki_p.page join (select ll_from, count(ll_lang) cnt from enwiki_p.langlinks group by ll_from having cnt >= 40 and max(ll_lang='fa') = 0) highll on page_id = ll_from where page_namespace = 0 order by cnt desc",
            "out":
            'وپ:گزارش دیتابیس/مقاله‌های مهم ایجادنشده بر پایه دیگر میان‌ویکی‌ها',
            "cols": [u'ردیف', u'مقاله', u'میان‌ویکی‌ها'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[:en:%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":29,
            "sql":
            "select page_title, page_len from enwiki_p.page join (select ll_from, count(ll_lang) cnt from enwiki_p.langlinks group by ll_from having max(ll_lang='fa') = 0) highll on page_id = ll_from where page_namespace = 0 and page_len > 150 * 1024 order by page_len desc",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های مهم ایجادنشده بر پایه حجم',
            "cols": [u'ردیف', u'مقاله', u'حجم'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست طولانی‌ترین مقاله‌های ویکی‌پدیای انگلیسی را نشان می‌دهد که در ویکی‌پدیای فارسی معادل ندارند (یا دست کم پیوند میان‌ویکی داده نشده‌است).\n\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d}} || [[:en:%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":30,
            "sql":
            "select distinct page_title from page join iwlinks on page_id = iwl_from left join langlinks on page_id = ll_from where page_namespace = 0 and ll_from is null and iwl_prefix not in ('b', 'n', 'q', 's', 'm', 'wikt', 'commons', 'wikispecies')",
            "out":
            'وپ:گزارش دیتابیس/مقاله‌های دارای پیوند به ویکی که میان‌ویکی ندارند',
            "cols": [u'ردیف', u'الگو'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d|NOSEP}} || [[%s]]',
            "sign": True
        },
        {
            "sqlnum":31,
            "sql":
            "select cl_to from categorylinks join page on cl_from = page_id where page_title = cl_to and page_namespace = 14",
            "out": 'وپ:گزارش دیتابیس/رده‌های حلقوی',
            "cols": [u'ردیف', u'رده'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d|NOSEP}} || [[:رده:%s]]',
            "sign": True
        },
        {
            "sqlnum":32,
            "sql":
            "select page_title FROM page_restrictions JOIN page ON page_id = pr_page AND page_namespace = 0 AND pr_type = 'edit' AND pr_level = 'sysop' AND pr_expiry = 'infinity'",
            "out":
            'ویکی‌پدیا:گزارش دیتابیس/مقاله‌های دارای محافظت کامل بی‌پایان',
            "cols": [u'ردیف', u'مقاله'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt": u'| {{formatnum:%d|NOSEP}} || [[%s]] ',
            "sign": True
        },
        {
            "sqlnum":33,
            "sql":
            "select page_title, count(ll_lang) from page join category on page_title = cat_title left join categorylinks on page_title = cl_to left join templatelinks on tl_from = page_id and tl_namespace = 10 and tl_title in ('رده_خالی' , 'رده_بهتر', 'رده_ابهام‌زدایی', 'رده_ردیابی‌کردن') left join langlinks on page_id = ll_from where page_namespace = 14 and page_is_redirect = 0 and cl_to is null and tl_title is null group by page_title",
            "out": 'وپ:گزارش دیتابیس/رده‌های خالی',
            "cols": [u'ردیف', u'رده', u'تعداد میان‌ویکی'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[:رده:%s]] || {{formatnum:%s|}}',
            "sign": True
        },
        {
            "sqlnum":34,
            "sql":
            "select ipb_address, mid(ipb_address, instr(ipb_address, '/') + 1) as cnt, ipb_by_text, ipb_timestamp, ipb_expiry, ipb_reason from ipblocks where ipb_address like '%/%'",
            "out": 'ویکی‌پدیا:گزارش_دیتابیس/محدوده_آی‌پی‌های_بسته‌شده',
            "cols":
            [u'ردیف',
             u'بازه',
             u'تعداد آی‌پی',
             u'مدیر',
             u'تاریخ بستن',
             u'انقضا',
             u'دلیل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || %s || {{formatnum:%s|NOSEP}} || [[کاربر:%s]] || {{formatnum:%s|NOSEP}} || {{formatnum:%s|NOSEP}} || %s',
            "sign": True
        },
        {
            "sqlnum":35,
            "sql":
            "select page_title, il_to from page join imagelinks on page_id = il_from where (not exists (select 1 from image where img_name = il_to)) and (not exists (select 1 from commonswiki_p.page where page_title = il_to and page_namespace = 6)) and (not exists (select 1 from page where page_title = il_to and page_namespace = 6)) and page_namespace = 10",
            "out":
            'ویکی‌پدیا:گزارش_دیتابیس/الگوهای دارای پیوند به پروندهای ناموجود',
            "cols": [u'ردیف', u'الگو', u'پرونده'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[الگو:%s|]] || [[:پرونده:%s]]',
            "sign": True
        },
        {
            "sqlnum":36,
            "sql":
            "select tl_title, count(*) from templatelinks where tl_namespace = 10 group by tl_title order by count(*) desc limit 1000",
            "out": 'ویکی‌پدیا:گزارش_دیتابیس/الگوهای دارای بیشترین تراگنجایش',
            "cols": [u'ردیف', u'الگو', u'تعداد تراگنجایش'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین صفحه فهرست ۱۰۰۰ الگوی دارای بیشترین تراگنجایش را نشان می‌دهد.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[الگو:%s|]] || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":37,
            "sql":
            "select tl_title, count(*) from page join templatelinks on page_title = tl_title and page_namespace = tl_namespace left join page_restrictions on pr_page = page_id and pr_level in ('sysop', 'autoconfirmed') and pr_type = 'edit' where tl_namespace = 10 and pr_page is null group by tl_title having count(*) > 500 order by count(*) desc",
            "out": 'ویکی‌پدیا:گزارش_دیتابیس/الگوهای پرکاربرد بدون محافظت',
            "cols": [u'ردیف', u'الگو', u'تعداد تراگنجایش'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین صفحه فهرست الگوی دارای دست کم ۵۰۰ تراگنجایش را نشان می‌دهد که محافظت نشده‌اند.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[الگو:%s|]] || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":38,
            "sql":
            "select page_title, (select count(*) from imagelinks where il_to = page_title) as imagelinks, (select count(*) from pagelinks where pl_namespace = 6 and pl_title = page_title) as links from page where page_namespace = 6 and page_is_redirect = 1 having imagelinks + links <= 1",
            "out":
            'ویکی‌پدیا:گزارش_دیتابیس/صفحه‌های بدون استفاده تغییرمسیر پرونده',
            "cols":
            [u'ردیف',
             u'صفحه پرونده',
             u'تعداد تراگنجایش',
             u'تعداد پیوند ورودی'],
            "summary": u'به روز کردن آمار',
            "pref": u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[:پرونده:%s|]] || {{formatnum:%s|NOSEP}} || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":39,
            "sql":
            "select user_name, sum(img_size) as tot from image join user on img_user = user_id group by img_user order by tot desc limit 500",
            "out":
            'وپ:گزارش دیتابیس/کاربران برپایه مقدار حجم پرونده بارگذاری شده',
            "cols": [u'ردیف', u'کاربر', u'حجم کل (بایت)'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست ۵۰۰ کاربر دارای بیشترین حجم بارگذاری در ویکی‌پدیای فارسی را نشان می‌دهد.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":40,
            "sql":
            "select u1.user_name blockee, u2.user_name blocker, replace(str_to_date(ipb_timestamp, '%Y%m%d%H%i%s'), 'T', ' ساعت ') blocktime, replace(str_to_date(ipb_expiry, '%Y%m%d%H%i%s'), 'T', ' ساعت ') blockend, ipb_reason from ipblocks join user u1 on ipb_user = u1.user_id join user u2 on ipb_by = u2.user_id where ipb_user <> 0 and ipb_expiry not in ('infinity', 'indefinite') and ipb_expiry > concat(date_format(now(), '%Y%m%d'), '000000')",
            "out": 'وپ:گزارش دیتابیس/کاربران بسته شده',
            "cols":
            [u'ردیف',
             u'کاربر هدف',
             u'مجری',
             u'شروع قطع دسترسی',
             u'پایان قطع دسترسی',
             u'دلیل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست کاربرانی را نشان می‌دهد که در زمان ثبت آمار دسترسی‌شان برای مدتی مشخص قطع شده بوده‌است. قطع دسترسی‌های آی‌پی و قطع دسترسی‌های بی‌پایان در این فهرست نشان داده نمی‌شوند.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] || [[کاربر:%s]] || {{formatnum:%s|NOSEP}} || {{formatnum:%s|NOSEP}} || %s',
            "sign": True
        },
        {
            "sqlnum":41,
            "sql":
            "select cl_to, count(cl_from) cnt from categorylinks join logging on log_title = cl_to left join page on cl_to = page_title and page_namespace = 14 where log_action = 'delete' and page_id is null group by cl_to order by CNT desc",
            "out": 'وپ:گزارش دیتابیس/رده‌های حذف شده مورد نیاز',
            "cols": [u'ردیف', u'رده', u'تعداد کاربردها'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d|NOSEP}} || [[:رده:%s]] || {{formatnum:%s}}',
            "sign": True
        },
        {
            "sqlnum":42,
            "sql":
            "select ipb_address, ipb_by_text, str_to_date(left(ipb_timestamp, 8), '%Y%m%d'), str_to_date(left(ipb_expiry, 8), '%Y%m%d'), ipb_reason from ipblocks where str_to_date(left(ipb_expiry, 8), '%Y%m%d') > date_add(str_to_date(left(ipb_timestamp, 8), '%Y%m%d'),interval 2 year) and ipb_expiry <> 'infinity' and ipb_user = 0",
            "out": 'وپ:گزارش دیتابیس/آی‌پی‌های بسته‌شده به مدت طولانی',
            "cols": [u'ردیف', u'آی‌پی', u'مجری', u'تاریخ بستن', u'تاریخ انقضا', u'دلیل'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست آی‌پی‌هایی را نشان می‌دهد که بیش از دو سال بسته شده‌اند (اما نه بی‌پایان).\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[کاربر:%s]] || [[کاربر:%s]] || {{formatnum:%s|NOSEP}} || {{formatnum:%s|NOSEP}} || <nowiki>%s</nowiki>',
            "sign": True
        },
        {
            "sqlnum":43,
            "sql":
            "SELECT  page_title, replace(str_to_date(pr_expiry, '%Y%m%d%H%i%s'), 'T', ' ساعت ')   FROM page_restrictions JOIN page ON page_id = pr_page WHERE page_namespace = 0 AND pr_type = 'edit' AND pr_level = 'sysop' AND pr_expiry != 'infinity';",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های دارای محافظت کامل با زمان محدود',
            "cols": [u'ردیف', u'مقاله',  u'تاریخ انقضا'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست مقاله‌هایی را نشان می‌دهد که محافظت کامل با زمان محدود (اما نه بی‌پایان) شده‌اند.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":44,
            "sql":
            "select p1.page_title, count(pl_from) as cnt from page p1 join categorylinks on p1.page_id = cl_from and cl_to = 'همه_صفحه‌های_ابهام‌زدایی' join pagelinks on pl_title = page_title and pl_namespace = 0 join page p2 on pl_from = p2.page_id and p2.page_namespace = 0 where p1.page_namespace = 0 group by pl_title order by 2 desc limit 1000;",
            "out": 'وپ:گزارش دیتابیس/صفحه‌های ابهام‌زدایی پرکاربرد',
            "cols": [u'ردیف', u'مقاله',  u'تعداد پیوندها'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست صفحه‌های ابهام‌زدایی را نشان می‌دهد که بیشترین پیوند به آن‌ها داده شده‌است.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":45,
            "sql":
            "select page.page_title,GROUP_CONCAT(CONCAT ('[[الگو:',tem.page_title,']]') SEPARATOR '، '), count(tem.page_title) as cnt from page join categorylinks on page_id = cl_from and cl_to = 'همه_صفحه‌های_ابهام‌زدایی' join pagelinks on pl_title = page_title JOIN (select * from page where page_namespace = 10 and page_is_redirect = 0) as tem WHERE tem.page_id=pl_from and pl_namespace = 0 AND pl_from_namespace=10  and NOT tem.page_title LIKE '%_/_%' and page.page_namespace = 0 group by page.page_title order by 3 desc limit 1000;",
            "out": 'وپ:گزارش دیتابیس/صفحه‌های ابهام‌زدایی استفاده شده در الگو',
            "cols": [u'ردیف', u'مقاله', u'الگوهای استفاده شده', u'تعداد پیوندها'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست صفحه‌های ابهام‌زدایی که در الگو به کار رفته‌اند را نشان می‌دهد.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[%s]] ||%s|| {{formatnum:%s|NOSEP}}',
            "sign": True
        },
        {
            "sqlnum":46,
            "sql":
            "SELECT fap.page_title, enp.page_title , limagelist.il_to FROM fawiki_p.page as fap INNER JOIN fawiki_p.langlinks as fal ON fap.page_id = fal.ll_from inner join enwiki_p.page as enp on fal.ll_title=enp.page_title join (SELECT * FROM enwiki_p.imagelinks as eni) as limagelist WHERE fap.page_namespace = 0 and fal.ll_lang = 'en' AND fap.page_is_redirect = 0 and fap.page_id not in (SELECT fai.il_from FROM fawiki_p.imagelinks as fai) and enp.page_id=limagelist.il_from and not limagelist.il_to like 'Flag_of_%' and not limagelist.il_to like 'Ambox_%' and not limagelist.il_to like 'Wiktionary%' and not limagelist.il_to like 'Wikibooks%' and not limagelist.il_to like 'Wikivoyage%' and not limagelist.il_to like 'Incubator%' and not limagelist.il_to like 'Searchtool%' and not limagelist.il_to like 'Speech_balloon%' and not limagelist.il_to like 'Crystal_Clear%' and not limagelist.il_to like 'Speakerlink%' and not limagelist.il_to like 'Loudspeaker%' and not limagelist.il_to like 'Padlock%' and not limagelist.il_to like 'Nuvola_apps_%' and not limagelist.il_to like 'Wikiquote%' and not limagelist.il_to like 'Wikisource%' and not limagelist.il_to like 'Wikinews%' and not limagelist.il_to like 'Wikiversity%' and not limagelist.il_to like 'Question_book%' and not limagelist.il_to like 'Folder_Hexagonal%' and not limagelist.il_to like 'Portal-puzzle%' and not limagelist.il_to like 'Edit-clear%' and not limagelist.il_to like 'Text_document_with_red_question_mark%' and not limagelist.il_to like '%_stub%' and not limagelist.il_to like 'Rod_of_Asclepius%' and not limagelist.il_to like 'Merge-arrows%' and not limagelist.il_to like '%_icon%' and not limagelist.il_to like '%Balloon%' and not limagelist.il_to like 'Mergefrom%' and not limagelist.il_to like 'WikiProject%' and not limagelist.il_to like 'Yes_check%' and not limagelist.il_to like 'X_mark%' and not limagelist.il_to like 'Blank%' and not limagelist.il_to like '%_Icon%' and not limagelist.il_to like 'Symbol_book_class%' and not limagelist.il_to like 'Free_and_open-source_software_logo%' and not limagelist.il_to like 'Red_pog%' and not limagelist.il_to like 'Symbol_list_class%' and not limagelist.il_to like 'Allah-green%' and not limagelist.il_to like 'Symbol_support_vote%' and not limagelist.il_to like 'A_coloured_voting_box%' and not limagelist.il_to like 'Wiki_letter_w_cropped%' and not limagelist.il_to like 'Commons%' limit 1000;",
            "out": 'وپ:گزارش دیتابیس/مقاله‌های نیازمند پرونده همسنگ',
            "cols": [u'ردیف', u'مقالهٔ ویکی‌پدیای فارسی', u'مقالهٔ ویکی‌پدیای انگلیسی', u'پروندهٔ به کار رفته در ویکی‌پدیای انگلیسی'],
            "summary": u'به روز کردن آمار',
            "pref":
            u'[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nاین فهرست صفحه‌هایی در ویکی‌پدیای فارسی را نشان می‌دهد که صفحهٔ نظیرشان در ویکی‌پدیای انگلیسی یک تصویر شاخص دارد.\n\nآخرین به روز رسانی: ~~~~~',
            "frmt":
            u'| {{formatnum:%d}} || [[%s]] || [[:en:%s]] || [[File:%s|60px]]',
            "sign": True
        },
    ]

    for t in tasks:
        if sqlnum:
            if sqlnum!=t["sqlnum"]:
                continue
        bot = stats.StatsBot(
            t["sql"],
            t["out"],
            t["cols"],
            t["summary"],
            t["pref"],
            t["frmt"],
            t["sign"])
        try:
            bot.run()
        except:
            print sys.exc_info()[0]

if __name__ == "__main__":
    #For testing specifice sql you can use it's sqlnum argument
    # python pwb.py weekly.py <sqlnum>
    # python pwb.py weekly.py 2
    try:
        sqlnum=int(sys.argv[1])
    except:
        sqlnum=0
    main(sqlnum)
