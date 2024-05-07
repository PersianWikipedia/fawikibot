#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
weekly-slow.py - a wrapper for stats.py to be called every week.
usage:
    python pwb.py weekly-slow <sqlnum> <maxtime>
    or
    python pwb.py weekly-slow <sqlnum>
    or
    python pwb.py weekly-slow
parameters:
    <sqlnum>: (optinal) integer Used to run specifice queries
    <maxtime>: (optional) maximum execution time for the specified query
"""
#
# (C) Pywikibot team, 2006-2014
# (C) w:fa:User:Huji, 2015
#
# Distributed under the terms of the MIT license.
#


import sys
import stats


def main(sqlnum, maxtime):
    tasks = [
        {
            "sqlnum": 1,
            "sql": """
SELECT
  page_title,
  cat_pages,
  cat_subcats,
  cat_files,
  COUNT(ll_lang)
FROM page
JOIN category
  ON page_title = cat_title
LEFT JOIN categorylinks
  ON page_id = cl_from
LEFT JOIN langlinks
  ON page_id = ll_from
WHERE
  page_namespace = 14
  AND page_is_redirect = 0
  AND cl_from IS NULL
GROUP BY
  page_title,
  cat_pages,
  cat_subcats,
  cat_files
LIMIT 5000
""",
            "out": "وپ:گزارش دیتابیس/رده‌های رده‌بندی نشده",
            "cols": [
                "ردیف",
                "رده",
                "تعداد صفحه‌ها",
                "تعداد زیررده‌ها",
                "تعداد پرونده‌ها",
                "تعداد میان‌ویکی",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:رده:%s]] || %s || %s "
            + "|| %s || %s",
            "sign": True,
        },
        {
            "sqlnum": 2,
            "sql": """
SELECT
  page_title,
  STR_TO_DATE(LEFT(rev_timestamp, 8), '%Y%m%d')
FROM page
JOIN revision
  ON page_latest = rev_id
LEFT JOIN categorylinks
  ON page_id = cl_from
WHERE
  page_namespace = 10
  AND cl_to IS NULL
  AND page_is_redirect = 0
ORDER BY page_latest
LIMIT 5000
""",
            "out": "وپ:گزارش دیتابیس/الگوهای رده‌بندی نشده",
            "cols": ["ردیف", "الگو", "آخرین ویرایش"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| %d || [[الگو:%s]] || %s",
            "sign": True,
        },
        {
            "sqlnum": 3,
            "sql": """
SELECT
  user_name,
  user_editcount
FROM user
LEFT JOIN user_groups
  ON user_id = ug_user
  AND ug_group = "bot"
WHERE
  ug_group IS NULL
  AND user_id <> 374638 -- پیام به کاربر جدید
ORDER BY user_editcount DESC
LIMIT 500
""",
            "out": "وپ:گزارش دیتابیس/کاربران بر اساس تعداد ویرایش‌ها",
            "cols": ["ردیف", "کاربر", "تعداد ویرایش"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}"
            + "\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
            + "|| {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 4,
            "sql": """
SELECT
  actor_name,
  SUM(
    CASE
      WHEN page_namespace = 0 THEN 1
      ELSE 0
    END
  ) article,
  SUM(
    CASE
      WHEN page_namespace = 10 THEN 1
      ELSE 0
    END
  ) tpl,
  SUM(
    CASE
      WHEN page_namespace = 12 THEN 1
      ELSE 0
    END
  ) helppage,
  SUM(
    CASE
      WHEN page_namespace = 14 THEN 1
      ELSE 0
    END
  ) cat,
  SUM(
    CASE
      WHEN page_namespace = 100 THEN 1
      ELSE 0
    END
  ) portal,
  COUNT(rev_first) tot
FROM revision r
JOIN (
  select
    MIN(rev_id) rev_first,
    rev_page
  FROM revision
  GROUP BY rev_page
) f
  ON r.rev_id = f.rev_first
JOIN page
  ON page_id = r.rev_page
JOIN actor
  ON rev_actor = actor_id
LEFT JOIN user_groups
  ON actor_user = ug_user
  AND ug_group = "bot"
WHERE
  actor_user <> 0
  AND ug_group IS NULL
  AND page_namespace IN (
    0,
    10,
    12,
    14,
    100
  )
GROUP BY rev_actor
ORDER BY tot desc
LIMIT 300
""",
            "out": "وپ:گزارش دیتابیس/"
            + "کاربران ویکی‌پدیا بر پایه تعداد ایجاد صفحه‌ها",
            "cols": [
                "ردیف",
                "کاربر",
                "مقاله جدید",
                "الگوی جدید",
                "راهنمای جدید",
                "رده جدید",
                "درگاه جدید",
                "جمع کل",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 5,
            "sql": """
SELECT
  actor_name,
  SUM(
    CASE
      WHEN page_namespace = 0 THEN 1
      ELSE 0
    END
  ) article,
  SUM(
    CASE
      WHEN page_namespace = 10 THEN 1
      ELSE 0
    END
  ) tpl,
  SUM(
    CASE
      WHEN page_namespace = 12 THEN 1
      ELSE 0
    END
  ) helppage,
  SUM(
    CASE
      WHEN page_namespace = 14 THEN 1
      ELSE 0
    END
  ) cat,
  SUM(
    CASE
      WHEN page_namespace = 100 THEN 1
      ELSE 0
    END
  ) portal,
  COUNT(rev_first) tot
FROM revision_userindex r
JOIN (
  SELECT
    MIN(rev_id) rev_first,
    rev_page
  FROM revision
  GROUP BY rev_page
) f
  ON r.rev_id = f.rev_first
JOIN page
  ON page_id = r.rev_page
JOIN actor
  ON rev_actor = actor_id
where
  actor_user > 0
  AND page_namespace IN (
    0,
    10,
    12,
    14,
    100
  )
GROUP BY rev_actor
ORDER BY tot DESC
limit 200
""",
            "out": "وپ:گزارش دیتابیس/"
            + "کاربران ویکی‌پدیا بر پایه تعداد ایجاد صفحه‌ها/ربات",
            "cols": [
                "ردیف",
                "کاربر",
                "مقاله جدید",
                "الگوی جدید",
                "راهنمای جدید",
                "رده جدید",
                "درگاه جدید",
                "جمع کل",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]]  "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 6,
            "sql": """
SELECT
  actor_name,
  STR_TO_DATE(LEFT(MIN(rev_timestamp), 8), '%Y%m%d'),
  SUM(
    CASE
      WHEN rev_len BETWEEN 0 AND 2048 THEN 1
      ELSE 0
    END
  ),
  SUM(
    CASE
      WHEN rev_len BETWEEN 2048 AND 15 * 1024 THEN 1
      ELSE 0
    END
  ),
  SUM(
    CASE
      WHEN rev_len BETWEEN 15 * 1024 AND 70 * 1024 THEN 1
      ELSE 0
    END
  ),
  SUM(
    CASE
      WHEN rev_len > 70 * 1024 THEN 1
      ELSE 0
    END
  ),
  COUNT(rev_first) tot
FROM revision_userindex r
JOIN (
  SELECT
    MIN(rev_id) rev_first,
    rev_page
  FROM revision
  GROUP BY rev_page
) f
  ON r.rev_id = f.rev_first
JOIN page
  ON page_id = r.rev_page
JOIN actor_revision
  ON rev_actor = actor_id
LEFT JOIN user_groups
  on actor_user = ug_user
  AND ug_group = "bot"
WHERE
  actor_user <> 0
  AND ug_group IS NULL
  AND page_namespace = 0
  AND page_is_redirect = 0
GROUP BY rev_actor
ORDER BY tot DESC
LIMIT 200
""",
            "out": "وپ:گزارش دیتابیس/"
            + "کاربران ویکی‌پدیا بر پایه تعداد ایجاد مقاله و حجم مقاله",
            "cols": [
                "ردیف",
                "کاربر",
                "اولین ایجاد مقاله",
                "مقاله ۰ تا ۲ کیلوبایت",
                "مقاله ۲ تا ۱۵ کیلوبایت",
                "مقاله ۱۵ تا ۷۰ کیلوبایت",
                "مقاله بالای ۷۰ کیلوبایت",
                "جمع کل",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}"
            + "\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
            + "|| {{formatnum:%s|NOSEP}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 7,
            "sql": """
SELECT
  actor_name,
  STR_TO_DATE(LEFT(MIN(rev_timestamp), 8), '%Y%m%d'),
  SUM(CASE
    WHEN rev_len BETWEEN 0 AND 2048 THEN 1
    ELSE 0
  END),
  SUM(CASE
    WHEN rev_len BETWEEN 2048 AND 15 * 1024 THEN 1
    ELSE 0
  END),
  SUM(CASE
    WHEN rev_len BETWEEN 15 * 1024 AND 70 * 1024 THEN 1
    ELSE 0
  END),
  SUM(CASE
    WHEN rev_len > 70 * 1024 THEN 1
    ELSE 0
  END),
  COUNT(rev_first) tot
FROM revision r
JOIN actor
  ON rev_actor = actor_id
JOIN (
  select min(rev_id) rev_first, rev_page from revision group by rev_page
) f
  ON r.rev_id = f.rev_first
JOIN page
  ON page_id = r.rev_page
WHERE
  actor_user <> 0
  AND page_namespace = 0
  AND page_is_redirect = 0
GROUP BY actor_user
ORDER BY tot desc
LIMIT 200
""",
            "out": "وپ:گزارش دیتابیس/"
            + "کاربران ویکی‌پدیا بر پایه تعداد ایجاد مقاله و حجم مقاله/"
            + "ربات",
            "cols": [
                "ردیف",
                "کاربر",
                "اولین ایجاد مقاله",
                "مقاله ۰ تا ۲ کیلوبایت",
                "مقاله ۲ تا ۱۵ کیلوبایت",
                "مقاله ۱۵ تا ۷۰ کیلوبایت",
                "مقاله بالای ۷۰ کیلوبایت",
                "جمع کل",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}"
            + "\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
            + "|| {{formatnum:%s|NOSEP}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 8,
            "sql": """
SELECT
  actor_name,
  SUM(CASE
    WHEN page_namespace = 0 THEN 1
    ELSE 0
  END) AS article,
  SUM(CASE
    WHEN page_namespace = 1 THEN 1
    ELSE 0
  END) AS articletalk,
  SUM(CASE
    WHEN page_namespace = 2 THEN 1
    ELSE 0
  END) AS usr,
  SUM(CASE
    WHEN page_namespace = 3 THEN 1
    ELSE 0
  END) AS usrtalk,
  SUM(CASE
    WHEN page_namespace = 4 THEN 1
    ELSE 0
  END) AS proj,
  SUM(CASE
    WHEN page_namespace = 5 THEN 1
    ELSE 0
  END) AS projtalk,
  SUM(CASE
    WHEN page_namespace = 6 THEN 1
    ELSE 0
  END) AS file,
  SUM(CASE
    WHEN page_namespace = 7 THEN 1
    ELSE 0
  END) AS filetalk,
  SUM(CASE
    WHEN page_namespace = 8 THEN 1
    ELSE 0
  END) AS mw,
  SUM(CASE
    WHEN page_namespace = 89 THEN 1
    ELSE 0
  END) AS mwtalk,
  SUM(CASE
    WHEN page_namespace = 10 THEN 1
    ELSE 0
  END) AS tpl,
  SUM(CASE
    WHEN page_namespace = 11 THEN 1
    ELSE 0
  END) AS tpltalk,
  SUM(CASE
    WHEN page_namespace = 12 THEN 1
    ELSE 0
  END) AS helppage,
  SUM(CASE
    WHEN page_namespace = 13 THEN 1
    ELSE 0
  END) AS helptalk,
  SUM(CASE
    WHEN page_namespace = 14 THEN 1
    ELSE 0
  END) AS cat,
  SUM(CASE
    WHEN page_namespace = 15 THEN 1
    ELSE 0
  END) AS cattalk,
  SUM(CASE
    WHEN page_namespace = 100 THEN 1
    ELSE 0
  END) AS portal,
  SUM(CASE
    WHEN page_namespace = 101 THEN 1
    ELSE 0
  END) AS portaltalk,
  SUM(CASE
    WHEN page_namespace = 828 THEN 1
    ELSE 0
  END) AS module,
  SUM(CASE
    WHEN page_namespace = 829 THEN 1
    ELSE 0
  END) AS moduletalk,
  COUNT(*) AS tot
FROM revision
JOIN actor
  ON rev_actor = actor_id
JOIN page
  ON page_id = rev_page
JOIN user
  ON actor_user = user_id
LEFT JOIN user_groups
  ON actor_user = ug_user
  AND ug_group = 'bot'
WHERE
  actor_user <> 0
  AND actor_user <> 374638 /* پیام به کاربر جدید */
  AND ug_group IS NULL
GROUP BY actor_name
ORDER BY tot DESC
LIMIT 100
""",
            "out": "وپ:گزارش دیتابیس/"
            + "کاربران ویکی‌پدیا بر پایه تعداد ویرایش در فضاهای نام",
            "cols": [
                "ردیف",
                "کاربر",
                "مقاله",
                "بحث",
                "کاربر",
                "بحث کاربر",
                "ویکی‌پدیا",
                "بحث ویکی‌پدیا",
                "پرونده",
                "بحث پرونده",
                "مدیاویکی",
                "بحث مدیاویکی",
                "الگو",
                "بحث الگو",
                "راهنما",
                "بحث راهنما",
                "رده",
                "بحث رده",
                "درگاه",
                "بحث درگاه",
                "پودمان",
                "بحث پودمان",
                "جمع کل",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 9,
            "sql": """
SELECT
  actor_name,
  SUM(CASE
    WHEN page_namespace = 0 THEN 1
    ELSE 0
  END) AS article,
  SUM(CASE
    WHEN page_namespace = 1 THEN 1
    ELSE 0
  END) AS articletalk,
  SUM(CASE
    WHEN page_namespace = 2 THEN 1
    ELSE 0
  END) AS usr,
  SUM(CASE
    WHEN page_namespace = 3 THEN 1
    ELSE 0
  END) AS usrtalk,
  SUM(CASE
    WHEN page_namespace = 4 THEN 1
    ELSE 0
  END) AS proj,
  SUM(CASE
    WHEN page_namespace = 5 THEN 1
    ELSE 0
  END) AS projtalk,
  SUM(CASE
    WHEN page_namespace = 6 THEN 1
    ELSE 0
  END) AS file,
  SUM(CASE
    WHEN page_namespace = 7 THEN 1
    ELSE 0
  END) AS filetalk,
  SUM(CASE
    WHEN page_namespace = 8 THEN 1
    ELSE 0
  END) AS mw,
  SUM(CASE
    WHEN page_namespace = 89 THEN 1
    ELSE 0
  END) AS mwtalk,
  SUM(CASE
    WHEN page_namespace = 10 THEN 1
    ELSE 0
  END) AS tpl,
  SUM(CASE
    WHEN page_namespace = 11 THEN 1
    ELSE 0
  END) AS tpltalk,
  SUM(CASE
    WHEN page_namespace = 12 THEN 1
    ELSE 0
  END) AS helppage,
  SUM(CASE
    WHEN page_namespace = 13 THEN 1
    ELSE 0
  END) AS helptalk,
  SUM(CASE
    WHEN page_namespace = 14 THEN 1
    ELSE 0
  END) AS cat,
  SUM(CASE
    WHEN page_namespace = 15 THEN 1
    ELSE 0
  END) AS cattalk,
  SUM(CASE
    WHEN page_namespace = 100 THEN 1
    ELSE 0
  END) AS portal,
  SUM(CASE
    WHEN page_namespace = 101 THEN 1
    ELSE 0
  END) AS portaltalk,
  SUM(CASE
    WHEN page_namespace = 828 THEN 1
    ELSE 0
  END) AS module,
  SUM(CASE
    WHEN page_namespace = 829 THEN 1
    ELSE 0
  END) AS moduletalk,
  COUNT(rev_id) AS tot
FROM revision
JOIN actor
  ON rev_actor = actor_id
JOIN page
  ON page_id = rev_page
WHERE
  actor_user <> 0
  and actor_user <> 374638 /* پیام به کاربر جدید */
GROUP BY actor_name
ORDER BY tot DESC
LIMIT 100
""",
            "out": "وپ:گزارش دیتابیس/"
            + "کاربران ویکی‌پدیا بر پایه تعداد ویرایش در فضاهای نام/ربات",
            "cols": [
                "ردیف",
                "کاربر",
                "مقاله",
                "بحث",
                "کاربر",
                "بحث کاربر",
                "ویکی‌پدیا",
                "بحث ویکی‌پدیا",
                "پرونده",
                "بحث پرونده",
                "مدیاویکی",
                "بحث مدیاویکی",
                "الگو",
                "بحث الگو",
                "راهنما",
                "بحث راهنما",
                "رده",
                "بحث رده",
                "درگاه",
                "بحث درگاه",
                "پودمان",
                "بحث پودمان",
                "جمع کل",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}} || {{formatnum:%s}} "
            + "|| {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 10,
            "sql": """
SELECT
  CONCAT(
    CASE
      WHEN page_namespace = 0 THEN ''
      ELSE ":"
    END,
    "{{ns:", page_namespace, "}}:",
    page_title
  ),
  STR_TO_DATE(LEFT(MIN(rev_timestamp), 8), '%Y%m%d') AS first_edit,
  STR_TO_DATE(LEFT(MAX(rev_timestamp), 8), '%Y%m%d') AS last_edit,
  COUNT(*)
FROM revision
JOIN page ON page_id = rev_page
GROUP BY
  page_namespace,
  page_title
ORDER BY
  COUNT(*) DESC,
  page_title ASC
LIMIT 1000
""",
            "out": "وپ:گزارش دیتابیس/پرویرایش‌ترین صفحه‌ها",
            "cols": [
                "ردیف",
                "صفحه",
                "اولین ویرایش",
                "آخرین ویرایش",
                "تعداد ویرایش",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}"
            + "\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[%s]] || {{formatnum:%s|NOSEP}} "
            + "|| {{formatnum:%s|NOSEP}} || {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 11,
            "sql": """
SELECT
  actor_name,
  STR_TO_DATE(LEFT(MAX(rev_timestamp), 8), '%Y%m%d') AS lastedit,
  COUNT(rev_id) cnt
FROM revision_userindex
JOIN actor_revision
  ON rev_actor = actor_id
JOIN user_groups
  ON actor_user = ug_user
  AND ug_group = 'autopatrolled'
GROUP BY rev_actor
ORDER BY cnt
LIMIT 1000
""",
            "out": "وپ:گزارش دیتابیس/کاربران گشت خودکار بر پایه تعداد ویرایش",
            "cols": ["ردیف", "کاربر", "آخرین ویرایش", "تعداد کل ویرایش‌ها"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
            + "|| {{formatnum:%s|NOSEP}} || {{formatnum:%s}}",
            "sign": True,
        },
        {
            "sqlnum": 12,
            "sql": """
SELECT
  lt_title,
  COUNT(*)
FROM linktarget
JOIN pagelinks
  ON lt_id = pl_target_id
LEFT JOIN page AS p1
  ON p1.page_namespace = lt_namespace
  AND p1.page_title = lt_title
JOIN logging_userindex
  ON lt_namespace = log_namespace
  AND lt_title = log_title
  AND log_type = 'delete'
JOIN page AS p2
  ON pl_from = p2.page_id
WHERE
  p1.page_id IS NULL
  AND lt_namespace = 0
GROUP BY lt_title
ORDER BY 2 DESC
LIMIT 1000
""",
            "out": "وپ:گزارش دیتابیس/پیوند به مقاله‌های حذف شده",
            "cols": ["ردیف", "مقاله", "تعداد پیوندهای ورودی"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[%s]] || {{formatnum:%s}} ",
            "sign": True,
        },
        {
            "sqlnum": 13,
            "sql": """
SELECT
  CONCAT('الگو:', lt_title),
  COUNT(*),
  GROUP_CONCAT(
    CONCAT ('[[',p2.page_namespace,':',p2.page_title,']]')
    SEPARATOR "، "
  )
FROM templatelinks
JOIN linktarget
  ON tl_target_id = lt_id
JOIN logging
  ON lt_namespace = log_namespace
  AND lt_title = log_title
  AND log_type = "delete"
JOIN page AS p2
  ON tl_from = p2.page_id
LEFT JOIN page AS p1
  ON p1.page_namespace = lt_namespace
  AND p1.page_title = lt_title
WHERE
  p1.page_id IS NULL
  AND lt_namespace = 10
GROUP BY lt_title
ORDER BY COUNT(*) DESC
LIMIT 1000
""",
            "out": "وپ:گزارش دیتابیس/پیوند به الگوهای حذف شده",
            "cols": ["ردیف", "الگو", "تعداد پیوند به", "صفحات به کار رفته"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[%s]] || {{formatnum:%s}} "
            + "|| %s",
            "sign": True,
        },
        {
            "sqlnum": 14,
            "sql": """
SELECT
  page_title,
  STR_TO_DATE(LEFT(MIN(rev_timestamp), 8), '%Y%m%d'),
  COUNT(ll_lang)
FROM page
JOIN category
  ON page_title = cat_title
JOIN revision
  ON rev_page = page_id
  AND rev_parent_id = 0
LEFT JOIN categorylinks
  ON page_title = cl_to
LEFT JOIN templatelinks
  ON tl_from = page_id
LEFT JOIN linktarget
  ON tl_target_id = lt_id
  AND lt_title IN (
    'رده_خالی',
    'رده_بهتر',
    'رده_ابهام‌زدایی',
    'رده_ردیابی‌کردن',
    'رده_ردیابی_کردن',
    'رده_ردیابی'
  )
LEFT JOIN langlinks
  ON page_id = ll_from
WHERE
  page_namespace = 14
  AND page_is_redirect = 0
  AND cl_to IS NULL
  AND tl_target_id IS NULL
GROUP BY
  page_title,
  rev_timestamp
ORDER BY
 COUNT(ll_lang),
 page_title
LIMIT 5000
""",
            "out": "وپ:گزارش دیتابیس/رده‌های خالی",
            "cols": ["ردیف", "رده", "تاریخ ایجاد", "تعداد میان‌ویکی"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d|NOSEP}} || [[:رده:%s]] "
            + "|| {{formatnum:%s|NOSEP}} || {{formatnum:%s|}}",
            "sign": True,
        },
        {
            "sqlnum": 17,
            "sql": """
SELECT
  actor_name,
  SUM(freq) TotalEdits,
  FORMAT(100 * SUM(
    CASE
      WHEN page_namespace = 0 THEN freq
      ELSE 0
    END
  ) / SUM(freq), 1) ContentEdits,
  FORMAT(100 * SUM(
    CASE
      WHEN page_namespace IN (8, 10) THEN freq
      ELSE 0
    END
  ) / SUM(freq), 1) TechnicalEdits,
  FORMAT(100 * SUM(
    CASE
      WHEN page_namespace IN (4, 5) THEN freq
      ELSE 0
    END
  ) / SUM(freq), 1) ProjectDiscussionEdits,
  FORMAT(100 * SUM(
    CASE
      WHEN page_namespace IN (1, 3, 7, 9, 11, 13) THEN freq
      ELSE 0
    END
  ) / SUM(freq), 1) OtherDiscussionEdits,
  FORMAT(100 * SUM(
    CASE
      WHEN page_namespace NOT IN (
        0,
        1,
        3,
        4,
        5,
        7,
        8,
        9,
        10,
        11,
        13
      ) THEN freq
      ELSE 0
    END
  ) / SUM(freq), 1) AllOtherEdits
FROM (
  SELECT
    actor_name,
    page_namespace,
    COUNT(*) freq
  FROM revision
  JOIN actor
    ON actor_id = rev_actor
  JOIN page
    ON rev_page = page_id
  WHERE actor_user IN
  (
    SELECT actor_user
    FROM revision
    JOIN actor
      ON rev_actor = actor_id
    LEFT JOIN user_groups
      ON actor_user = ug_user
      AND ug_group = 'bot'
    WHERE
      rev_timestamp > DATE_FORMAT(
        DATE_SUB(NOW(), INTERVAL 30 DAY),
        '%Y%m%d000000'
      )
      AND actor_user <> 0
      AND actor_user NOT IN (
        374638, /* پیام به کاربر جدید */
        285515 /* FawikiPatroller */
      )
      AND ug_user IS NULL
  )
  GROUP BY
    actor_user,
    page_namespace
) last30days
GROUP BY actor_name
ORDER BY
  SUM(freq) DESC,
  actor_name DESC
LIMIT 1000
""",
            "out": "وپ:گزارش دیتابیس/کاربران فعال در یک ماه اخیر",
            "cols": [
                "ردیف",
                "کاربر",
                "تعداد کل ویرایش‌ها",
                "ویرایش در مقاله‌ها",
                "ویرایش‌های فنی",
                "بحث‌های پروژه",
                "سایر بحث‌ها",
                "سایر ویرایش‌ها",
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}"
            + "\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s|]] "
            + "|| {{formatnum:%s}} || %s%% || %s%% || %s%% || %s%% "
            + "|| %s%% ",
            "sign": True,
        },
        {
            "sqlnum": 18,
            "sql": """
SELECT
  user_name,
  MAX(iwlinks) AS h_index
FROM
(
  SELECT
    t1.actor_user,
    t1.iwlinks,
    SUM(t2.freq) AS total
  FROM
  (
    SELECT
      actor_user,
      iwlinks,
      COUNT(*) AS freq
    FROM
    (
      SELECT
        actor_user,
        rev_page,
        COUNT(ll_lang) AS iwlinks
      FROM revision_userindex
      JOIN actor_revision
        ON rev_actor = actor_id
      JOIN page
        ON rev_page = page_id
        AND page_namespace = 0
      JOIN langlinks
        ON ll_FROM = rev_page
      WHERE
        rev_parent_id = 0
        AND actor_user <> 0
      GROUP BY rev_page
    ) t
    GROUP BY
      actor_user,
      iwlinks
  ) t1
  JOIN
  (
    SELECT
      actor_user,
      iwlinks,
      COUNT(*) AS freq
    FROM
    (
      SELECT
        actor_user,
        rev_page,
        COUNT(ll_lang) AS iwlinks
      FROM revision_userindex
      JOIN actor_revision
        ON rev_actor = actor_id
      JOIN page
        ON rev_page = page_id
        AND page_namespace = 0
      JOIN langlinks
        ON ll_FROM = rev_page
      WHERE
        rev_parent_id = 0
        AND actor_user <> 0
      GROUP BY rev_page
    ) t
    GROUP BY
      actor_user,
      iwlinks
  ) t2
    ON t2.actor_user = t1.actor_user
    AND t2.iwlinks >= t1.iwlinks
  GROUP BY
    t1.actor_user,
    t1.iwlinks
) h
JOIN user
  ON actor_user = user_id
LEFT JOIN user_groups
  ON ug_user = actor_user
  AND ug_group = "bot"
WHERE
  total >= iwlinks
  AND iwlinks > 5
  AND ug_user IS NULL
GROUP BY actor_user
ORDER BY h_index DESC
""",
            "out": "وپ:گزارش دیتابیس/کاربران ویکی‌پدیا بر پایه شاخص اچ",
            "cols": ["ردیف", "کاربر", "شاخص اچ"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}"
            + "\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s|]] || {{formatnum:%s}} ",
            "sign": True,
        },
        {
            "sqlnum": 19,
            "sql": """
SELECT page_title
FROM page
JOIN (
  SELECT
    rev_page,
    COUNT(DISTINCT rev_actor) AS cnt
  FROM revision
  GROUP BY rev_page
  HAVING cnt = 1
) singleauth
  ON page_id = rev_page
LEFT JOIN linktarget
  ON lt_title = page_title
  AND lt_namespace = 4
LEFT JOIN pagelinks
  ON pl_target_id = lt_id
  AND pl_from <> 1171408 /* The report itself */
LEFT JOIN templatelinks
  ON tl_target_id = lt_id
WHERE
  page_namespace = 4
  AND page_is_redirect = 0
  AND page_title NOT LIKE "اشتباه‌یاب/موارد_درست/%"
  AND lt_title IS NULL
""",
            "out": "وپ:گزارش دیتابیس/صفحه‌های پروژه یتیم تک‌نویسنده",
            "cols": ["ردیف", "صفحه"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[{{ns:4}}:%s]]",
            "sign": True,
        },
        {
            "sqlnum": 20,
            "sql": """
SELECT
  actor_name,
  COUNT(DISTINCT page_id)
FROM page
JOIN revision_userindex
  ON rev_page = page_id
JOIN actor_revision
  ON rev_actor = actor_id
WHERE
  page_namespace = 0
  AND page_is_redirect = 0
  AND rev_actor NOT IN (
    SELECT actor_id
    FROM actor
    JOIN user_groups
      ON ug_user = actor_user
    WHERE ug_group = 'bot'
  )
GROUP BY actor_name
ORDER BY COUNT(DISTINCT page_id) DESC
LIMIT 500
""",
            "out": "وپ:گزارش دیتابیس/کاربران بر پایه تعداد مقالات ویرایش‌کرده",
            "cols": ["ردیف", "کاربر", "شمار مقاله‌ها"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[کاربر:%s]] || {{formatnum:%s}}",
            "sign": True,
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
            t["sign"],
            maxtime,
        )
        bot.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sqlnum = int(sys.argv[1])
        if len(sys.argv) > 2:
            maxtime = int(sys.argv[2])
        else:
            maxtime = None
    else:
        sqlnum = 0
        maxtime = None
    main(sqlnum, maxtime)
