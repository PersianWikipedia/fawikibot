#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ISBN fixer bot!

This bot finds all uses of the ISBN magic link, and replaces it with the
{{ISBN}} template. It also checks to see if the link appears in a latin or
Persian citation, and accordingly assigns parameters to the {{ISBN}} template
so that it properly shows in LTR/RTL.
"""
#
# (C) Pywikibot team, 2006-2016
# (C) Huji, 2016
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

#

import pywikibot
import re
import string
from pywikibot import pagegenerators

from pywikibot.bot import (
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)
from pywikibot.tools import issue_deprecation_warning

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}


class ISBNBot(
    # Refer pywikobot.bot for generic bot classes
    SingleSiteBot,  # A bot only working on one site
    # CurrentPageBot,  # Sets 'current_page'. Process it in treat_page method.
    #                  # Not needed here because we have subclasses
    ExistingPageBot,  # CurrentPageBot which only treats existing pages
    NoRedirectPageBot,  # CurrentPageBot which only treats non-redirects
):

    def __init__(self, generator, **kwargs):
        """
        Constructor.

        @param generator: the page generator that determines on which pages
            to work
        @type generator: generator
        """
        # Add your own options to the bot and set their defaults
        # -always option is predefined by BaseBot class
        self.availableOptions.update({
            'summary': u'ربات: جایگزینی پیوند جادویی شابک با الگو شابک',
        })

        # call constructor of the super class
        super(ISBNBot, self).__init__(site=True, **kwargs)

        # handle old -dry paramter
        self._handle_dry_param(**kwargs)

        # assign the generator to the bot
        self.generator = generator

    def _handle_dry_param(self, **kwargs):
        """
        Read the dry parameter and set the simulate variable instead.

        This is a private method. It prints a deprecation warning for old
        -dry paramter and sets the global simulate variable and informs
        the user about this setting.

        The constuctor of the super class ignores it because it is not
        part of self.availableOptions.

        @note: You should ommit this method in your own application.

        @keyword dry: deprecated option to prevent changes on live wiki.
            Use -simulate instead.
        @type dry: bool
        """
        if 'dry' in kwargs:
            issue_deprecation_warning('dry argument',
                                      'pywikibot.config.simulate', 1)
            # use simulate variable instead
            pywikibot.config.simulate = True
            pywikibot.output('config.simulate was set to True')

    def guess_language(self, txt):
        LatinLetters = set(string.ascii_letters)
        # Remove common non-word characters
        txt = re.sub('[\{\[\}\]\|=,.\-\'"*]', '', txt)
        total = 0
        latin = 0

        for char in txt:
            total += 1
            if char in LatinLetters:
                latin += 1

        if total == 0:
            return False

        if float(latin) / total > 0.5:
            return 'Latin'
        else:
            return 'Non-latin'

    def treat_page(self):
        text = self.current_page.text
        newtext = u''
        lines = text.split('\n')
        anyISBN = False
        ISBNpat = u' ISBN\s((?=[-0-9xX ]{17})(?:[0-9]+[- ]){3,4}[0-9]*[xX0-9])'

        for line in lines:
            # Add a space before ISBN to make it easier for the pattern to detect it
            line = line.replace('=ISBN', '= ISBN')
            line = line.replace('|ISBN', '| ISBN')

            hasISBN = re.search(ISBNpat, line)

            if hasISBN:
                anyISBN = True
                ISBNlink = hasISBN.group(0)
                ISBNpart = hasISBN.group(1)

                # Use the last (up to) 50 characters to determine language
                linepart = line[max(line.index('ISBN') - 50, 0):line.index('ISBN')]

                gl = self.guess_language(linepart)
                if gl is False:
                    # Do not change the line as we cannot guess its language
                    pass
                elif gl == 'Latin':
                    replacement = u' {{ISBN|' + ISBNpart + u'|en}}'
                    line = line.replace(ISBNlink, replacement)
                else:
                    if (u'شابک=' in line or u'شابک =' in line):
                        replacement = ISBNpart
                    else:
                        replacement = u' {{شابک|' + ISBNpart + u'}}'
                    line = line.replace(ISBNlink, replacement)

            newtext += line + '\n'

        if anyISBN:
            self.put_current(newtext, summary=self.getOption('summary'))


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    options = {}
    # Process global arguments to determine desired site
    local_args = pywikibot.handle_args(args)

    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    genFactory = pagegenerators.GeneratorFactory()

    # Parse command line arguments
    for arg in local_args:

        # Catch the pagegenerators options
        if genFactory.handleArg(arg):
            continue  # nothing to do here

        # Now pick up your own options
        arg, sep, value = arg.partition(':')
        option = arg[1:]
        if option in ('summary', 'text'):
            if not value:
                pywikibot.input('Please enter a value for ' + arg)
            options[option] = value
        # take the remaining options as booleans.
        # You will get a hint if they aren't pre-definded in your bot class
        else:
            options[option] = True

    gen = genFactory.getCombinedGenerator()
    if gen:
        # The preloading generator is responsible for downloading multiple
        # pages from the wiki simultaneously.
        gen = pagegenerators.PreloadingGenerator(gen)
        # pass generator and private options to the bot
        bot = ISBNBot(gen, **options)
        bot.run()  # guess what it does
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False

if __name__ == '__main__':
    main()
