#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
nightly.py - a wrapper for stats.py to be called every night.
usage:
    python pwb.py nightly <sqlnum> <maxtime>
    or
    python pwb.py nightly <sqlnum>
    or
    python pwb.py nightly
parameters:
    <sqlnum>: (optinal) integer Used to run specifice queries
    <maxtime>: (optional) maximum execution time for the specified query
"""
#
# (C) w:fa:User:Huji, 2015-2021
#


import sys
import stats


def main(sqlnum, maxtime):
    tasks = [
        {
            "sqlnum": 1,
            "sql": """
SELECT
  actor_name,
  user_editcount,
  GROUP_CONCAT(rc_title ORDER BY edits DESC SEPARATOR ' {{*}} ')
FROM
(
  SELECT
    actor_name,
    user_editcount,
    CONCAT('[[', REPLACE(rc_title, '_', ' '), ']]') AS rc_title
  FROM recentchanges_userindex
  JOIN actor
    ON actor_id = rc_actor
  JOIN user
    ON actor_user = user_id
  WJERE
    user_editcount > 0
    AND user_editcount < 100
    AND rc_namespace = 0
    AND rc_timestamp >
      DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 2 DAY), '%Y%m%d000000')
    AND rc_source = 'mw.edit'
  GROUP BY
    actor_name,
    user_editcount,
    rc_title
) AS newbies
GROUP BY
  actor_name,
  user_editcount
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های هدف کاربران تازه‌کار",
            "cols": [
              "کاربر",
              "شمار ویرایش‌ها",
              "مقاله‌ها"
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}" +
                    "\n\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| [[کاربر:%s|]] || {{formatnum:%s|NOSEP}} || %s",
            "sign": True
        },
        {
            "sqlnum": 2,
            "sql": """
SELECT
  rc_title,
  GROUP_CONCAT(actor_name ORDER BY edits DESC SEPARATOR ' {{*}} ')
FROM
(
  SELECT
    CONCAT('[[کاربر:', actor_name, ']]') as actor_name,
    CONCAT('[[', rc_title, ']]') as rc_title
  FROM recentchanges_userindex
  JOIN actor
    ON actor_id = rc_actor
  JOIN user
    ON actor_user = user_id
  WHERE
    user_editcount > 0
    AND user_editcount < 100
    AND rc_namespace = 0
    AND rc_timestamp >
      DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 2 DAY), '%Y%m%d000000')
    AND rc_source = 'mw.edit'
  GROUP BY
    actor_name,
    rc_title
) AS newbies
GROUP BY rc_title
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC
""",
            "out": "وپ:گزارش دیتابیس/مقاله‌های هدف چند کاربر تازه‌کار",
            "cols": [
              "مقاله",
              "کاربران"
            ],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]" +
                    "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| %s || %s",
            "sign": True
        }
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
            maxtime)
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
