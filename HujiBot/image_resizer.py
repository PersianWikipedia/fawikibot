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


class ImageResizerBot:

    def __init__(self):
        self.cat = 'رده:محتویات غیر آزاد'
        self.site = pywikibot.Site()
        self.summary = 'کوچک کردن تصویر غیر آزاد'

    def get_image_from_image_page(self, imagePage):
        """Get the image object to work based on an imagePage object."""
        imageURL = imagePage.get_file_url()
        imageURLopener = http.fetch(imageURL)
        imageBuffer = io.BytesIO(imageURLopener.content[:])
        image = Image.open(imageBuffer)
        return image

    def treat(self, filepage):
        text = filepage.text

        pat = r'\{\{([Nn]on-free no reduce|پرهیز از نسخه کوچکتر)\}\}'
        regex = re.compile(pat)

        if regex.search(text) is not None:
            return

        fileinfo = filepage.latest_file_info

        width = fileinfo.width
        height = fileinfo.height

        if (width < 500 and height < 500) or width * height < 100000:
            return

        newwidth = math.floor(width * math.sqrt(100000 / (width * height)))
        newheight = math.floor(height * math.sqrt(100000 / (width * height)))

        img = self.get_image_from_image_page(filepage)
        newimg = img.resize((newwidth, newheight))
        filepath = '/tmp/' + filepage.title(with_ns=False)

        newimg.save(filepath)
        self.site.upload(
            filepage,
            source_filename=filepath,
            comment=self.summary,
            ignore_warnings=True)
        os.remove(filepath)

    def run(self):
        cat = pywikibot.Category(self.site, self.cat)
        gen = pagegenerators.CategorizedPageGenerator(cat)

        for page in pagegenerators.PreloadingGenerator(gen):
            self.treat(page)


if __name__ == "__main__":
    bot = ImageResizerBot()
    bot.run()
