#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot cleans up old sandbox user pages
"""
#
# (C) User:Huji, 2019
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

#

import pywikibot
import toolforge
from pywikibot import pagegenerators

from pywikibot.bot import (
    SingleSiteBot,
    ExistingPageBot,
    NoRedirectPageBot,
    AutomaticTWSummaryBot,
)

docuReplacements = {"&params;": pagegenerators.parameterHelp}

SUMMARY = "([[ویکی‌پدیا:سیاست ربات‌رانی/درخواست مجوز/HujiBot/وظیفه ۲۰|و ۲۰]])"
NEWTEXT = "{{صفحه کاربری غیرفعال خالی شده}}"


class HujiBot(
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot
):
    def __init__(self, generator, **kwargs):
        super(HujiBot, self).__init__(site=True, **kwargs)
        self.generator = generator
        self.summary = SUMMARY

    def treat_page(self):
        self.put_current(NEWTEXT, summary=self.summary)


def main(*args):
    options = {}
    local_args = pywikibot.handle_args(args)

    genFactory = pagegenerators.GeneratorFactory()

    for arg in local_args:
        if genFactory.handleArg(arg):
            continue  # nothing to do here
        arg, sep, value = arg.partition(":")
        option = arg[1:]
        if option in ("summary", "text"):
            if not value:
                pywikibot.input("Please enter a value for " + arg)
            options[option] = value
        elif option in ("method"):
            if not value:
                options[option] = "all"
            else:
                options[option] = value
        else:
            options[option] = True

    gen = genFactory.getCombinedGenerator()
    if gen:
        gen = pagegenerators.PreloadingGenerator(gen)
        bot = HujiBot(gen, **options)
        bot.run()
        return True
    else:
        conn = toolforge.connect("fawiki")
        cursor = conn.cursor()
        sql = """
SELECT DISTINCT
  concat('کاربر:', page_title) AS title
FROM page
JOIN revision
  ON rev_page = page_id
  AND rev_id = page_latest
JOIN categorylinks
  ON page_id = cl_from
WHERE
  page_namespace = 2
  AND page_title like '%/صفحه_تمرین'
  AND rev_timestamp < DATE_FORMAT(
    DATE_SUB(NOW(), INTERVAL 1 YEAR),
    '%Y%m%d000000'
  )
ORDER BY rev_timestamp
"""
        cursor.execute(sql.encode("utf-8"))
        results = cursor.fetchall()
        print(len(results), " rows will be processed")

        for rowid in range(len(results)):
            row = results[rowid]
            title = row[0]
            page = pywikibot.Page(pywikibot.Site(), title.decode("utf-8"))
            page.put(NEWTEXT, SUMMARY)

        return True


if __name__ == "__main__":
    main()
