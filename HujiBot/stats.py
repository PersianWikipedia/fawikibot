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
import MySQLdb as mysqldb
import time

page_namespace = {
    u'0': u'',
    u'1': u'بحث:',
    u'2': u'کاربر:',
    u'3': u'بحث کاربر:',
    u'4': u'ویکی‌پدیا:',
    u'5': u'بحث ویکی‌پدیا:',
    u'6': u':پرونده:',
    u'7': u'بحث پرونده:',
    u'8': u'مدیاویکی:',
    u'9': u'بحث مدیاویکی:',
    u'10': u'الگو:',
    u'11': u'بحث الگو:',
    u'12': u'راهنما:',
    u'13': u'بحث راهنما:',
    u'14': u':رده:',
    u'15': u'بحث رده:',
    u'100': u'درگاه:',
    u'101': u'بحث درگاه:',
    u'102': u'کتاب:',
    u'103': u'بحث کتاب:',
    u'118': u'پیش‌نویس:',
    u'119': u'بحث پیش‌نویس:',
    u'828': u'پودمان:',
    u'829': u'بحث پودمان:'
}
user_groups = {
    u'uploader': u'بارگذار',
    u'transwiki': u'درون ریز بین‌ویکی‌ها',
    u'templateeditor': u'ویرایشگر الگو',
    u'sysop': u'مدیر',
    u'rollbacker': u'واگردان',
    u'registered': u'ثبت‌نام‌کرده',
    u'patroller': u'گشت‌زن',
    u'oversight': u'پنهانگر',
    u'OTRS-member': u'عضو OTRS',
    u'ipblock-exempt': u'استثنای قطع دسترسی',
    u'interface-admin': u'مدیر رابط کاربری',
    u'import': u'درون‌ریز',
    u'Image-reviewer': u'بازبین تصویر',
    u'extendedconfirmed': u'تأییدشده پایدار',
    u'eponline': u'داوطلب دورهٔ برخط',
    u'epinstructor': u'استاد دوره',
    u'epcoordinator': u'هماهنگ‌کنندهٔ دوره',
    u'epcampus': u'داوطلب دورهٔ پردیس',
    u'eliminator': u'ویکی‌بان',
    u'confirmed': u'کاربر تائیدشده',
    u'checkuser': u'بازرس کاربر',
    u'bureaucrat': u'دیوانسالار',
    u'botadmin': u'مدیر رباتیک',
    u'autoreviewer': u'بازبینی‌خودکار',
    u'autopatrolled': u'گشت خودکار',
    u'accountcreator': u'سازنده حساب',
    u'abusefilter': u'تنظیم‌کنندهٔ پالایهٔ خرابکاری'
}


class StatsBot:

    def __init__(self, sql=None, out=None, cols=None, summary=None, pref=None,
                 frmt=None, sqlnum=None, sign=True, maxtime=None):
        if not (sql and out and cols and summary):
            raise ValueError('You must define sql, out, cols, and summary')
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
        pywikibot.output("Start time: %s" %
                         time.asctime(time.gmtime(bot_start)))

        site = pywikibot.Site()
        page = pywikibot.Page(site, self.out)
        sign = pywikibot.Page(site, self.out + u'/امضا')
        text = u'<!-- SQL = ' + self.sql + u' -->\n'
        text += self.pref + u'\n'
        text += u'{| class="wikitable sortable"\n'
        for col in self.cols:
            text += u'!' + col + u'\n'
        query_start = time.time()
        conn = mysqldb.connect(
            host="fawiki.web.db.svc.wikimedia.cloud",
            db="fawiki_p",
            read_default_file="~/replica.my.cnf",
            charset="utf8"
        )
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
        timer = '<!-- Query time: %d seconds -->\n' % delta
        text = timer + text
        text = u'<!-- SQL Number = ' + str(self.sqlnum) + u' -->\n' + text
        print(len(results), ' rows will be processed')

        for rowid in range(len(results)):
            row = results[rowid]
            text += u'|-\n'
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
                if '%d' in self.frmt:
                    row = (rowid + 1,) + row
                text += self.frmt % row
                text += u'\n'
            else:
                for item in row:
                    text += u'| ' + item + u'\n'
        text += u'|}'
        # Convert Namespace number to their names
        for ns in page_namespace:
            text = text.replace(
                u'[[' + ns + u':',
                u'[[' + page_namespace[ns]
            )
        for user_grp in user_groups:
            text = text.replace(
                u' ' + user_grp,
                u' ' + user_groups[user_grp]
            )
        text = text.replace(
            u'||  ،',
            u'|| '
        ).replace(
            u'،   ||',
            u' ||'
        ).replace(
            u'، ،',
            u'،'
        )
        if not self.save(text, page, self.summary):
            pywikibot.output(u'Page %s not saved.' % page.title(asLink=True))

        if self.sign:
            if not self.save('~~~~~', sign, self.summary):
                pywikibot.outout(u'Signature note saved in %s.' %
                                 sign.title(asLink=True))
        bot_end = time.time()
        delta = int(bot_end - bot_start)
        print("Total time: %d seconds" % delta)
        pywikibot.output("Total time: %d seconds" % delta)
        pywikibot.output("End time: %s" % time.asctime(time.gmtime(bot_end)))
        print("Stats bot out ...")

    def save(self, text, page, comment=None, minorEdit=True,
             botflag=True):
        try:
            page.text = text
            # Save the page
            page.save(summary=comment or self.summary,
                      minor=minorEdit, botflag=botflag)
        except pywikibot.LockedPageError:
            pywikibot.output(u"Page %s is locked; skipping."
                             % page.title(asLink=True))
        except pywikibot.EditConflictError:
            pywikibot.output(
                u'Skipping %s because of edit conflict'
                % (page.title()))
        except pywikibot.SpamblacklistError as error:
            pywikibot.output(
                u'Cannot change %s due to spam blacklist entry %s'
                % (page.title(), error.url))
        except pywikibot.OtherPageSaveError as error:
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
    pref = 'آخرین به روز رسانی: ~~~~~\n\n'
    frmt = None
    sqlnum = 0
    maxtime = None
    for arg in local_args:
        if arg.startswith('-sql:'):
            sql = arg[len('-sql:'):]
        elif arg.startswith('-out:'):
            out = arg[len('-out:'):]
        elif arg.startswith('-cols:'):
            cols = arg[len('-cols:'):].split(',')
        elif arg.startswith('-summary:'):
            summary = arg[len('-summary:'):]
        elif arg.startswith('-pref:'):
            pref = arg[len('-pref:'):] + '\n\n' + pref
        elif arg.startswith('-frmt:'):
            frmt = arg[len('-frmt:'):]
        elif arg.startswith('-sign:'):
            sign = False
        elif arg.startswith('-maxtime:'):
            maxtime = int(arg[len('-maxtime:')])
    bot = StatsBot(sql, out, cols, summary, pref, frmt, sqlnum, sign, maxtime)
    bot.run()


if __name__ == "__main__":
    main()
