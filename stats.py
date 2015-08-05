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

This bot always stores the SQL query in an HTML comment (<!-- ... -->) at the
top of the page to allow reproducibility of the results by others.
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
import re
import MySQLdb as mysqldb


class StatsBot:

    def __init__(self, sql=None, out=None, cols=None, summary=None, pref=None,
                 frmt=None, sign=True):
        if not (sql and out and cols and summary):
            raise ValueError('You must define sql, out, cols, and summary')
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
        sign = pywikibot.Page(site, self.out + u'/امضا')
        text = u'<!-- SQL = ' + self.sql + u' -->\n'
        text += self.pref + u'\n'
        text += u'{| class="wikitable sortable"\n'
        for col in self.cols:
            text += u'!' + col + u'\n'

        conn = mysqldb.connect("fawiki.labsdb", db="fawiki_p",
                               read_default_file="~/replica.my.cnf")
        cursor = conn.cursor()
        self.sql = self.sql.encode(site.encoding())
        cursor.execute(self.sql)
        results = cursor.fetchall()
        print len(results), ' rows will be processed'

        for rowid in range(len(results)):
            row = results[rowid]
            text += u'|-\n'
            row = list(row)
            for idx in range(len(row)):
                row[idx] = str(row[idx]).decode('utf-8')
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

        if not self.save(text, page, self.summary):
            pywikibot.output(u'Page %s not saved.' % page.title(asLink=True))

        if self.sign:
            if not self.save('~~~~~', sign, self.summary):
                pywikibot.outout(u'Signature note saved in %s.' %
                    sign.title(asLink=True))

    def save(self, text, page, comment=None, minorEdit=True,
             botflag=True):
        try:
            page.text = text
            # Save the page
            page.save(summary=comment or self.comment,
                      minor=minorEdit, botflag=botflag)
        except pywikibot.LockedPage:
            pywikibot.output(u"Page %s is locked; skipping."
                             % page.title(asLink=True))
        except pywikibot.EditConflict:
            pywikibot.output(
                u'Skipping %s because of edit conflict'
                % (page.title()))
        except pywikibot.SpamfilterError as error:
            pywikibot.output(
                u'Cannot change %s due to spam blacklist entry %s'
                % (page.title(), error.url))
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
    bot = StatsBot(sql, out, cols, summary, pref, frmt, sign)
    bot.run()

if __name__ == "__main__":
    main()

