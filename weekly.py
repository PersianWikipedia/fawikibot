#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
weekly.py - a wrapper for stats.py to be called every week.
usage:
    python pwb.py weekly <sqlnum>
    or
    python pwb.py weekly
parameters:
    <sqlnum>: (optinal) integer Used to run specifice queries
"""
#
# (C) Pywikibot team, 2006-2014
# (C) w:fa:User:Huji, 2015-2016
#
#
from __future__ import unicode_literals

#

import pywikibot
import sys
import stats


def main(sqlnum):
    tasks = [
        {
            "sqlnum": 1,
            "sql": """
SELECT DISTINCT
  log_id,
  user_name,
  CONCAT(':{{ns:', ar_namespace, '}}:', ar_title) AS link,
  log_comment,
  STR_TO_DATE(LEFT(log_timestamp, 8), '%Y%m%d'),
  'حذف تصویر' AS issue
FROM logging
JOIN user_groups ug
  ON log_user = ug.ug_user
  AND ug.ug_group = 'eliminator'
JOIN user
  ON log_user = user_id
JOIN archive
  ON log_page = ar_page_id
LEFT JOIN user_groups ug2
  ON log_user = ug2.ug_user
  AND ug2.ug_group = 'Image-reviewer'
WHERE
  log_type = 'delete'
  AND ar_namespace = 6
  AND log_timestamp >=
    DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 30 DAY), '%Y%m%d000000')
  AND ug2.ug_user IS NULL
UNION
SELECT DISTINCT
  log_id,
  u.user_name,
  CONCAT('کاربر:', log_title) AS link,
  log_comment,
  STR_TO_DATE(LEFT(log_timestamp, 8), '%Y%m%d'),
  'بستن غیرمجاز' AS issue
FROM logging
JOIN user_groups ug
  ON log_user = ug.ug_user
JOIN user u
  ON log_user = u.user_id
JOIN user u2
  ON log_title = u2.user_name
JOIN user_groups ug2
  ON u2.user_id = ug2.ug_user
WHERE
  ug.ug_group = 'eliminator'
  AND log_type = 'block'
  AND ug2.ug_group IN (
    'sysop',
    'bureaucrat',
    'patroller',
    'autopatrol',
    'rollbacker'
  )
  AND log_timestamp >=
    DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 30 DAY), '%Y%m%d000000')
UNION
SELECT DISTINCT
  log_id,
  user_name,
  log_title AS link,
  log_comment,
  STR_TO_DATE(LEFT(log_timestamp, 8), '%Y%m%d'),
  'محافظت کامل' AS issue
FROM logging
JOIN user_groups
  ON log_user = ug_user
JOIN user
  ON log_user = user_id
WHERE
  ug_group = 'eliminator'
  AND log_type = 'protect'
  AND log_action = 'protect'
  AND log_params LIKE '%level%sysop%'
  AND log_timestamp >=
    DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 30 DAY), '%Y%m%d000000')
UNION
SELECT
  log_id,
  user_name,
  CONCAT('{{ns:' , log_namespace, '}}:', log_title) AS link,
  log_comment,
  STR_TO_DATE(LEFT(log_timestamp, 8), '%Y%m%d'),
  'احیای نسخهٔ حذف‌شده' AS issue
FROM logging
JOIN user_groups
  ON log_user = ug_user
JOIN user
  ON user_id = log_user
WHERE
  ug_group = 'eliminator'
  AND log_params LIKE '%nfield";i:0%'
  AND log_type='delete'
  AND log_action='revision'
  AND log_timestamp >=
    DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 30 DAY), '%Y%m%d000000')
ORDER BY log_id DESC
""",
            "out": "وپ:گزارش دیتابیس/گزارش عملکرد اشتباه ویکی‌بان‌ها",
            "cols": ["شناسه", "کاربر", "هدف", "توضیح", "تاریخ", "مشکل"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این صفحه جدولی از فعالیت‌های ویکی‌بان‌ها در یک ماه گذشته را نشان می‌دهد که ممکن
است ناقض [[وپ:ویکی‌بان]] باشند. مواردی که چک می‌کند عبارتند از:
* حذف تصاویر (چک کنید که کاربر دسترسی جداگانه برای حذف تصاویر داشته باشد)
* بستن کاربران دارای دسترسی گشت خودکار یا گشت یا واگردان یا مدیر
* محافظت در سطح محافظت کامل و/یا برای بیشتر از یک هفته
آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| %s || [[کاربر:%s|]] || [[%s]] || " +
                    "<nowiki>%s</nowiki> || {{formatnum:%s|NOSEP}} || %s",
            "sign": True
        },
        {
            "sqlnum": 2,
            "sql": """
SELECT page_title
FROM categorylinks
JOIN page
  ON cl_from = page_id
LEFT JOIN imagelinks
  ON il_to = page_title
WHERE
  cl_to = 'پرونده‌های_مالکیت_عمومی'
  AND page_namespace = 6
  AND il_from IS NULL
""",
            "out": "وپ:گزارش دیتابیس/پرونده‌های آزاد استفاده نشده",
            "cols": ["ردیف", "پرونده"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:File:%s]]",
            "sign": True
        },
        {
            "sqlnum": 3,
            "sql": """
SELECT page_title
FROM categorylinks
JOIN page
  ON cl_from = page_id
LEFT JOIN imagelinks
  ON il_to = page_title
WHERE cl_to = 'محتویات_غیر_آزاد'
  AND page_namespace = 6
  AND il_from IS NULL
""",
            "out": "ویکی‌پدیا:گزارش_دیتابیس/پرونده‌های غیر آزاد استفاده نشده",
            "cols": ["ردیف", "پرونده"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:پرونده:%s|]]",
            "sign": True
        },
        {
            "sqlnum": 4,
            "sql": """
SELECT
  page_title,
  STR_TO_DATE(LEFT(page_touched,8), '%Y%m%d')
FROM page
LEFT JOIN categorylinks
  ON page_id = cl_from
WHERE
  page_namespace = 6
  AND page_is_redirect = 0
  AND cl_to IS NULL
""",
            "out": "وپ:گزارش دیتابیس/پرونده‌های رده‌بندی نشده",
            "cols": ["ردیف", "پرونده", "تاریخ بارگذاری"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:File:%s]] " +
                    "|| {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 5,
            "sql": """
SELECT
  ipb_address,
  ipb_by_text,
  STR_TO_DATE(LEFT(ipb_timestamp,8), '%Y%m%d'),
  ipb_reason
FROM ipblocks
WHERE
  ipb_expiry = 'infinity'
  AND ipb_user = 0
""",
            "out": "وپ:گزارش دیتابیس/آی‌پی‌های بی‌پایان بسته شده",
            "cols": ["ردیف", "آی‌پی", "مدیر", "تاریخ", "دلیل"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:بحث کاربر:%s|]] " +
                    "|| [[کاربر:%s|]] " +
                    "|| {{عبارت چپ‌چین|{{formatnum:%s|NOSEP}}}} || %s",
            "sign": True
        },
        {
            "sqlnum": 6,
            "sql": """
SELECT
 CASE
   WHEN up_value = 'male' THEN 'مرد'
   ELSE 'زن'
 END AS Gender,
 COUNT(up_value)
FROM user_properties
WHERE up_property = 'gender'
GROUP BY up_value
""",
            "out": "وپ:گزارش دیتابیس/ترجیحات کاربران/جنسیت",
            "cols": ["جنسیت", "تعداد"],
            "summary": "به روز کردن آمار",
            "pref": u'',
            "frmt": "| %s || {{formatnum:%s}}",
            "sign": False
        },
        {
            "sqlnum": 7,
            "sql": """
SELECT
  (mid(up_value, 10, locate('|', mid(up_value,10))-1) / 60) AS offset,
  COUNT(up_value)
FROM user_properties
WHERE up_property = 'timecorrection'
GROUP BY offset
ORDER BY offset
""",
            "out": "وپ:گزارش دیتابیس/ترجیحات کاربران",
            "cols": ["اختلاف ساعت", "تعداد"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~\n\n==جنسیت==\n\n{{/جنسیت}}" +
                    "\n\n==منطقه زمانی==\n\n",
            "frmt": "| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 8,
            "sql": """
SELECT page_title
FROM page
LEFT JOIN categorylinks
  ON page_id = cl_from
WHERE
  page_namespace = 0
  AND page_is_redirect = 0
  AND cl_from IS NULL
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های رده‌بندی نشده",
            "cols": ["ردیف", "مقاله"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[%s]]",
            "sign": True
        },
        {
            "sqlnum": 9,
            "sql": """
SELECT
  page_title,
  STR_TO_DATE(LEFT(rev_timestamp, 8), '%Y%m%d')
FROM page JOIN revision
  ON page_latest = rev_id
LEFT JOIN pagelinks
  ON page_id = pl_from
WHERE
  page_namespace = 0
  AND page_is_redirect = 0
  AND pl_from IS NULL
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های بدون پیوند ویکی",
            "cols": ["ردیف", "مقاله", "آخرین ویرایش"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 10,
            "sql": """
SELECT
  page_title,
  pl_title
FROM page JOIN pagelinks
  ON page_id = pl_from
LEFT JOIN categorylinks
  ON page_id = cl_from
  AND cl_to = 'مقاله‌های_نامزد_حذف_سریع'
WHERE
  page_namespace = 0
  AND pl_namespace IN (2, 3)
  AND cl_to IS NULL
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های دارای پیوند به صفحه کاربری",
            "cols": ["ردیف", "مقاله", "پیوند به صفحه (بحث) کاربر"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست شامل صفحه‌هایی که برچسب حذف سریع دارند اما در ردهٔ حذف سریع قرار
نگرفته‌اند نیز می‌شود

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || [[کاربر:%s]]",
            "sign": True
        },
        {
            "sqlnum": 11,
            "sql": """
SELECT
  page_namespace,
  page_title,
  page_len,
  STR_TO_DATE(LEFT(rev_timestamp, 8), '%Y%m%d')
FROM page
JOIN revision
  ON page_latest = rev_id
WHERE page_len > 300 * 1024
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های پرحجم",
            "cols": ["ردیف", "مقاله", "پیوند به صفحه (بحث) کاربر"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[{{ns:%s}}:%s]] " +
                    "|| {{formatnum:%s}} || {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 12,
            "sql": """
SELECT page_title
FROM page
JOIN (
  SELECT
    rev_page,
    COUNT(DISTINCT rev_user) AS cnt
  FROM revision
  GROUP BY rev_page
  HAVING cnt = 1
) singleauth
  ON page_id = rev_page
LEFT JOIN pagelinks
  ON pl_title = page_title
  AND pl_namespace = 4
  AND pl_from <> 1171408
LEFT JOIN templatelinks
  ON tl_title = page_title
  AND tl_namespace = 4
WHERE
  page_namespace = 4
  AND page_is_redirect = 0
  AND pl_title IS NULL
  AND tl_title IS NULL
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های پروژه یتیم تک‌نویسنده",
            "cols": ["ردیف", "صفحه"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[{{ns:4}}:%s]]",
            "sign": True
        },
        {
            "sqlnum": 13,
            "sql": """
SELECT
  i1.img_name,
  i2.img_name
FROM image i1
JOIN image i2
  ON i1.img_sha1 = i2.img_sha1 AND i1.img_name > i2.img_name
""",
            "out": "وپ:گزارش دیتابیس/پرونده‌های تکراری",
            "cols": ["ردیف", "پرونده اول", "پرونده دوم"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[:پرونده:%s]] || [[:پرونده:%s]]",
            "sign": True
        },
        {
            "sqlnum": 14,
            "sql": """
SELECT
  page_title,
  COUNT(il_to) cnt,
  SUM(
    CASE
      WHEN il_from_namespace = 0 THEN 0
      ELSE 1
    END
  ) AS nonarticle
FROM page
JOIN categorylinks
  ON page_id = cl_from
  AND cl_to = 'محتویات_غیر_آزاد'
JOIN imagelinks
  ON page_title = il_to
GROUP BY page_title
HAVING cnt > 10
ORDER BY cnt DESC
""",
            "out": "وپ:گزارش دیتابیس/محتویات غیرآزاد بیش از حد استفاده شده",
            "cols": ["ردیف", "پرونده", "کل کاربردها", "کاربرد غیر منصفانه"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست پرونده‌های غیر آزادی را نشان می‌دهد که بیش از ده بار استفاده شده‌اند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[:پرونده:%s]] " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 15,
            "sql": """
SELECT
  page_title,
  page_len
FROM page
JOIN categorylinks
  ON page_id = cl_from
  AND cl_to = 'همه_مقاله‌های_خرد'
WHERE page_len > 10 * 1024
ORDER BY page_len DESC
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های خرد بلند",
            "cols": ["ردیف", "مقاله", "حجم"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست مقاله‌هایی را نشان می‌دهد که برچسب خرد دارند و دست کم یک کیلوبایت
حجم دارند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 16,
            "sql": """
SELECT
  page_namespace,
  page_title
FROM externallinks
JOIN page
  ON el_from = page_id
WHERE
  LEFT(el_to, 7) = 'mailto:'
  AND el_to NOT LIKE '%wikimedia.org%'
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های دارای پیوند به رایانامه",
            "cols": ["ردیف", "صفحه"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست صفحه‌هایی را نشان می‌دهد که پیوند به نشانی ایمیل دارند (اما مواردی
که نشانی ایمیل مربوط به خود ویکی‌مدیا است را نشان نمی‌دهد).

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[{{ns:%s}}:%s]]",
            "sign": True
        },
        {
            "sqlnum": 17,
            "sql": """
SELECT
  page_title,
  STR_TO_DATE(LEFT(rev_timestamp, 8), '%Y%m%d')
FROM page
JOIN revision
  ON page_latest = rev_id
LEFT JOIN categorylinks
  ON page_id = cl_from
  AND cl_to = 'صفحه‌های_ابهام‌زدایی'
WHERE
  page_namespace = 0
  AND page_is_redirect = 0
  AND rev_timestamp <
    CONCAT(DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 4 YEAR), '%Y%m%d'), '000000')
  AND cl_to IS NULL
ORDER BY rev_timestamp
LIMIT 5000
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های فراموش‌شده",
            "cols": ["ردیف", "صفحه", "آخرین ویرایش"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست مقاله‌هایی را نشان می‌دهد که دست کم چهار سال  از آخرین ویرایش‌شان
می‌گذرد (به جز صفحه‌های ابهام‌زدایی).

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 18,
            "sql": """
SELECT
  page_title,
  page_len
FROM page
WHERE
  page_namespace = 0
  AND page_len > 20 * 1024
ORDER BY page_len DESC
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های پرحجم",
            "cols": ["ردیف", "صفحه", "حجم"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست مقاله‌هایی را نشان می‌دهد که دست کم بیست کیلوبایت حجم دارند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 19,
            "sql": """
SELECT
  page_title,
  page_len
FROM page
LEFT JOIN categorylinks
  ON page_id = cl_from
  AND cl_to IN (
  'همه_صفحه‌های_ابهام‌زدایی',
  'نام‌های_کوچک',
  'نام‌های_خانوادگی',
  'همه_مقاله‌های_مجموعه‌نمایه'
  )
WHERE
  page_namespace = 0
  AND page_is_redirect = 0
  AND cl_to IS NULL
  AND page_len < 500
ORDER BY page_len
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های کم‌حجم",
            "cols": ["ردیف", "مقاله", "حجم"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست مقاله‌هایی را نشان می‌دهد که زیر پانصد بایت حجم دارند (به جز صفحه های
ابهام‌زدایی).

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 20,
            "sql": """
SELECT
  page.page_namespace,
  page.page_namespace,
  noredir,
  redir,
  COUNT(page_id) tot
FROM page
JOIN (
  SELECT
    page_namespace,
    COUNT(page_id) redir
  FROM page
  WHERE page_is_redirect = 1
  GROUP BY page_namespace
) redir
  ON page.page_namespace = redir.page_namespace
JOIN (
  SELECT
    page_namespace,
    COUNT(page_id) noredir
  FROM page
  WHERE page_is_redirect = 0
  GROUP BY page_namespace
) noredir
  ON page.page_namespace = noredir.page_namespace
GROUP BY page.page_namespace
""",
            "out": "وپ:گزارش دیتابیس/تعداد صفحه‌های هر فضای نام",
            "cols": [
                u"ردیف",
                u"شناسه فضای نام",
                u"عنوان فضای نام",
                u"بدون تغییرمسیر",
                u"تغییرمسیر",
                u"جمع کل"
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || %s || {{ns:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 21,
            "sql": """
SELECT
  page_namespace,
  page_title,
  page_len
FROM page
LEFT JOIN categorylinks
  ON page_id = cl_from
  AND cl_to = 'همه_صفحه‌های_ابهام‌زدایی'
JOIN (
  SELECT
    rev_page,
    COUNT(DISTINCT rev_user) cnt
  FROM revision
  GROUP BY rev_page
  HAVING cnt = 1
) authors
  ON page_id = rev_page
WHERE
  page_namespace NOT IN (6, 14)
  AND page_is_redirect = 0
  AND page_namespace IN (0, 4, 12)
  AND cl_to IS NULL
  AND page_len < 10
ORDER BY page_len
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های کوتاه تک‌نویسنده",
            "cols": ["ردیف", "صفحه", "حجم"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست صفحه‌هایی در فضای نام مقاله، ویکی‌پدیا یا راهنما را نشان می‌دهد که
زیر ده بایت حجم و تنها یک ویرایشگر دارند (به جز صفحه های ابهام‌زدایی).

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[{{ns:%s}}:%s]] " +
                    "|| {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 22,
            "sql": """
SELECT
  page_title,
  il_to
FROM page
JOIN imagelinks
  ON il_from = page_id
WHERE
  page_namespace = 0
  AND il_to NOT IN (
    SELECT page_title
    FROM page
    WHERE
    page_namespace = 6
  )
  AND il_to NOT IN (
    SELECT page_title
    FROM commonswiki_p.page
    WHERE page_namespace = 6
  )
LIMIT 10000
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های دارای پیوند به پرونده ناموجود",
            "cols": ["ردیف", "مقاله", "پرونده"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست حداکثر ده‌هزارتا از مقاله‌هایی را نشان می‌دهد که زیر ده بایت حجم و
تنها یک ویرایشگر دارند (به جز صفحه های ابهام‌زدایی).

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || [[:پرونده:%s]]",
            "sign": True
        },
        {
            "sqlnum": 23,
            "sql": """
SELECT
  user_name,
  COUNT(log_id) cnt
FROM user
JOIN logging
  ON log_user = user_id
LEFT JOIN user_groups
  ON log_user = ug_user
  AND ug_group = 'bot'
WHERE
  log_type ='patrol'
  AND log_action='patrol'
  AND (
    log_params LIKE '%auto";i:0;}'
    OR log_params LIKE '%0'
  )
  AND ug_group IS NULL
GROUP BY
  log_user,
  log_action
ORDER BY cnt DESC
""",
            "out": "وپ:گزارش دیتابیس/کاربران بر پایه تعداد گشت‌زنی‌ها",
            "cols": ["ردیف", "کاربر", "گشت‌زنی"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست تنها گشت‌زدن‌های غیر خودکار را شامل می‌شود و کاربرانی که در حال
حاضر برچسب ربات دارند را شامل نمی‌شود.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} ",
            "sign": True
        },
        {
            "sqlnum": 24,
            "sql": """
SELECT
  user_name,
  COUNT(wll_id) gotlove,
  IFNULL(gavelove, 0)
FROM user
JOIN wikilove_log
  ON user_id = wll_receiver
LEFT JOIN (
  SELECT
    wll_sender,
    COUNT(wll_id) gavelove
  FROM wikilove_log
  GROUP BY wll_sender
) gavelove
  ON user_id = gavelove.wll_sender
GROUP BY wll_receiver
ORDER BY gotlove DESC
""",
            "out": "وپ:گزارش دیتابیس/کاربران بر پایه قدردانی‌ها",
            "cols": ["ردیف", "کاربر", "قدردانی از او", "قدردانی او از دیگران"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
کاربرانی که در حال حاضر برچسب ربات دارند را شامل نمی‌شود.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 25,
            "sql": """
SELECT
  log_title,
  COUNT(log_id),
  IFNULL(thankback, 0),
  COUNT(log_id) + IFNULL(thankback, 0) AS cnt
FROM logging
LEFT JOIN (
  SELECT
    user_name,
    COUNT(log_id) thankback
  FROM logging JOIN user
    ON user_id = log_user
  WHERE log_type = 'thanks'
  GROUP BY user_name
) back
  ON back.user_name = replace(log_title, '_', ' ')
WHERE log_type = 'thanks'
GROUP BY log_title
ORDER BY cnt DESC
""",
            "out": "وپ:گزارش دیتابیس/کاربران بر پایه تعداد تشکر",
            "cols":
            ["ردیف",
             "کاربر",
             "تشکرها از او",
             "تشکرهای او از دیگران",
             "جمع کل"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 26,
            "sql": """
SELECT
  user_name,
  IFNULL(del.cnt, 0),
  IFNULL(res.cnt, 0),
  IFNULL(revdel.cnt, 0),
  IFNULL(logdel.cnt, 0),
  IFNULL(prot.cnt, 0),
  IFNULL(unprot.cnt, 0),
  IFNULL(editprot.cnt, 0),
  IFNULL(block.cnt, 0),
  IFNULL(unblock.cnt, 0),
  IFNULL(editblock.cnt, 0),
  IFNULL(renames.cnt, 0),
  IFNULL(rights.cnt, 0),
  (
    IFNULL(del.cnt, 0) +
    IFNULL(res.cnt, 0) +
    IFNULL(revdel.cnt, 0) +
    IFNULL(logdel.cnt, 0) +
    IFNULL(prot.cnt, 0) +
    IFNULL(unprot.cnt, 0) +
    IFNULL(editprot.cnt, 0) +
    IFNULL(block.cnt, 0) +
    IFNULL(unblock.cnt, 0) +
    IFNULL(editblock.cnt, 0) +
    IFNULL(renames.cnt, 0) +
    IFNULL(rights.cnt, 0)
  ) tot
FROM user JOIN user_groups
  ON user_id = ug_user
  AND ug_group = 'sysop'
LEFT JOIN (
  SELECT
   log_user,
   COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'delete'
    AND log_action='delete'
  GROUP BY log_user
) del
  ON user_id = del.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'delete'
    AND log_action='restore'
  GROUP BY log_user
) res
  ON user_id = res.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'delete'
    AND log_action='revision'
  GROUP BY log_user
) revdel
  ON user_id = revdel.log_user
LEFT JOIN (
  SELECT
    log_user,\
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'delete'
    AND log_action = 'event'
  GROUP BY log_user
) logdel
  ON user_id = logdel.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'protect'
    AND log_action = 'protect'
  GROUP BY log_user
) prot
  ON user_id = prot.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'protect'
    AND log_action = 'unprotect'
  GROUP BY log_user
) unprot
  ON user_id = unprot.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'protect'
    AND log_action = 'modify'
  GROUP BY log_user
) editprot
  ON user_id = editprot.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'block'
    AND log_action = 'block'
  GROUP BY log_user
) block
  ON user_id = block.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'block'
    AND log_action = 'unblock'
  GROUP BY log_user
) unblock
  ON user_id = unblock.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE
    log_type = 'block'
    AND log_action = 'reblock'
  GROUP BY log_user
) editblock
  ON user_id = editblock.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE log_type = 'renameuser'
  GROUP BY log_user
) renames
  ON user_id = renames.log_user
LEFT JOIN (
  SELECT
    log_user,
    COUNT(log_id) cnt
  FROM logging
  WHERE log_type = 'rights'
  AND log_action = 'rights'
  GROUP BY log_user
) rights
  ON user_id = rights.log_user
ORDER BY tot DESC
""",
            "out": "وپ:گزارش دیتابیس/فعالیت‌ مدیران کنونی",
            "cols": [
                "ردیف",
                "کاربر",
                "حذف",
                "احیا",
                "حذف نسخه",
                "حذف سیاهه",
                "محافظت",
                "رفع محافظت",
                "تغییر محافظت",
                "بستن",
                "باز کردن",
                "تغییر بندایش",
                "تغییر نام",
                "تغییر اختیارات",
                "جمع کل"
             ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 27,
            "sql": """
SELECT *
FROM (
  SELECT DISTINCT
    user_name,
    IFNULL(del.cnt, 0),
    IFNULL(res.cnt, 0),
    IFNULL(revdel.cnt, 0),
    IFNULL(logdel.cnt, 0),
    IFNULL(prot.cnt, 0),
    IFNULL(unprot.cnt, 0),
    IFNULL(editprot.cnt, 0),
    IFNULL(block.cnt, 0),
    IFNULL(unblock.cnt, 0),
    IFNULL(editblock.cnt, 0),
    IFNULL(renames.cnt, 0),
    IFNULL(rights.cnt, 0),
    (
      IFNULL(del.cnt, 0) +
      IFNULL(res.cnt, 0) +
      IFNULL(revdel.cnt, 0) +
      IFNULL(logdel.cnt, 0) +
      IFNULL(prot.cnt, 0) +
      IFNULL(unprot.cnt, 0) +
      IFNULL(editprot.cnt, 0) +
      IFNULL(block.cnt, 0) +
      IFNULL(unblock.cnt, 0) +
      IFNULL(editblock.cnt, 0) +
      IFNULL(renames.cnt, 0) +
      IFNULL(rights.cnt, 0)
    ) tot
  FROM user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'delete'
      AND log_action='delete'
    GROUP BY log_user
  ) del
    ON user_id = del.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'delete'
      AND log_action='restore'
    GROUP BY log_user
  ) res
    ON user_id = res.log_user
  LEFT JOIN (
    SELECT
     log_user,
     COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'delete'
      AND log_action='revision'
    GROUP BY log_user
  ) revdel
    ON user_id = revdel.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'delete'
      AND log_action = 'event'
    GROUP BY log_user
  ) logdel
    ON user_id = logdel.log_user
  LEFT JOIN (
    SELECT
     log_user,
     COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'protect'
      AND log_action = 'protect'
    GROUP BY log_user
  ) prot
    ON user_id = prot.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'protect'
      AND log_action = 'unprotect'
    GROUP BY log_user
  ) unprot
    ON user_id = unprot.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'protect'
      AND log_action = 'modify'
    GROUP BY log_user
  ) editprot
    ON user_id = editprot.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'block'
      AND log_action = 'block'
    GROUP BY log_user
  ) block
    ON user_id = block.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'block'
      AND log_action = 'unblock'
    GROUP BY log_user
  ) unblock
    ON user_id = unblock.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'block'
      AND log_action = 'reblock'
    GROUP BY log_user
  ) editblock
    ON user_id = editblock.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE log_type = 'renameuser'
    GROUP BY log_user
  ) renames
    ON user_id = renames.log_user
  LEFT JOIN (
    SELECT
      log_user,
      COUNT(log_id) cnt
    FROM logging
    WHERE
      log_type = 'rights'
      AND log_action = 'rights'
    GROUP BY log_user
  ) rights
    ON user_id = rights.log_user
) withzeros
WHERE tot > 0
ORDER BY tot DESC
""",
            "out": "وپ:گزارش دیتابیس/فعالیت‌های مدیران از ابتدا",
            "cols": [
                "ردیف",
                "کاربر",
                "حذف",
                "احیا",
                "حذف نسخه",
                "حذف سیاهه",
                "محافظت",
                "رفع محافظت",
                "تغییر محافظت",
                "بستن",
                "باز کردن",
                "تغییر بندایش",
                "تغییر نام",
                "تغییر اختیارات",
                "جمع کل"
             ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 28,
            "sql": """
SELECT
  page_title,
  cnt
FROM enwiki_p.page
JOIN (
  SELECT
    ll_from,
    COUNT(ll_lang) cnt
  FROM enwiki_p.langlinks
  GROUP BY ll_from
  HAVING
    cnt >= 40
    AND max(ll_lang='fa') = 0
) highll
  ON page_id = ll_from
WHERE page_namespace = 0
ORDER BY cnt DESC
""",
            "out": "وپ:گزارش دیتابیس/" +
                   "مقاله‌های مهم ایجادنشده بر پایه دیگر میان‌ویکی‌ها",
            "cols": ["ردیف", "مقاله", "میان‌ویکی‌ها"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\n{{/بالا}}\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[:en:%s]] || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 29,
            "sql": """
SELECT
  page_title,
  page_len
FROM enwiki_p.page
JOIN (
  SELECT
    ll_from,
    COUNT(ll_lang) cnt
  FROM enwiki_p.langlinks
  GROUP BY ll_from
  HAVING
    max(ll_lang='fa') = 0
) highll
  ON page_id = ll_from
WHERE
  page_namespace = 0
  AND page_len > 150 * 1024
ORDER BY page_len DESC
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های مهم ایجادنشده بر پایه حجم",
            "cols": ["ردیف", "مقاله", "حجم"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست طولانی‌ترین مقاله‌های ویکی‌پدیای انگلیسی را نشان می‌دهد که در
ویکی‌پدیای فارسی معادل ندارند (یا دست کم پیوند میان‌ویکی داده نشده‌است).

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[:en:%s]] || {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 30,
            "sql": """
SELECT DISTINCT page_title
FROM page
JOIN iwlinks
  ON page_id = iwl_from
LEFT JOIN langlinks
  ON page_id = ll_from
WHERE
  page_namespace = 0
  AND ll_from IS NULL
  AND iwl_prefix NOT IN (
    'b', 'n', 'q', 's', 'm', 'wikt', 'commons', 'wikispecies'
  )
""",
            "out": "وپ:گزارش دیتابیس/" +
                   "مقاله‌های دارای پیوند به ویکی که میان‌ویکی ندارند",
            "cols": ["ردیف", "الگو"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[%s]]",
            "sign": True
        },
        {
            "sqlnum": 31,
            "sql": """
SELECT cl_to
FROM categorylinks
JOIN page
  ON cl_from = page_id
WHERE
 page_title = cl_to
 AND page_title <> 'صفحه‌های_نمایه‌نشده'
 AND page_namespace = 14
""",
            "out": "وپ:گزارش دیتابیس/رده‌های حلقوی",
            "cols": ["ردیف", "رده"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:رده:%s]]",
            "sign": True
        },
        {
            "sqlnum": 32,
            "sql": """
SELECT
  page_title,
  CASE
    WHEN page_is_redirect = 1 THEN '{{بله}}'
    ELSE '{{خیر}}'
  END AS is_redirect
FROM page_restrictions
JOIN page
  ON page_id = pr_page
  AND page_namespace = 0
  AND pr_type = 'edit'
  AND pr_level = 'sysop'
  AND pr_expiry = 'infinity'
""",
            "out":
            'ویکی‌پدیا:گزارش دیتابیس/مقاله‌های دارای محافظت کامل بی‌پایان',
            "cols": ["ردیف", "مقاله", "تغییرمسیر؟"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[%s]] || %s ",
            "sign": True
        },
        # Query 33 was moved to weekly-slow #14
        {
            "sqlnum": 34,
            "sql": """
SELECT
  ipb_address,
  MID(ipb_address, INSTR(ipb_address, '/') + 1) AS cnt,
  ipb_by_text,
  STR_TO_DATE(LEFT(ipb_timestamp,8), '%Y%m%d'),
  STR_TO_DATE(LEFT(ipb_expiry,8), '%Y%m%d'),
  ipb_reason
FROM ipblocks
WHERE ipb_address LIKE '%/%'
""",
            "out": "ویکی‌پدیا:گزارش_دیتابیس/محدوده_آی‌پی‌های_بسته‌شده",
            "cols":
            ["ردیف",
             "بازه",
             "تعداد آی‌پی",
             "مدیر",
             "تاریخ بستن",
             "انقضا",
             "دلیل"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || %s || " +
                    "{{formatnum:%s|NOSEP}} || [[کاربر:%s]] " +
                    "|| {{عبارت چپ‌چین|{{formatnum:%s|NOSEP}}}} " +
                    "|| {{عبارت چپ‌چین|{{formatnum:%s|NOSEP}}}} || %s",
            "sign": True
        },
        {
            "sqlnum": 35,
            "sql": """
SELECT
  page_title,
  il_to
FROM page
JOIN imagelinks
  ON page_id = il_from
WHERE (
  NOT EXISTS (
    SELECT 1
    FROM image
    WHERE img_name = il_to
    )
  )
  AND (
    NOT EXISTS (
      SELECT 1
      FROM commonswiki_p.page
      WHERE
        page_title = il_to
        AND page_namespace = 6
    )
  )
  AND (
    NOT EXISTS (
      SELECT 1
      FROM page
      WHERE
        page_title = il_to
        AND page_namespace = 6
    )
  )
  AND page_namespace = 10
""",
            "out": "ویکی‌پدیا:گزارش_دیتابیس/" +
                   "الگوهای دارای پیوند به پرونده‌های ناموجود",
            "cols": ["ردیف", "الگو", "پرونده"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[الگو:%s|]] " +
                    "|| [[:پرونده:%s]]",
            "sign": True
        },
        {
            "sqlnum": 36,
            "sql": """
SELECT
  tl_title,
  COUNT(*)
FROM templatelinks
WHERE tl_namespace = 10
GROUP BY tl_title
ORDER BY COUNT(*) DESC
LIMIT 1000
""",
            "out": "ویکی‌پدیا:گزارش_دیتابیس/الگوهای دارای بیشترین تراگنجایش",
            "cols": ["ردیف", "الگو", "تعداد تراگنجایش"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این صفحه فهرست ۱۰۰۰ الگوی دارای بیشترین تراگنجایش را نشان می‌دهد.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[الگو:%s|]] " +
                    "|| {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 37,
            "sql": """
SELECT
  tl_title,
  COUNT(*)
FROM page
JOIN templatelinks
  ON page_title = tl_title
  AND page_namespace = tl_namespace
LEFT JOIN page_restrictions
  ON pr_page = page_id
  AND pr_level IN ('sysop', 'autoconfirmed')
  AND pr_type = 'edit'
WHERE
  tl_namespace = 10
  AND pr_page IS NULL
GROUP BY tl_title
HAVING COUNT(*) > 500
ORDER BY COUNT(*) DESC
""",
            "out": "ویکی‌پدیا:گزارش_دیتابیس/الگوهای پرکاربرد بدون محافظت",
            "cols": ["ردیف", "الگو", "تعداد تراگنجایش"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این صفحه فهرست الگوی دارای دست کم ۵۰۰ تراگنجایش را نشان می‌دهد که محافظت
نشده‌اند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[الگو:%s|]] " +
                    "|| {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 38,
            "sql": """
SELECT
  page_title,
  (
    SELECT COUNT(*)
    FROM imagelinks
    WHERE il_to = page_title
  ) AS imagelinks,
  (
    SELECT COUNT(*)
    FROM pagelinks
    WHERE
      pl_namespace = 6
      AND pl_title = page_title
  ) AS links
  FROM page
  WHERE
    page_namespace = 6
    AND page_is_redirect = 1
HAVING imagelinks + links <= 1
""",
            "out": "ویکی‌پدیا:گزارش_دیتابیس/" +
                   "صفحه‌های بدون استفاده تغییرمسیر پرونده",
            "cols":
            ["ردیف",
             "صفحه پرونده",
             "تعداد تراگنجایش",
             "تعداد پیوند ورودی"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\n: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:پرونده:%s|]] " +
                    "|| {{formatnum:%s|NOSEP}} || {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 39,
            "sql": """
SELECT
  user_name,
  sum(img_size) AS tot
FROM image
JOIN user
  ON img_user = user_id
GROUP BY img_user
ORDER BY tot DESC
LIMIT 500
""",
            "out": "وپ:گزارش دیتابیس/" +
                   "کاربران برپایه مقدار حجم پرونده بارگذاری شده",
            "cols": ["ردیف", "کاربر", "حجم کل (بایت)"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست ۵۰۰ کاربر دارای بیشترین حجم بارگذاری در ویکی‌پدیای فارسی را نشان
می‌دهد.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] " +
                    "|| {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 40,
            "sql": """
SELECT
  u1.user_name blockee,
  u2.user_name blocker,
  REPLACE(STR_TO_DATE(ipb_timestamp, '%Y%m%d%H%i%s'), 'T', ' ساعت ') blocktime,
  REPLACE(STR_TO_DATE(ipb_expiry, '%Y%m%d%H%i%s'), 'T', ' ساعت ') blockend,
  ipb_reason
FROM ipblocks
JOIN user u1
  ON ipb_user = u1.user_id
JOIN user u2
  ON ipb_by = u2.user_id
WHERE
  ipb_user <> 0
  AND ipb_expiry NOT IN ('infinity', 'indefinite')
  AND ipb_expiry > CONCAT(DATE_FORMAT(NOW(), '%Y%m%d'), '000000')
""",
            "out": "وپ:گزارش دیتابیس/کاربران بسته شده",
            "cols":
            ["ردیف",
             "کاربر هدف",
             "مجری",
             "شروع قطع دسترسی",
             "پایان قطع دسترسی",
             "دلیل"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست کاربرانی را نشان می‌دهد که در زمان ثبت آمار دسترسی‌شان برای مدتی
مشخص قطع شده بوده‌است. قطع دسترسی‌های آی‌پی و قطع دسترسی‌های بی‌پایان در این
فهرست نشان داده نمی‌شوند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] || " +
                    "[[کاربر:%s]] || {{formatnum:%s|NOSEP}} " +
                    "|| {{formatnum:%s|NOSEP}} || %s",
            "sign": True
        },
        {
            "sqlnum": 41,
            "sql": """
SELECT
  cl_to,
  COUNT(cl_from) cnt
FROM categorylinks
JOIN logging
  ON log_title = cl_to
LEFT JOIN page
  ON cl_to = page_title
  AND page_namespace = 14
WHERE
  log_action = 'delete'
  AND page_id IS NULL
GROUP BY cl_to
ORDER BY CNT DESC
""",
            "out": "وپ:گزارش دیتابیس/رده‌های حذف شده مورد نیاز",
            "cols": ["ردیف", "رده", "تعداد کاربردها"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:رده:%s]] " +
                    "|| {{formatnum:%s}}",
            "sign": True
        },
        {
            "sqlnum": 42,
            "sql": """
SELECT
  ipb_address,
  ipb_by_text,
  STR_TO_DATE(LEFT(ipb_timestamp, 8), '%Y%m%d'),
  STR_TO_DATE(LEFT(ipb_expiry, 8), '%Y%m%d'),
  ipb_reason
FROM ipblocks
WHERE
  STR_TO_DATE(LEFT(ipb_expiry, 8), '%Y%m%d') >
    DATE_ADD(STR_TO_DATE(LEFT(ipb_timestamp, 8), '%Y%m%d'), INTERVAL 2 YEAR)
  AND ipb_expiry <> 'infinity'
  AND ipb_user = 0
""",
            "out": "وپ:گزارش دیتابیس/آی‌پی‌های بسته‌شده به مدت طولانی",
            "cols": [
                "ردیف",
                "آی‌پی",
                "مجری",
                "تاریخ بستن",
                "تاریخ انقضا",
                "دلیل"
            ],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست آی‌پی‌هایی را نشان می‌دهد که بیش از دو سال بسته شده‌اند
(اما نه بی‌پایان).

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] || [[کاربر:%s]] " +
                    "|| {{formatnum:%s|NOSEP}} || {{formatnum:%s|NOSEP}} " +
                    "|| <nowiki>%s</nowiki>",
            "sign": True
        },
        {
            "sqlnum": 43,
            "sql": """
SELECT
  page_title,
  REPLACE(STR_TO_DATE(pr_expiry, '%Y%m%d%H%i%s'), 'T', ' ساعت ')
FROM page_restrictions
JOIN page
  ON page_id = pr_page
WHERE
  page_namespace = 0
  AND pr_type = 'edit'
  AND pr_level = 'sysop'
  AND pr_expiry != 'infinity'
""",
            "out": "وپ:گزارش دیتابیس/" +
                   "مقاله‌های دارای محافظت کامل با زمان محدود",
            "cols": ["ردیف", "مقاله",  "تاریخ انقضا"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست مقاله‌هایی را نشان می‌دهد که محافظت کامل با زمان محدود
(اما نه بی‌پایان) شده‌اند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] " +
                    "|| {{عبارت چپ‌چین|{{formatnum:%s|NOSEP}}}}",
            "sign": True
        },
        {
            "sqlnum": 44,
            "sql": """
SELECT
  page_namespace,
  page_title,
  pr_type,
  STR_TO_DATE(pr_expiry, '%Y%m%d%H%i%s')
FROM page_restrictions
JOIN page
  ON page_id = pr_page
  AND pr_level = 'extendedconfirmed'
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های دارای نیمه‌محافظت ویژه",
            "cols": ["ردیف", "صفحه",  "نوع محافظت",  "پایان محافظت"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست صفحه‌هایی که نیمه‌محافظت ویژه شده‌اند، را نشان می‌دهد.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[{{ns:%s}}:%s]] || %s " +
                    "|| {{عبارت چپ‌چین|{{formatnum:%s|NOSEP}}}}",
            "sign": True
        },
        {
            "sqlnum": 45,
            "sql": """
SELECT
  p1.page_title,
  COUNT(pl_from) AS cnt
FROM page p1
JOIN categorylinks
  ON p1.page_id = cl_from
  AND cl_to = 'همه_صفحه‌های_ابهام‌زدایی'
JOIN pagelinks
  ON pl_title = page_title
  AND pl_namespace = 0
JOIN page p2
  ON pl_from = p2.page_id
  AND p2.page_namespace = 0
WHERE p1.page_namespace = 0
GROUP BY pl_title
ORDER BY cnt DESC
LIMIT 1000
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های ابهام‌زدایی پرکاربرد",
            "cols": ["ردیف", "مقاله",  "تعداد پیوندها"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست صفحه‌های ابهام‌زدایی را نشان می‌دهد که بیشترین پیوند به آن‌ها داده
شده‌است.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 46,
            "sql": """
SELECT
  page.page_title,
  GROUP_CONCAT(CONCAT('[[الگو:',tem.page_title,']]') SEPARATOR '، '),
  COUNT(tem.page_title) AS cnt
FROM page
JOIN categorylinks
  ON page_id = cl_from
  AND cl_to = 'همه_صفحه‌های_ابهام‌زدایی'
JOIN pagelinks
  ON pl_title = page_title
JOIN (
  SELECT *
  FROM page
  WHERE
    page_namespace = 10
    AND page_is_redirect = 0
) AS tem
  ON tem.page_id=pl_from
WHERE
  pl_namespace = 0
  AND pl_from_namespace=10
  AND NOT tem.page_title LIKE '%_/_%'
  AND page.page_namespace = 0
GROUP BY page.page_title
ORDER BY cnt DESC
LIMIT 1000
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های ابهام‌زدایی استفاده شده در الگو",
            "cols": ["ردیف", "مقاله", "الگوهای استفاده شده", "تعداد پیوندها"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست صفحه‌های ابهام‌زدایی که در الگو به کار رفته‌اند را نشان می‌دهد.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || %s " +
                    "|| {{formatnum:%s|NOSEP}}",
            "sign": True
        },
        {
            "sqlnum": 47,
            "sql": """
SELECT
  fap.page_title,
  enp.page_title,
  limagelist.il_to,
  limagelist.il_to
FROM fawiki_p.page AS fap
JOIN fawiki_p.langlinks AS fal
  ON fap.page_id = fal.ll_from
  AND fap.page_namespace = 0
  AND fap.page_is_redirect = 0
JOIN fawiki_p.templatelinks AS fat
  ON fat.tl_namespace=10
  AND fat.tl_from=fap.page_id
  AND (
    fat.tl_title LIKE 'جعبه%'
    OR fat.tl_title LIKE 'Infobox%'
  )
JOIN enwiki_p.page AS enp
  ON fal.ll_title=enp.page_title
  AND enp.page_namespace = 0
  AND enp.page_is_redirect = 0
JOIN (
  SELECT *
  FROM enwiki_p.imagelinks AS eni
) AS limagelist
WHERE
  fap.page_namespace = 0
  AND fal.ll_lang = 'en'
  AND fap.page_is_redirect = 0
  AND fap.page_id NOT IN (
    SELECT fai.il_from
    FROM fawiki_p.imagelinks AS fai
    WHERE
      NOT fai.il_to LIKE 'Flag_of_%'
      AND NOT fai.il_to LIKE 'Ambox_%'
      AND NOT fai.il_to LIKE 'Wiktionary%'
      AND NOT fai.il_to LIKE 'Wikibooks%'
      AND NOT fai.il_to LIKE 'Wikivoyage%'
      AND NOT fai.il_to LIKE 'Incubator%'
      AND NOT fai.il_to LIKE 'Searchtool%'
      AND NOT fai.il_to LIKE 'Speech_balloon%'
      AND NOT fai.il_to LIKE 'Crystal_Clear%'
      AND NOT fai.il_to LIKE 'Speakerlink%'
      AND NOT fai.il_to LIKE 'Loudspeaker%'
      AND NOT fai.il_to LIKE 'Padlock%'
      AND NOT fai.il_to LIKE 'Nuvola_apps_%'
      AND NOT fai.il_to LIKE 'Wikiquote%'
      AND NOT fai.il_to LIKE 'Wikisource%'
      AND NOT fai.il_to LIKE 'Wikinews%'
      AND NOT fai.il_to LIKE 'Wikiversity%'
      AND NOT fai.il_to LIKE 'Question_book%'
      AND NOT fai.il_to LIKE 'Folder_Hexagonal%'
      AND NOT fai.il_to LIKE 'Portal-puzzle%'
      AND NOT fai.il_to LIKE 'Edit-clear%'
      AND NOT fai.il_to LIKE 'Text_document_with_red_question_mark%'
      AND NOT fai.il_to LIKE '%_stub%'
      AND NOT fai.il_to LIKE 'Rod_of_Asclepius%'
      AND NOT fai.il_to LIKE 'Merge-arrows%'
      AND NOT fai.il_to LIKE '%_icon%'
      AND NOT fai.il_to LIKE '%Balloon%'
      AND NOT fai.il_to LIKE 'Mergefrom%'
      AND NOT fai.il_to LIKE 'WikiProject%'
      AND NOT fai.il_to LIKE 'Yes_check%'
      AND NOT fai.il_to LIKE 'X_mark%'
      AND NOT fai.il_to LIKE 'Blank%'
      AND NOT fai.il_to LIKE '%_Icon%'
      AND NOT fai.il_to LIKE 'Symbol_book_class%'
      AND NOT fai.il_to LIKE 'Free_and_open-source_software_logo%'
      AND NOT fai.il_to LIKE 'Red_pog%'
      AND NOT fai.il_to LIKE 'Symbol_list_class%'
      AND NOT fai.il_to LIKE 'Allah-green%'
      AND NOT fai.il_to LIKE 'Symbol_support_vote%'
      AND NOT fai.il_to LIKE 'A_coloured_voting_box%'
      AND NOT fai.il_to LIKE 'Wiki_letter_w_cropped%'
      AND NOT fai.il_to LIKE '%.wav'
      AND NOT fai.il_to LIKE '%.mid'
      AND NOT fai.il_to LIKE '%.ogg'
      AND NOT fai.il_to LIKE '%.ogv'
      AND NOT fai.il_to LIKE '%.webm'
      AND NOT fai.il_to LIKE 'Commons%'
  )
  AND enp.page_id = limagelist.il_from
  AND NOT limagelist.il_to LIKE 'Flag_of_%'
  AND NOT limagelist.il_to LIKE 'Ambox_%'
  AND NOT limagelist.il_to LIKE 'Wiktionary%'
  AND NOT limagelist.il_to LIKE 'Wikibooks%'
  AND NOT limagelist.il_to LIKE 'Wikivoyage%'
  AND NOT limagelist.il_to LIKE 'Incubator%'
  AND NOT limagelist.il_to LIKE 'Searchtool%'
  AND NOT limagelist.il_to LIKE 'Speech_balloon%'
  AND NOT limagelist.il_to LIKE 'Crystal_Clear%'
  AND NOT limagelist.il_to LIKE 'Speakerlink%'
  AND NOT limagelist.il_to LIKE 'Loudspeaker%'
  AND NOT limagelist.il_to LIKE 'Padlock%'
  AND NOT limagelist.il_to LIKE 'Nuvola_apps_%'
  AND NOT limagelist.il_to LIKE 'Wikiquote%'
  AND NOT limagelist.il_to LIKE 'Wikisource%'
  AND NOT limagelist.il_to LIKE 'Wikinews%'
  AND NOT limagelist.il_to LIKE 'Wikiversity%'
  AND NOT limagelist.il_to LIKE 'Question_book%'
  AND NOT limagelist.il_to LIKE 'Folder_Hexagonal%'
  AND NOT limagelist.il_to LIKE 'Portal-puzzle%'
  AND NOT limagelist.il_to LIKE 'Edit-clear%'
  AND NOT limagelist.il_to LIKE 'Text_document_with_red_question_mark%'
  AND NOT limagelist.il_to LIKE '%_stub%'
  AND NOT limagelist.il_to LIKE 'Rod_of_Asclepius%'
  AND NOT limagelist.il_to LIKE 'Merge-arrows%'
  AND NOT limagelist.il_to LIKE '%_icon%'
  AND NOT limagelist.il_to LIKE '%Balloon%'
  AND NOT limagelist.il_to LIKE 'Mergefrom%'
  AND NOT limagelist.il_to LIKE 'WikiProject%'
  AND NOT limagelist.il_to LIKE 'Yes_check%'
  AND NOT limagelist.il_to LIKE 'X_mark%'
  AND NOT limagelist.il_to LIKE 'Blank%'
  AND NOT limagelist.il_to LIKE '%_Icon%'
  AND NOT limagelist.il_to LIKE 'Symbol_book_class%'
  AND NOT limagelist.il_to LIKE 'Free_and_open-source_software_logo%'
  AND NOT limagelist.il_to LIKE 'Red_pog%'
  AND NOT limagelist.il_to LIKE 'Symbol_list_class%'
  AND NOT limagelist.il_to LIKE 'Allah-green%'
  AND NOT limagelist.il_to LIKE 'Symbol_support_vote%'
  AND NOT limagelist.il_to LIKE 'A_coloured_voting_box%'
  AND NOT limagelist.il_to LIKE 'Wiki_letter_w_cropped%'
  AND NOT limagelist.il_to LIKE '%.svg'
  AND NOT limagelist.il_to LIKE '%.png'
  AND NOT limagelist.il_to LIKE '%.ogg'
  AND NOT limagelist.il_to LIKE '%.webm'
  AND NOT limagelist.il_to LIKE '%.ogv'
  AND NOT limagelist.il_to LIKE '%.wav'
  AND NOT limagelist.il_to LIKE '%.mid'
  AND NOT limagelist.il_to LIKE 'Commons%'
GROUP BY limagelist.il_to
ORDER BY fap.page_title;
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های نیازمند پرونده همسنگ",
            "cols": [
                "ردیف",
                "مقالهٔ ویکی‌پدیای فارسی",
                "مقالهٔ ویکی‌پدیای انگلیسی",
                "پروندهٔ به کار رفته در ویکی‌پدیای انگلیسی",
                "نام پرونده"
            ],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست صفحه‌هایی در ویکی‌پدیای فارسی را نشان می‌دهد که صفحهٔ نظیرشان در
ویکی‌پدیای انگلیسی یک تصویر شاخص دارد.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || [[:en:%s]] " +
                    "|| [[File:%s|60px]]|| %s",
            "sign": True
        },
        {
            "sqlnum": 48,
            "sql": """
SELECT
  rev_user_text,
  STR_TO_DATE(LEFT(min(rev_timestamp), 8), '%Y%m%d') AS sunrise,
  STR_TO_DATE(LEFT(min(sunset), 8), '%Y%m%d') AS sunset,
  old_edits,
  COUNT(rev_id) AS recent_edits,
  GROUP_CONCAT(DISTINCT(ug_group) SEPARATOR ' ') AS groups,
  CASE
    WHEN ipb_user IS NULL THEN ''
    ELSE '{{بله}}'
  END AS blocked
FROM revision
JOIN (
  SELECT
    rev_user old_user,
    max(rev_timestamp) sunset,
    COUNT(rev_id) AS old_edits
  FROM revision
  WHERE
    rev_user <> 0
    AND rev_timestamp < CONCAT(
      YEAR(CURDATE()) - 3,
      LPAD(MONTH(CURDATE()) , 2, 0),
      '01000000'
    )
  GROUP BY rev_user
) old
  ON old_user = rev_user
LEFT JOIN user_groups
  ON rev_user = ug_user
LEFT JOIN ipblocks
  ON ipb_user = rev_user
WHERE
  rev_user <> 0
  AND rev_timestamp > CONCAT(
    YEAR(CURDATE()),
    LPAD(MONTH(CURDATE()) , 2, 0),
    '01000000'
  )
  AND rev_user NOT IN (
    SELECT rev_user
    FROM revision
    WHERE
      rev_user <> 0
      AND rev_timestamp < CONCAT(
        YEAR(CURDATE()),
        LPAD(MONTH(CURDATE()) , 2, 0),
        '01000000')
      AND rev_timestamp > CONCAT(
        YEAR(CURDATE()) - 3,
        LPAD(MONTH(CURDATE()) , 2, 0),
        '01000000'
      )
)
GROUP BY rev_user_text
""",
            "out": "وپ:گزارش دیتابیس/حساب‌های از آب‌نمک درآمده",
            "cols": [
                "ردیف",
                "کاربر",
                "اولین ویرایش{{سخ}} در ماه جاری",
                "آخرین ویرایش{{سخ}} قبل از مرخصی",
                "ویرایش‌های پیش{{سخ}} از غیبت",
                "ویرایش‌های{{سخ}} پس از ظهور",
                "گروه‌های کاربری",
                "قطع دسترسی"
            ],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست کاربرانی را نشان می‌دهد که از اول ماه جاری میلادی ویرایشی
داشته‌اند، در سه سال منتهی به ماه جاری میلادی هیچ ویرایشی نداشته‌اند، و در زمان
پیش از آن دورهٔ سه‌ساله دست کم یک ویرایش کرده‌اند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] " +
                    "|| {{formatnum:%s|NOSEP}} || {{formatnum:%s|NOSEP}} " +
                    "|| {{formatnum:%s}} || {{formatnum:%s}} || %s || %s",
            "sign": True
        },
        {
            "sqlnum": 49,
            "sql": """
SELECT
  CASE
    WHEN page_namespace = 0 THEN page_title
    ELSE CONCAT(':{{ns:', page_namespace, '}}:', page_title)
  END AS page_title,
  cl_to
FROM (
  SELECT
    cl_from,
    cl_to
  FROM categorylinks
  JOIN page
    ON cl_to = page_title
    AND page_namespace = 14
  WHERE page_is_redirect = 1
  LIMIT 5000
) redir
JOIN page
  ON cl_from = page_id
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های دارای ردهٔ تغییرمسیر",
            "cols": ["ردیف", "صفحه", "رده"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست صفحه‌هایی را نشان می‌دهد که در یک یا چند رده قرار دارند که آن
رده‌ها خود تغییر مسیر هستند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || [[:رده:%s]] ",
            "sign": True
        },
        {
            "sqlnum": 50,
            "sql": """
SELECT
  CASE
    WHEN page_namespace = 0 THEN page_title
    ELSE CONCAT(':{{ns:', page_namespace, '}}:', page_title)
  END AS page_title,
  cl_to
FROM (
  SELECT
    cl1.cl_from,
    cl1.cl_to
  FROM categorylinks cl1
  JOIN page
    ON cl1.cl_to = page_title
    AND page_namespace = 14
  JOIN categorylinks cl2
   ON page_id = cl2.cl_from
   AND cl2.cl_to = 'رده‌های_منتقل‌شده'
   LIMIT 5000
) redir
JOIN page
  ON cl_from = page_id
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های دارای ردهٔ منتقل‌شده",
            "cols": ["ردیف", "صفحه", "رده"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست صفحه‌هایی را نشان می‌دهد که در یک یا چند رده قرار دارند که آن
رده‌ها خود تغییر مسیر هستند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || [[:رده:%s]] ",
            "sign": True
        },
        {
            "sqlnum": 51,
            "sql": """
SELECT DISTINCT
  rev_user_text,
  COUNT(*) cnt,
  CASE
    WHEN ufg_group IS NULL THEN ''
    ELSE '{{خیر|بله}}'
  END AS lostautopatrol
FROM revision
LEFT JOIN user_former_groups
  ON rev_user = ufg_user
  AND ufg_group IN ('autopatrolled', 'autopatrol')
LEFT JOIN page
  ON rev_page = page_id
WHERE
  rev_parent_id = 0
  AND page_is_redirect = 0
  AND page_namespace = 0
  AND rev_timestamp >
    CASE
      WHEN MONTH(CURDATE()) = 1 THEN CONCAT(
        YEAR(CURDATE()) - 1,
        '12',
        LPAD(DAY(CURDATE()), 2, 0),
        '000000'
      )
      ELSE CONCAT(
        YEAR(CURDATE()),
        LPAD(MONTH(CURDATE()) - 1, 2, 0),
        LPAD(DAY(CURDATE()), 2, 0),
        '000000'
      )
    END
  AND rev_user NOT IN (
    SELECT ug_user
    FROM user_groups
    WHERE ug_group IN ('autopatrolled', 'sysop', 'bot')
  )
  AND rev_user <> 0 /* anonymous users */
  AND rev_user <> 374638 /* پیام به کاربر جدید */
GROUP BY
  rev_user_text,
  ufg_group
HAVING cnt > 20
ORDER BY cnt DESC
""",
            "out": "وپ:گزارش دیتابیس/نامزدهای احتمالی گشت خودکار",
            "cols": [
                "ردیف",
                "کاربر",
                "تعداد مقاله‌های جدید در یک ماه اخیر",
                "قبلاً گشت خودکار را از دست داده؟"
            ],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست کاربرانی را نشان می‌دهد که اخیراً بسیار مقاله ساخته‌اند و ممکن است
نامزد خوبی برای دسترسی گشت خودکار باشند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] " +
                    "|| {{formatnum:%s}} || %s ",
            "sign": True
        },
        {
            "sqlnum": 52,
            "sql": """
SELECT
  page_title AS title,
  cnt
FROM (
  SELECT
    ll_from AS page_id,
    COUNT(ll_lang) AS cnt
  FROM enwiki_p.langlinks
  GROUP BY ll_from
  HAVING
    COUNT(ll_lang)>=1
    AND MAX(ll_lang='fa') = 0
) AS sq
JOIN enwiki_p.page p
  ON p.page_id = sq.page_id
WHERE page_namespace=828
ORDER BY
  cnt DESC,
  page_title
""",
            "out": "وپ:گزارش دیتابیس/پودمان‌های مورد نیاز",
            "cols": ["ردیف", "پودمان", "تعداد میان‌ویکی"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[:en:Module:%s]] " +
                    "|| {{formatnum:%s}} ",
            "sign": True
        },
        {
            "sqlnum": 53,
            "sql": """
SELECT
  page_title,
  COUNT(*) reverts
FROM revision
JOIN page
  ON page_id = rev_page
WHERE
  rev_comment LIKE '%واگردانده شد'
  AND rev_timestamp >
    CONCAT(DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 1 YEAR), '%Y%m%d'), '000000')
  AND page_namespace = 0
GROUP BY rev_page
HAVING COUNT(*) > 10
ORDER BY reverts DESC
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های دارای بیشترین واگردانی",
            "cols": ["ردیف", "پودمان", "تعداد میان‌ویکی"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست مقاله‌های را نشان می‌دهد که در یکسال اخیر دست کم ۱۰ بار واگردانی
شده‌اند. ممکن است این مقاله‌ها نامزدهای خوبی برای محافظت یا
پی‌گیری توسط مدیران باشند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] || {{formatnum:%s}} ",
            "sign": True
        },
        {
            "sqlnum": 54,
            "sql": """
SELECT page_title
FROM page
WHERE page_id IN (
        SELECT cl_from
        FROM categorylinks
        WHERE cl_to  LIKE 'درگذشتگان%'
        )
    and page_id IN (
        SELECT cl_from
        FROM categorylinks
        WHERE cl_to LIKE '%افراد_زنده%'
    )
    AND page_is_redirect = 0;
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌‌های دارای رده‌های درگذشتگان و افراد زنده",
            "cols": ["ردیف", "مقاله"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست مقاله‌های را نشان می‌دهد که دارای رده‌های درگذشتگان و افراد زنده هستند و باید یکی از رده‌ها بر پایهٔ متن  مقاله حذف شوند. 

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[%s]] ",
            "sign": True
        },
        {
            "sqlnum": 55,
            "sql": """
USE fawiki_p;
select users.user_name, REGEXP_REPLACE(GROUP_CONCAT(DISTINCT(ug_group) SEPARATOR ' '),'(uploader|autopatrolled|ipblock\-exempt)','') AS groups,active_days
from
(
SELECT
  user_id,user_name,
  COUNT(*) AS active_days
FROM
(
  SELECT DISTINCT
    rev_user,
    LEFT(rev_timestamp, 8)
  FROM revision
  WHERE
    rev_timestamp > CONCAT(DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 1 YEAR), '%Y%m%d'), '000000')
) AS rev_days
JOIN user
  ON rev_user = user_id
LEFT JOIN user_groups
  ON user_id = ug_user
  AND ug_group = 'bot'
WHERE
   ug_user IS NULL
   AND user_id NOT IN ('374638','285515')# پیام_به_کاربر_جدید and FawikiPatroller
GROUP BY
  rev_user
HAVING
  COUNT(*) > 100
) as users
join user_groups
ON users.user_id = ug_user
GROUP BY
  user_id
ORDER BY
 users.active_days DESC;
""",
            "out": "وپ:گزارش دیتابیس/کاربران بر اساس تعداد روزهای فعال در سال اخیر",
            "cols": ["ردیف", "گروه کاربری","کاربر", "روزهای فعال"],
            "summary": "به روز کردن آمار",
            "pref": """
[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]
این فهرست کاربران را نشان می‌دهد که در یکسال اخیر بیش  از صد روز را در ویکی‌پدیا ویرایش کرده‌اند.

آخرین به روز رسانی: ~~~~~
""",
            "frmt": "| {{formatnum:%d}} || [[User:%s|]] || {{formatnum:%s}} ",
            "sign": True
        },
    ]

    for t in tasks:
        if sqlnum:
            if sqlnum != t["sqlnum"]:
                continue
        bot = stats.StatsBot(
            t["sql"],
            t["out"],
            t["cols"],
            t["summary"],
            t["pref"],
            t["frmt"],
            t["sqlnum"],
            t["sign"])
        bot.run()

if __name__ == "__main__":
    try:
        sqlnum = int(sys.argv[1])
    except:
        sqlnum = 0
    main(sqlnum)
