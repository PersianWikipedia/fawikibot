#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
inactiveusers.py - a script to collect statistics about inactive users of the
wiki.

usage:

    python pwb.py inactiveusers

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
import toolforge


class InactiveUsersBot:
    def __init__(
        self,
        sql=None,
        out=None,
        cols=None,
        summary=None,
        pref=None,
        frmt=None,
        sign=True,
    ):
        if not (sql and out and cols and summary):
            raise ValueError("You must define sql, out, cols, and summary")
        self.sql = sql
        self.out = out
        self.cols = cols
        self.summary = summary
        self.pref = pref
        self.frmt = frmt
        self.sign = sign

    def run(self):
        site = pywikibot.Site()
        page = pywikibot.Page(site, self.out)
        sign = pywikibot.Page(site, self.out + "/امضا")
        text = "<!-- SQL = " + self.sql + " -->\n"
        text += self.pref + "\n"
        text += '{| class="wikitable sortable"\n'
        for col in self.cols:
            text += "!" + col + "\n"

        conn = toolforge.connect("fawiki")
        cursor = conn.cursor()
        self.sql = self.sql.encode(site.encoding())
        cursor.execute(self.sql)
        results = cursor.fetchall()
        print(len(results), " rows will be processed")

        for rowid in range(len(results)):
            row = results[rowid]
            text += "|-\n"
            row = list(row)
            for idx in range(len(row)):
                if isinstance(row[idx], bytes):
                    row[idx] = row[idx].decode()
                row[idx] = str(row[idx])
                row[idx] = row[idx].replace("rollbacker", "واگردان")
                row[idx] = row[idx].replace("patroller", "گشت‌زن")
                row[idx] = row[idx].replace("eliminator", "ویکی‌بان")
                row[idx] = row[idx].replace("sysop", "مدیر")
                row[idx] = row[idx].replace("bureaucrat", "دیوانسالار")
                row[idx] = row[idx].replace("Image-reviewer", "بازبین تصاویر")
                row[idx] = row[idx].replace("templateeditor", "ویرایشگر الگو")
                row[idx] = row[idx].replace("oversight", "پنهانگر")
                row[idx] = row[idx].replace(",", "، ")
            if self.frmt:
                row = tuple(row)
                if "%d" in self.frmt:
                    row = (rowid + 1,) + row
                text += self.frmt % row
                text += "\n"
            else:
                for item in row:
                    text += "| " + item + "\n"
        text += "|}"

        if not self.save(text, page, self.summary):
            pywikibot.output("Page %s not saved." % page.title(asLink=True))

        if self.sign:
            if not self.save("~~~~~", sign, self.summary):
                pywikibot.outout(
                    "Signature note saved in %s." % sign.title(asLink=True)
                )

    def save(self, text, page, comment=None, minorEdit=True, botflag=True):
        try:
            page.text = text
            # Save the page
            page.save(
                summary=comment or self.comment,
                minor=minorEdit,
                botflag=botflag,
            )
        except pywikibot.LockedPage:
            pywikibot.output(
                "Page %s is locked; skipping." % page.title(asLink=True)
            )
        except pywikibot.EditConflict:
            pywikibot.output(
                "Skipping %s because of edit conflict" % (page.title())
            )
        except pywikibot.SpamfilterError as error:
            pywikibot.output(
                "Cannot change %s due to spam blacklist entry %s"
                % (page.title(), error.url)
            )
        else:
            return True


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    sql = """
SELECT
  actor_name,
  STR_TO_DATE(LEFT(MAX(rev_timestamp), 8), '%Y%m%d') AS latest,
  group_concat(distinct ug.ug_group)
FROM revision
JOIN actor
  ON rev_actor = actor_id
  AND actor_user <> 0
JOIN user_groups AS ug
  ON ug_user = actor_user
LEFT JOIN user_groups AS ug2
  ON ug2.ug_user = actor_user
  AND ug2.ug_group = 'bot'
WHERE
  ug2.ug_group IS NULL
  AND ug.ug_group IN (
    'rollbacker',
    'patroller',
    'eliminator',
    'sysop',
    'bureaucrat',
    'Image-reviewer',
    'templateeditor',
    'oversight'
  )
GROUP BY actor_name
HAVING latest < DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 6 MONTH),'%Y%m%d%H%i%s')
"""
    out = "وپ:گزارش دیتابیس/کاربران غیر فعال در گروه‌های کاربری"
    cols = ["ردیف", "کاربر", "آخرین ویرایش", "گروه‌ها"]
    summary = "به روز کردن آمار"
    pref = "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\nآخرین به روز رسانی: ~~~~~\n\n"
    frmt = (
        "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
        + "|| {{formatnum:%s|NOSEP}} || %s"
    )
    bot = InactiveUsersBot(sql, out, cols, summary, pref, frmt, True)
    bot.run()


if __name__ == "__main__":
    main()
