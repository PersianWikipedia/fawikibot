#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################
# Copyright (C) 2018 Z        (User:ZxxZxxZ)
#                    Reza1615 (User:Reza1615)
#                    Huji     (User:Huji)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#############################################
 
from __future__ import absolute_import, unicode_literals
 
import re
import time
import webcitation
import pywikibot

from pywikibot import pagegenerators
from pywikibot.bot import (
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)
from datetime import (
    timedelta, datetime)

class WebCiteBot(
    SingleSiteBot,
    ExistingPageBot,
    NoRedirectPageBot
):

    deadlink = []

    def __init__(self, generator, **kwargs):
        # Edit summary
        self.availableOptions.update({
            'summary': u'ربات: [[وپ:پایدار|بایگانی منابع برخط]]',
        })

        # Call constructor of the super class
        super(WebCiteBot, self).__init__(site=True, **kwargs)

       # Assign the generator to the bot
        self.generator = generator

        # Save edits without asking
        self.options['always'] = True

        # Global counter for all archived links
        self.counter = 0

        # Maximum number of links that can be archived each day
        self.availableOptions.update({
            'maxlinks': 99,
        })

    def persianDigits(self, s):
        return str(s).replace(u'0',u'۰') \
            .replace(u'1',u'۱') \
            .replace(u'2',u'۲') \
            .replace(u'3',u'۳') \
            .replace(u'4',u'۴') \
            .replace(u'5',u'۵') \
            .replace(u'6',u'۶') \
            .replace(u'7',u'۷') \
            .replace(u'8',u'۸') \
            .replace(u'9',u'۹')

    def persianDate(self):
        monthNames = [
            u"ژانویه",
            u"فوریه",
            u"مارس",
            u"آوریل",
            u"مه",
            u"ژوئن",
            u"ژوئیه",
            u"اوت",
            u"سپتامبر",
            u"اکتبر",
            u"نوامبر",
            u"دسامبر"
            ]

        today = datetime.today()
        y = today.year
        m = monthNames[today.month - 1]
        d = today.day

        d = self.persianDigits(d)
        y = self.persianDigits(y)

        return '%s %s %s' % (d, m, y)

    def archive(self, URL):
        pywikibot.output("Requesting URL %s" % URL)
        try:
            archiveURL = webcitation.capture(URL)
        except:
            pywikibot.output(u"\03{red}Archive attempt failed!\03{default}")
            return False
        pywikibot.output(u"\03{lightgreen}Successfully archived at %s\03{default}" % archiveURL)
        self.counter += 1
        return archiveURL

    def treat_page(self):
        if (self.current_page.namespace() != 0):
            pywikibot.output("Not an article; skipped...")
            return True
        
        text = self.current_page.text

        # Persian Citations
        persianDate = self.persianDate()
        faCitationPattern = u'\{\{\s*یادکرد(?:\{\{.*?\}\}|.)*?\}\}'
        faArchivePattern = u'\| *(پیوند بایگانی|نشانی بایگانی) *= *[^ |}]'
        faBlankArchivePattern = u'\| *(پیوند بایگانی|نشانی بایگانی|تاریخ بایگانی) *= *(?=[|}])'
        faUrlPattern = u'\| *(نشانی|پیوند) *= *([^|]+) *\|'
        faCitations = re.findall(faCitationPattern, text, re.S)
        if not faCitations:
            pywikibot.output(u"\03{lightpurple}No Persian citations!\03{default}")
        else:
            for citation in faCitations:
                if not re.findall(faArchivePattern, citation, re.S):
                    # Not archived already
                    url = re.findall(faUrlPattern, citation, re.S)
                    if url and url[0][1].strip() != "":
                        # Try archiving it
                        if self.counter + 1 > self.getOption('maxlinks'):
                            pywikibot.output(u"\03{red}WebCitation quota is used up!\03{default}")
                            continue
                        
                        arc = self.archive(url[0][1])
                        if not arc:
                            # Archiving failed
                            continue
                        # Remove any blank archiveurl parameters
                        newCitation = re.sub(faBlankArchivePattern, "", citation)
                        # Add archiveurl and archivedate
                        newParams = "| پیوند بایگانی = %s | تاریخ بایگانی = %s }}" % (arc, persianDate)
                        newCitation = re.sub("}}$", newParams, newCitation)
                        text = text.replace(citation, newCitation)

        # English Citations
        englishDate = datetime.today().strftime("%-d %B %Y")
        enCitationPattern = u'\{\{\s*cite(?:\{\{.*?\}\}|.)*?\}\}'
        enArchivePattern = u'\| *(archiveurl|archive-url) *= *[^ |}]'
        enBlankArchivePattern = u'\| *(archiveurl|archive-url|archivedate|archive-date) *= *(?=[|}])'
        enUrlPattern = u'\| *(url) *= *([^|]+) *\|'
        enCitations = re.findall(enCitationPattern, text, re.S)
        if not enCitations:
            pywikibot.output(u"\03{lightpurple}No English citations!\03{default}")
        else:
            for citation in enCitations:
                if not re.findall(enArchivePattern, citation, re.S):
                    # Not archived already
                    url = re.findall(enUrlPattern, citation, re.S)
                    if url and url[0][1].strip() != "":
                        # Try archiving it
                        if self.counter + 1 > self.getOption('maxlinks'):
                            pywikibot.output(u"\03{red}WebCitation quota is used up!\03{default}")
                            continue
                        
                        arc = self.archive(url[0][1])
                        if not arc:
                            # Archiving failed
                            continue
                        # Remove any blank archiveurl parameters
                        newCitation = re.sub(enBlankArchivePattern, "", citation)
                        # Add archiveurl and archivedate
                        newParams = "| archive-url = %s | archive-date = %s }}" % (arc, englishDate)
                        newCitation = re.sub("}}$", newParams, newCitation)
                        text = text.replace(citation, newCitation)

        self.put_current(text, summary=self.getOption('summary'))

def main(*args):
    options = {}
    local_args = pywikibot.handle_args(args)
    genFactory = pagegenerators.GeneratorFactory()

    for arg in local_args:
        # Catch the pagegenerators options
        if genFactory.handleArg(arg):
            continue  # nothing to do here
        # Take the remaining options as booleans.
        else:
            pywikibot.output('Unknown argument(s)!')

    gen = genFactory.getCombinedGenerator()
    if gen:
        gen = pagegenerators.PreloadingGenerator(gen)
        bot = WebCiteBot(gen, **options)
        bot.run()
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False
 
if __name__ == "__main__":
    main()

