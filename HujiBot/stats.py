#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
stats.py - a script to collect statistics about the wiki.

usage:

    python pwb.py stats [OPTIONS]

List of parameters

  -sql      The SQL query that will be executed to get the statsistics. These
            statistics will then be saved on wiki as a table.
  -out      Name of the page on the wiki in which the results are saved. The
            bot will edit that page (or throw an error if unable to edit).
  -cols     Human-understandable column headers for the results table. This
            parameter must be a string in comma-separated format (using "," as
            separator). The first row of output table (the headers) will be
            generated using the items in this comma-separated list.
  -summary  This specifies the edit summary that the bot will use when editing
            the page.
  -pref     This optional parameter allows the user to add some preface before
            the result table. For instance, using -pref:'{{/up}}' will include
            the /up at the beginning of the page (which can then be editted to
            add explanations about the query results.
  -frmt     This optional parameter specifies the format of the output (rows of
            the table). If this is not specified, then a simple table will be
            generated where each row of the query result will be shown as a row
            in the table; in this case, the only parsing that is done is by
            localizing the numeric cells. If this parameter is specified, then
            it will be used as a formatting string in the standard way that
            python handles string formatting (i.e. %s will be replaced with a
            given string and so on).
  -maxtime  Maximum execution time of SQL queries (in minutes). Default is 30.

This bot always stores the SQL query in an HTML comment (<!-- ... -->) at the
top of the page to allow reproducibility of the results by others.
"""
#
# (C) Pywikibot team, 2006-2014
# (C) w:fa:User:Huji, 2015
#
# Distributed under the terms of the MIT license.
#

import pywikibot
from pywikibot import exceptions
import toolforge
import time

page_namespace = {
    "0": "",
    "1": "بحث:",
    "2": "کاربر:",
    "3": "بحث کاربر:",
    "4": "ویکی‌پدیا:",
    "5": "بحث ویکی‌پدیا:",
    "6": ":پرونده:",
    "7": "بحث پرونده:",
    "8": "مدیاویکی:",
    "9": "بحث مدیاویکی:",
    "10": "الگو:",
    "11": "بحث الگو:",
    "12": "راهنما:",
    "13": "بحث راهنما:",
    "14": ":رده:",
    "15": "بحث رده:",
    "100": "درگاه:",
    "101": "بحث درگاه:",
    "102": "کتاب:",
    "103": "بحث کتاب:",
    "118": "پیش‌نویس:",
    "119": "بحث پیش‌نویس:",
    "828": "پودمان:",
    "829": "بحث پودمان:",
}
user_groups = {
    "uploader": "بارگذار",
    "transwiki": "درون ریز بین‌ویکی‌ها",
    "templateeditor": "ویرایشگر الگو",
    "sysop": "مدیر",
    "rollbacker": "واگردان",
    "registered": "ثبت‌نام‌کرده",
    "patroller": "گشت‌زن",
    "oversight": "پنهانگر",
    "OTRS-member": "عضو OTRS",
    "ipblock-exempt": "استثنای قطع دسترسی",
    "interface-admin": "مدیر رابط کاربری",
    "import": "درون‌ریز",
    "Image-reviewer": "بازبین تصویر",
    "extendedconfirmed": "تأییدشده پایدار",
    "eponline": "داوطلب دورهٔ برخط",
    "epinstructor": "استاد دوره",
    "epcoordinator": "هماهنگ‌کنندهٔ دوره",
    "epcampus": "داوطلب دورهٔ پردیس",
    "eliminator": "ویکی‌بان",
    "confirmed": "کاربر تائیدشده",
    "checkuser": "بازرس کاربر",
    "bureaucrat": "دیوانسالار",
    "botadmin": "مدیر رباتیک",
    "autoreviewer": "بازبینی‌خودکار",
    "autopatrolled": "گشت خودکار",
    "accountcreator": "سازنده حساب",
    "abusefilter": "تنظیم‌کنندهٔ پالایهٔ خرابکاری",
}


class StatsBot:
    def __init__(
        self,
        sql=None,
        out=None,
        cols=None,
        summary=None,
        pref=None,
        frmt=None,
        sqlnum=None,
        sign=True,
        maxtime=None,
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
        self.sqlnum = sqlnum
        self.maxtime = 30 if maxtime is None else maxtime

    def run(self):
        print("Stats bot started ...")
        print("Process number: %s" % self.sqlnum)
        pywikibot.output("Process number: %s" % self.sqlnum)
        bot_start = time.time()
        pywikibot.output(
            "Start time: %s" % time.asctime(time.gmtime(bot_start))
        )

        site = pywikibot.Site()
        page = pywikibot.Page(site, self.out)
        sign = pywikibot.Page(site, self.out + "/امضا")
        text = "<!-- SQL = " + self.sql + " -->\n"
        text += self.pref + "\n"
        text += '{| class="wikitable sortable"\n'
        for col in self.cols:
            text += "!" + col + "\n"
        query_start = time.time()
        conn = toolforge.connect("fawiki", charset="utf8")
        cursor = conn.cursor()
        max_time = "SET SESSION MAX_STATEMENT_TIME = 60 * %d;" % (self.maxtime)
        cursor.execute(max_time)
        max_len = "SET SESSION GROUP_CONCAT_MAX_LEN = 15000;"
        cursor.execute(max_len)
        try:
            cursor.execute(self.sql)
        except Exception:
            print("Query took too long therefore StatBot was stopped!")
            return
        results = cursor.fetchall()
        query_end = time.time()
        delta = int(query_end - query_start)
        print("Query time: %d seconds" % delta)
        timer = "<!-- Query time: %d seconds -->\n" % delta
        text = timer + text
        text = "<!-- SQL Number = " + str(self.sqlnum) + " -->\n" + text
        print(len(results), " rows will be processed")

        for rowid in range(len(results)):
            row = results[rowid]
            text += "|-\n"
            row = list(row)
            for idx in range(len(row)):
                if isinstance(row[idx], bytes):
                    try:
                        row[idx] = row[idx].decode()
                    except Exception:
                        try:
                            row[idx] = row[idx].decode()[:-1]
                        except Exception:
                            row[idx] = row[idx].decode()[:-2]

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
        # Convert Namespace number to their names
        for ns in page_namespace:
            text = text.replace("[[" + ns + ":", "[[" + page_namespace[ns])
        for user_grp in user_groups:
            text = text.replace(" " + user_grp, " " + user_groups[user_grp])
        text = (
            text.replace("||  ،", "|| ")
            .replace("،   ||", " ||")
            .replace("، ،", "،")
        )
        if not self.save(text, page, self.summary):
            pywikibot.output("Page %s not saved." % page.title())

        if self.sign:
            if not self.save("~~~~~", sign, self.summary):
                pywikibot.outout("Signature note saved in %s." % sign.title())
        bot_end = time.time()
        delta = int(bot_end - bot_start)
        print("Total time: %d seconds" % delta)
        pywikibot.output("Total time: %d seconds" % delta)
        pywikibot.output("End time: %s" % time.asctime(time.gmtime(bot_end)))
        print("Stats bot out ...")

    def save(self, text, page, comment=None, minorEdit=True, botflag=True):
        try:
            page.text = text
            # Save the page
            page.save(
                summary=comment or self.summary,
                minor=minorEdit,
                botflag=botflag,
            )
        except exceptions.LockedPageError:
            pywikibot.output("Page %s is locked; skipping." % page.title())
        except exceptions.EditConflictError:
            pywikibot.output(
                "Skipping %s because of edit conflict" % (page.title())
            )
        except exceptions.SpamblacklistError as error:
            pywikibot.output(
                "Cannot change %s due to spam blacklist entry %s"
                % (page.title(), error.url)
            )
        except exceptions.OtherPageSaveError as error:
            pywikibot.output("Page save error")
            pywikibot.output(error)
        else:
            return True


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    local_args = pywikibot.handle_args(args)
    sql = None
    out = None
    cols = None
    summary = None
    pref = "آخرین به روز رسانی: ~~~~~\n\n"
    frmt = None
    sqlnum = 0
    maxtime = None
    for arg in local_args:
        if arg.startswith("-sql:"):
            sql = arg[len("-sql:") :]
        elif arg.startswith("-out:"):
            out = arg[len("-out:") :]
        elif arg.startswith("-cols:"):
            cols = arg[len("-cols:") :].split(",")
        elif arg.startswith("-summary:"):
            summary = arg[len("-summary:") :]
        elif arg.startswith("-pref:"):
            pref = arg[len("-pref:") :] + "\n\n" + pref
        elif arg.startswith("-frmt:"):
            frmt = arg[len("-frmt:") :]
        elif arg.startswith("-sign:"):
            sign = False
        elif arg.startswith("-maxtime:"):
            maxtime = int(arg[len("-maxtime:")])
    bot = StatsBot(sql, out, cols, summary, pref, frmt, sqlnum, sign, maxtime)
    bot.run()


if __name__ == "__main__":
    main()
