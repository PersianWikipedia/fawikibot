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
        text = self.pref + "\n"
        text += '{| class="wikitable sortable"\n'
        for col in self.cols:
            text += "!" + col + "\n"

        conn = toolforge.connect("fawiki")
        cursor = conn.cursor()

        users = self.get_users()
        print(len(users), "rows will be processed")

        counter = 1

        for user in users:
            print("Retreiving data for user #%d" % counter)
            sql = self.sql % user
            sql = sql.encode(site.encoding())
            cursor.execute(sql)
            results = cursor.fetchall()

            for rowid in range(len(results)):
                row = results[rowid]
                row = list(row)
                row[0] = row[0].decode("utf-8")
                row = tuple(row)

                text += "|-\n"
                if "%d" in self.frmt:
                    row = (rowid + 1,) + row
                text += self.frmt % row
                text += "\n"

            counter += 1

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

    def get_users(self):
        sql = """
SELECT actor_id
FROM revision_userindex
JOIN actor_revision
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
        374638, -- پیام به کاربر جدید
        285515  -- FawikiPatroller
    )
    AND ug_user IS NULL
GROUP BY actor_id
ORDER BY COUNT(rev_id) DESC
LIMIT 1000
"""
        conn = toolforge.connect("fawiki")
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


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
  FROM revision_userindex
  JOIN actor_revision
    ON actor_id = rev_actor
  JOIN page
    ON rev_page = page_id
  WHERE actor_id = %s
  GROUP BY
    page_namespace
) AS edits
GROUP BY actor_name
"""

    out = "وپ:گزارش دیتابیس/کاربران فعال در یک ماه اخیر"
    cols = ["ردیف", "کاربر", "تعداد کل ویرایش‌ها", "ویرایش در مقاله‌ها",
            "ویرایش‌های فنی", "بحث‌های پروژه", "سایر بحث‌ها",
            "سایر ویرایش‌ها"]
    summary = "به روز کردن آمار"
    pref = "[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n{{/بالا}}"
    + "\n\nآخرین به روز رسانی: ~~~~~",
    frmt = (
        "| {{formatnum:%d|NOSEP}} || [[کاربر:%s]] "
        + "|| {{formatnum:%s}} || ٪{{formatnum:%s}} || ٪{{formatnum:%s}} "
        + "|| ٪{{formatnum:%s}} || ٪{{formatnum:%s}} || ٪{{formatnum:%s}}"
    )
    bot = InactiveUsersBot(sql, out, cols, summary, pref, frmt, True)
    bot.run()


if __name__ == "__main__":
    main()
