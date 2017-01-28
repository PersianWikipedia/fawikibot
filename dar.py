#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
dar.py - a script to move categories by request

useage:

    python pwb.py dar [OPTIONS]

"""
#
# (C) Reza (w:fa:User:Reza1615), 2015
# (C) Amir (w:fa:User:Ladsgroup), 2015
# (C) Huji (w:fa:User:Huji), 2016
#
# Distributed under the terms of MIT License (MIT)
#
from __future__ import absolute_import, unicode_literals

#

import pywikibot
from pywikibot import pagegenerators
import sys
import json
import codecs
import re
from scripts import category


class CatMoveBot:

    def __init__(self, logPage=None):
        if logPage is None:
            raise ValueError('Log page must be specified')
        self.logPage = logPage
        self.site = pywikibot.Site('fa')
        self.redirTemplate = u'رده بهتر'
        self.summary = u'[[وپ:دار|ربات: انتقال رده]] به درخواست [[User:' + \
            '%s|%s]] از [[:%s]] به [[:%s]]'

    """
    Actually moves pages from one category to the other.

    @param origin: name of the origin category
    @param destination: name of the destination category
    @param user: Name of the user on whose behalf the category move is done
    """
    def move(self, origin, destination, user):
        comment = self.summary % (user, user, origin, destination)
        cat = category.CategoryMoveRobot(
            origin, destination, batch=True,
            comment=comment, inplace=False, move_oldcat=True,
            delete_oldcat=True, title_regex=None, history=False)
        cat.run()

    """
    Plans moving pages from one category to the other, and updates the category
    pages to reflect this move.

    @param task: A list with two elements; the first element is the name of the
        origin category, and the second is the name of the destination category
    @param user: Name of the user on whose behalf the category move is done
    """
    def run(self, task, user):
        origin = task[0]
        destination = task[1]
        # Title of the destination page, without prefix
        destTitle = re.sub('^(رده|[Cc]ategory)\:', '', destination)

        originPage = pywikibot.Page(self.site, origin)
        destinationPage = pywikibot.Page(self.site, destination)
        originPageText = ''
        destinationPageText = ''

        if originPage:
            try:
                originPageText = originPage.get()
                # Replace contents with the {{Category redirect}} template
                originPage.put(
                    '{{' + self.redirTemplate + '|' + destTitle + '}}',
                    self.summary % (user, user, origin, destinatino))
            except:
                # Failed to fetch page contents. Gracefully ignore!
                pass

        if destinationPage:
            try:
                originPageText = originPage.get()
                # TODO: Remove old {{Category redirect}}
            except:
                # Failed to fetch page contents. Gracefully ignore!
                pass

        self.move(origin, destination, user)


class CatMoveInput:

    """
    @param cacheFile: path to the local cache of previously validated users
    """
    def __init__(self, cacheFile=None):
        if cacheFile is None:
            raise ValueError('Cache file location must be specified')
        else:
            self.cacheFile = cacheFile
        self.cache = self.loadCache()
        self.site = pywikibot.Site('fa')
        self.tasksPageDefault = u'{{/بالا}}'
        self.moverBots = [u'Dexbot', u'HujiBot']
        self.threshold = 3000
        self.successSummary = u'ربات: انتقال رده انجام شد!'

    def loadCache(self):
        f = codecs.open(self.cacheFile, 'r', 'utf-8')
        txt = f.read().strip()
        f.close()
        if txt == '':
            # Brand new cache file, will fail json.loads()
            # Return an empty dictionary instead
            cache = {}
        else:
            cache = json.loads(txt)
        return cache

    """
    @param cache: Validated users cache in JSON format
    """
    def updateCache(self, cache):
        fh = codecs.open(self.cacheFile, 'w', 'utf-8')
        fh.write(json.dumps(cache))
        fh.close()

    """
    Verifies that the user's edit count is greater than self.threshold

    @param username
    """
    def verifyUser(self, username):
        username = username.replace(u' ', u'_')

        # If we have already established that this user qualifies
        # then don't verify the user again
        if self.cache.get(username):
            return True

        # Only users whose edit count is larger than self.threshold
        # can request category moves
        params = {
            'action': 'query',
            'list': 'users',
            'ususers': username,
            'usprop': 'editcount'
        }

        try:
            req = pywikibot.data.api.Request(site=self.site, **params)
            query = req.submit()
            if query[u'query'][u'users'][0][u'editcount'] > self.threshold:
                self.cache[username] = True
                self.updateCache(self.cache)
                return True
            else:
                return False
        except:
            return False

    """
    Looks for a list of category move requests on the given page.

    Each task must be defined in a separate line using either of the following
    three formats:

    * Category:Origin > Category:Destination
    * [[:Category:Origin]] > [[:Category:Destination]]
    * Origin @ Destination

    Spaces are optional around `>` and `@` characters, and after the `*`.

    If such a list is found, it will return a dictionary object containing a
    list of category move tasks and name of the user on whose behalf categories
    are moved.

    @param tasksPageName: Wiki page on which category move requests are listed
    """
    def processInput(self, tasksPageName):
        tasksPage = pywikibot.Page(self.site, tasksPageName)

        try:
            pageText = tasksPage.get()
            pageHistory = tasksPage.getVersionHistory()
            lastUser = pageHistory[0][2]
        except pywikibot.IsRedirectPage:
            tasksPage = tasksPage.getRedirectTarget()
            try:
                pageText = tasksPage.get()
                pageHistory = tasksPage.getVersionHistory()
                lastUser = pageHistory[0][2]
            except:
                raise ValueError('Task list page not found!')
        except:
            raise ValueError('Task list page not found!')

        if lastUser in self.moverBots:
            print json.dumps({
                'result': 'Last edit was by a mover bot. Request ignored.'
            })
            return False
        elif self.verifyUser(lastUser):
            print json.dumps({
                'result': 'User verified. Processing task list.'
            })
            tasks = self.getTaskList(pageText)
            tasksPage.put(self.tasksPageDefault, self.successSummary)
            return {'tasks': tasks, 'user': lastUser}
        else:
            print json.dumps({
                'result': 'Last editor was not qualified. Request ignored.'
            })
            return False

    """
    Returns a list of lists, where each inner lists describe one category move
    request (i.e. [origin, destination]).

    @param taskText: wikicode of the page containing category move requests
    """
    def getTaskList(self, taskText):
        taskList = []
        for line in taskText.strip('\r').split('\n'):
            if line[0] == '*':
                # Remove the * and any immediately following spaces
                line = re.sub('^\* *', '', line)
                # Unlink category links
                if '[[' in line:
                    line = re.sub('\[\[\:(رده|[Cc]ategory)\:([^\]]+)\]\]',
                                  '\\1:\\2', line)
                # Split by '>' or '@' (optionally surrounded by spaces)
                if '>' in line or '@' in line:
                    pieces = re.split(' *[>@] *', line)
                    # Clean up category mentions
                    for i in range(0, len(pieces)):
                        # Make edit summaries more beautiful!
                        pieces[i] = pieces[i].replace(u'_', u' ')
                        # Add missing `Category` prefix
                        if (
                            re.search('^[Cc]ategory\:', pieces[i]) is None and
                            re.search('^رده\:', pieces[i]) is None
                        ):
                            pieces[i] = u'رده:' + pieces[i]
                    # Add the pair to our task list
                    taskList.append(pieces)
                else:
                    # Skip the line
                    pass
        return taskList


def main():
    cacheFile = '/data/project/dexbot/cache_dar.txt'

    vBot = CatMoveInput(cacheFile)
    req = vBot.processInput(u'ویکی‌پدیا:درخواست انتقال رده')

    for task in req['tasks']:
        mBot = CatMoveBot(u'ویکی‌پدیا:درخواست انتقال رده')
        mBot.run(task, req['user'])

if __name__ == '__main__':
    main()
