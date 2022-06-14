#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot uncouples those shortened footnotes that are reused by using the
`name` parameter of the <ref> tag.
"""
#
# (C) User:Huji, 2019
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

#

import pywikibot
import re
from pywikibot import pagegenerators

from pywikibot.bot import (
    SingleSiteBot,
    ExistingPageBot,
    NoRedirectPageBot,
    AutomaticTWSummaryBot,
)

docuReplacements = {"&params;": pagegenerators.parameterHelp}


class RefDenamerBot(
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot
):
    def __init__(self, generator, **kwargs):
        super(RefDenamerBot, self).__init__(site=True, **kwargs)
        self.generator = generator
        self.summary = (
            "تمیزکاری پانویس‌های کوتاه "
            + "([[وپ:سیاست ربات‌رانی/"
            + "درخواست مجوز/HujiBot/وظیفه ۲۱|وظیفه ۲۱]])"
        )
        self.allowednamespaces = [0]

    def treat_page(self):
        text = self.current_page.text

        def_pat = (
            "<ref ([^>]*)name=([\"']?)([^>'\"]+)([\"']?)([^>]*)>"
            + "({{پک\\|[^<]+\\}\\})"
            + "<\\/ref>"
        )

        while re.search(def_pat, text) is not None:
            m = re.search(def_pat, text)
            original = m.group(0)
            name = m.group(3)
            fullform = (
                "<ref " + m.group(1) + m.group(5) + ">" + m.group(6) + "</ref>"
            )
            fullform = fullform.replace("<ref >", "<ref>")
            reuse_pat = (
                "<ref ([^>/]* )*name=[\"']?"
                + re.escape(name)
                + "[\"']?( [^>/]*)*/>"
            )

            text = re.sub(reuse_pat, fullform, text)
            text = text.replace(original, fullform)

        self.put_current(text, summary=self.summary)


def main(*args):
    options = {}
    local_args = pywikibot.handle_args(args)

    genFactory = pagegenerators.GeneratorFactory()

    for arg in local_args:
        if genFactory.handleArg(arg):
            continue  # nothing to do here
        arg, sep, value = arg.partition(":")
        option = arg[1:]
        if option in ("summary"):
            if not value:
                pywikibot.input("Please enter a value for " + arg)
            options[option] = value
        else:
            options[option] = True

    gen = genFactory.getCombinedGenerator()
    if gen:
        gen = pagegenerators.PreloadingGenerator(gen)
        bot = RefDenamerBot(gen, **options)
        bot.run()
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False


if __name__ == "__main__":
    main()
