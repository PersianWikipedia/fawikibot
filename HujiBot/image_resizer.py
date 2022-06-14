#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
image_resizer.py - a script that reduces the size of non-free images

usage:

    python pwb.py image_resizer
"""
#
# (C) w:fa:User:Huji, 2021
#
# Distributed under the terms of the MIT license.
#


import io
import os
import math
from PIL import Image
import pywikibot
from pywikibot import pagegenerators
from pywikibot.comms import http
import re
import urllib


class ImageResizerBot:
    def __init__(self):
        self.cat = "رده:محتویات غیر آزاد"
        self.site = pywikibot.Site()
        self.summary = (
            "کوچک کردن تصویر غیر آزاد ([[ویکی‌پدیا:"
            + "سیاست ربات‌رانی/درخواست مجوز/HujiBot/وظیفه ۲۴|وظیفه ۲۴]])"
        )

    def get_resized_image(self, file_page, thumb_width):
        """Get the image object to work based on an imagePage object."""
        thumb_url = "https://fa.wikipedia.org/w/thumb.php?f=%s&w=%s" % (
            urllib.parse.quote_plus(file_page.title(with_ns=False)),
            thumb_width,
        )
        imageURLopener = http.fetch(thumb_url)
        imageBuffer = io.BytesIO(imageURLopener.content[:])
        image = Image.open(imageBuffer)
        return image

    def treat(self, filepage):
        print(filepage)

        text = filepage.text

        pat = r"\{\{([Nn]on-free no reduce|پرهیز از نسخه کوچکتر)\}\}"
        regex = re.compile(pat)

        if regex.search(text) is not None:
            return

        fileinfo = filepage.latest_file_info

        width = fileinfo.width
        height = fileinfo.height

        if width * height > 100000:
            newwidth = math.floor(width * math.sqrt(100000 / (width * height)))
            newimg = self.get_resized_image(filepage, newwidth)
            filepath = "/tmp/" + filepage.title(with_ns=False)

            newimg.save(filepath)
            self.site.upload(
                filepage,
                source_filename=filepath,
                comment=self.summary,
                ignore_warnings=True,
            )
            os.remove(filepath)

            filepage = pywikibot.FilePage(self.site, filepage.title())
            filehistory = filepage.get_file_history()

            for key in filehistory:
                version = filehistory[key]
                if version["width"] * version["height"] <= 100000:
                    continue
                oldimageid = version["archivename"].split("!")[0]
                self.site.deleterevs(
                    "oldimage",
                    oldimageid,
                    hide="content",
                    show="",
                    reason=self.summary,
                    target=filepage.title(),
                )

    def get_categories_list(self, page):
        cats = list(page.categories())
        cat_titles = list()
        for c in cats:
            cat_titles.append(c.title(with_ns=False))
        return cat_titles

    def run(self):
        cat = pywikibot.Category(self.site, self.cat)
        gen = pagegenerators.CategorizedPageGenerator(cat)
        pgen = pagegenerators.PreloadingGenerator(gen)

        for page in pgen:
            ignored_extensions = [".pdf", ".svg", ".ogg", "webm"]
            cat_list = self.get_categories_list(page)
            if "محتویات آزاد" in cat_list:
                continue
            if ignored_extensions.count(page.title()[-4:].lower()) == 0:
                self.treat(page)


if __name__ == "__main__":
    bot = ImageResizerBot()
    bot.run()
