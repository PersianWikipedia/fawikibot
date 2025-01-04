#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
weekly-en.py - a wrapper for stats.py to be called every week.
usage:
    python pwb.py weekly-en <sqlnum> <maxtime>
    or
    python pwb.py weekly-en <sqlnum>
    or
    python pwb.py weekly-en
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
  COUNT(ll.ll_lang) AS interwiki_count,
  COALESCE(pp.pp_value, '&mdash;') AS description
FROM page p
JOIN langlinks ll
  ON p.page_id = ll.ll_from
LEFT JOIN page_props pp
  ON p.page_id = pp.pp_page
  AND pp.pp_propname = 'wikibase-shortdesc'
LEFT JOIN langlinks ll2
  ON p.page_id = ll2.ll_from
  AND ll2.ll_lang = 'fa'
WHERE
  p.page_namespace = 0
  AND p.page_is_redirect = 0
  AND ll2.ll_lang IS NULL
GROUP BY
  p.page_title,
  pp.pp_value
HAVING COUNT(ll.ll_lang) > 10
ORDER BY interwiki_count DESC
LIMIT 100
""",
            "out": "ویکی‌پدیا:گزارش دیتابیس/"
            + "مقاله‌های مهم ایجادنشده بر پایه دیگر میان‌ویکی‌ها",
            "cols": ["ردیف", "مقاله", "شمار میان‌ویکی‌ها", "توضیحات"],
            "summary": "به روز کردن آمار",
            "pref": "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}"
            + "\nآخرین به روز رسانی: ~~~~~",
            "frmt": "| {{formatnum:%d}} || [[:en:%s]] || {{formatnum:%s}}"
            + " |dir=ltr| %s",
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
            "enwiki",
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
