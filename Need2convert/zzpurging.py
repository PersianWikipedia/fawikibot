#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2011
#
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-

import catlib,query,config
import pagegenerators,re,sys,fa_cosmetic_changes
import wikipedia,codecs,string,time
from xml.dom import minidom
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
page_list_run=[]
#-----------------------------------------------version-----------------------------------------
def englishdictionry( enlink ,firstsite='fa',secondsite='en'):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    if enlink.find('#')!=-1:
        return False
    if enlink==u'':
        return False    
    enlink=enlink.replace(u' ',u'_')
    site = wikipedia.getSite(firstsite)
    sitesecond= wikipedia.getSite(secondsite)
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': enlink,
        'redirects': 1,
        'lllimit':500,
    }
    try:
        categoryname = query.GetData(params,site)  
        for item in categoryname[u'query'][u'pages']:
            case=categoryname[u'query'][u'pages'][item][u'langlinks']
        for item in case:
            if item[u'lang']==secondsite:
                intersec=item[u'*']
                break
        result=intersec
        return result
    except: 
        return False

def purgquery(falink,pagesite):
    temps=[]
    if pagesite=='en':
        enlink=englishdictionry(falink)
    else:
        enlink=falink
    if enlink:
        enlink=enlink.replace(u' ',u'_')
        site = wikipedia.getSite(pagesite)
        #https://en.wikipedia.org/w/api.php?action=purge&titles=Iran|Tehran|Greece|Germany&forcelinkupdate=1
        params = {
                'action': 'purge',
                'titles': enlink,
                'forcelinkupdate': 1
        }

        #try:
        if params:
            categoryname = query.GetData(params,site)
            for item in categoryname[u'purge']:
                templateha=item[u'title']
                break
            return templateha
        #except: 
        #    return u''
def run(gen,pagesite='en'):
    for pagework in gen:
        purgetiltle=purgquery(pagework,'en')
        if purgetiltle:
            wikipedia.output(u'Purged --->'+purgetiltle)
        purgetiltle=purgquery(pagework.title(),'fa')
        if purgetiltle:
            wikipedia.output(u'Purged --->'+purgetiltle)

def main():
    wikipedia.config.put_throttle = 0
    wikipedia.put_throttle.setDelay()
    summary_commandline,gen,template = None,None,None
    namespaces,PageTitles,exceptions = [],[],[]
    encat,newcatfile='',''
    autoText,autoTitle = False,False
    recentcat,newcat=False,False
    genFactory = pagegenerators.GeneratorFactory()
    for arg in wikipedia.handleArgs():
        if arg == '-autotitle':
            autoTitle = True
        elif arg == '-autotext':
            autoText = True
        elif arg.startswith( '-page' ):
            if len( arg ) == 5:
                PageTitles.append( wikipedia.input( u'Which page do you want to chage?' ) )    
            else:
                PageTitles.append( arg[6:] )
            break
        elif arg.startswith( '-except:' ):
            exceptions.append( arg[8:] )
        elif arg.startswith( '-template:' ):
            template = arg[10:]
        elif arg.startswith( '-encat:' ):
            encat = arg[7:].replace(u'Category:',u'').replace(u'category:',u'').replace(u'رده:',u'')
            break
        elif arg.startswith( '-newcatfile:' ):
            newcatfile = arg[12:]
            break
        elif arg.startswith('-recentcat'):    
            arg=arg.replace(':','')
            if len(arg) == 10:
                genfa = pagegenerators.RecentchangesPageGenerator()
            else:
                genfa = pagegenerators.RecentchangesPageGenerator(number = int(arg[10:]))
            genfa = pagegenerators.DuplicateFilterPageGenerator(genfa)
            genfa = pagegenerators.NamespaceFilterPageGenerator( genfa,[14] )
            preloadingGen = pagegenerators.PreloadingGenerator( genfa,60)
            recentcat=True
            break
        elif arg.startswith('-newcat'):    
            arg=arg.replace(':','')
            if len(arg) == 7:
                genfa = pagegenerators.NewpagesPageGenerator(100, False, None,14)
            else:
                genfa = pagegenerators.NewpagesPageGenerator(int(arg[7:]), False, None,14)
            preloadingGen = pagegenerators.PreloadingGenerator( genfa,60)
            newcat=True
            break
        elif arg.startswith( '-namespace:' ):
            namespaces.append( int( arg[11:] ) )
        elif arg.startswith( '-summary:' ):
            wikipedia.setAction( arg[9:] )
            summary_commandline = True
        else:
            generator = genFactory.handleArg( arg )
            if generator:
                gen = generator

    if PageTitles:
        pages = [wikipedia.Page( wikipedia.getSite(),PageTitle ) for PageTitle in PageTitles]
        gen = iter( pages )
    if recentcat:      
        for workpage in preloadingGen:
                workpage=workpage.title()
                cat = catlib.Category( wikipedia.getSite('fa'),workpage)
                gent = pagegenerators.CategorizedPageGenerator( cat )
                run( gent)
        wikipedia.stopme()    
        sys.exit()
    if newcat:
        run(preloadingGen)
    if newcatfile:
        text2 = codecs.open( newcatfile,'r' ,'utf8' )
        text = text2.read()
        linken = re.findall(ur'\[\[.*?\]\]',text, re.S)
        run(linken)
        wikipedia.stopme()    
        sys.exit()
    if not gen:
        wikipedia.stopme()    
        sys.exit()
    if namespaces != []:
        gen = pagegenerators.NamespaceFilterPageGenerator( gen,namespaces )
    preloadingGen = pagegenerators.PreloadingGenerator( gen,pageNumber = 60 )
    run( preloadingGen)
 
 
if __name__ == '__main__':
        main()
