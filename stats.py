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
from pywikibot import config, textlib
import MySQLdb as mysqldb


class StatsBot:

    def __init__(self, sql=None, out=None, cols=None, summary=None, pref=None):
        if not (sql and out and cols and summary):
            raise ValueError('You must define sql, out, cols, and summary')
        self.sql = sql
        self.out = out
        self.cols = cols
        self.summary = summary
        self.pref = pref

    def run(self):
        site = pywikibot.Site()
        page = pywikibot.Page(site, self.out)
        text = u'<!-- SQL = ' + self.sql + ' -->\n'
        text += self.pref
        text += u'{| class="wikitable sortable"\n'
        for col in self.cols.split(','):
            text += u'!' + col + u'\n'

        conn = mysqldb.connect("fawiki.labsdb", db="fawiki_p",
                               read_default_file="~/replica.my.cnf")
        cursor = conn.cursor()
        self.sql = self.sql.encode(site.encoding())
        cursor.execute(self.sql)
        results = cursor.fetchall()
        for row in results:
            text += u'|-\n'
            for item in row:
                if isinstance(item, int) or isinstance(item, long):
                    item = textlib.to_local_digits(str(item), 'fa')
                else:
                    item = str(item)
                text += u'| ' + item.decode('utf-8') + u'\n'
        text += u'|}'

        if not self.save(text, page, self.summary):
            pywikibot.output(u'Page %s not saved.' % page.title(asLink=True))

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
    for arg in local_args:
        if arg.startswith('-sql:'):
            sql = arg[len("-sql:"):]
        elif arg.startswith('-out:'):
            out = arg[len("-out:"):]
        elif arg.startswith('-cols:'):
            cols = arg[len("-cols:"):]
        elif arg.startswith("-summary:"):
            summary = arg[len("-summary:"):]
        elif arg.startswith("-pref:"):
            pref = arg[len("-pref:"):] + '\n\n' + pref
    bot = StatsBot(sql, out, cols, summary, pref)
    bot.run()

if __name__ == "__main__":
    main()

