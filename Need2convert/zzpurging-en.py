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

def purgquery(enlink):
    temps=[]
    if enlink:
        enlink=enlink.replace(u' ',u'_')
        site = wikipedia.getSite('en')
        #https://en.wikipedia.org/w/api.php?action=purge&titles=Iran|Tehran|Greece|Germany&forcelinkupdate=1
        params = {
                'action': 'purge',
                'titles': enlink,
                'forcelinkupdate': 1
        }
        wikipedia.output(str(params))
        #try:
        if params:
            categoryname = query.GetData(params,site)
            for item in categoryname[u'purge']:
                templateha=item[u'title']
                break
            return templateha
        #except: 
        #    return u''

mylist=[u"Template:2010 FIFA World Cup finalists/sandbox",
u"Template:Age in sols/doc",
u"Template:ALB/doc",
u"Template:ARE/doc",
u"Template:ARG/doc",
u"Template:Art world",
u"Template:BAG assistance needed",
u"Template:Bakhshe Janah",
u"Template:Bakhshe Markazi Bastak",
u"Template:Beethoven piano sonatas/doc",
u"Template:Better source/doc",
u"Template:BFA/doc",
u"Template:Bfidb individual/doc",
u"Template:BGD/doc",
u"Template:Bio icon2",
u"Template:Book/doc",
u"Template:Calendar/Sun1stMonthStartFri",
u"Template:Calendar/Sun1stMonthStartSat",
u"Template:Calendar/Sun1stMonthStartWed",
u"Template:CAN/doc",
u"Template:COI/doc",
u"Template:Color topics/doc",
u"Template:Compression software implementations/doc",
u"Template:Consonants/doc",
u"Template:Controversial-issues/doc",
u"Template:Controversial/doc",
u"Template:Country data Bohemia/doc",
u"Template:Country data Bosnia and Herzegovina/doc",
u"Template:Country data Burma/doc",
u"Template:Country data Byelorussian SSR/doc",
u"Template:Country data Chuuk/doc",
u"Template:Country data Karelia/doc",
u"Template:Country data Limburg (Netherlands)/doc",
u"Template:Country data Melilla/doc",
u"Template:Country data Mohéli/doc",
u"Template:Country data Pohnpei/doc",
u"Template:Country data Timor-Leste/doc",
u"Template:Country data Wake Island/doc",
u"Template:CPV/doc",
u"Template:CUB/doc",
u"Template:Db-song-notice/doc",
u"Template:Digital distribution platforms/doc",
u"Template:Dispute-resolution/medcom",
u"Template:Disputed-category/doc",
u"Template:EGY/doc",
u"Template:Epic Mickey series",
u"Template:Facts/doc",
u"Template:Fbm/doc",
u"Template:Filmsbygenre",
u"Template:Football squad end",
u"Template:Football squad mid",
u"Template:Further reading cleanup/doc",
u"Template:General Motors",
u"Template:GEO/doc",
u"Template:Geographic Location 2/doc",
u"Template:GNU/doc",
u"Template:Google trends/doc",
u"Template:Greek mythology (deities)",
u"Template:Horse latitudes coordinates",
u"Template:IFIS/doc",
u"Template:Indonesia Provinces TOC",
u"Template:Infobox carbon/doc",
u"Template:Infobox iron/doc",
u"Template:Infobox livermorium/doc",
u"Template:Infobox lunar crater or mare/doc",
u"Template:Infobox Upanishad/doc",
u"Template:Infobox zinc/doc",
u"Template:ISS-Dockingbays1",
u"Template:JAM/doc",
u"Template:KGZ/doc",
u"Template:Khowar language sidebar",
u"Template:KIR/doc",
u"Template:Labelled Map of South Africa Provinces",
u"Template:Latin America and Caribbean topic/doc",
u"Template:LCA/doc",
u"Template:Lists of Solar System objects/doc",
u"Template:LTU/doc",
u"Template:Main Page interwikis",
u"Template:Marxian economics",
u"Template:Match report templates",
u"Template:Measurement-stub",
u"Template:MLI/doc",
u"Template:MNE/doc",
u"Template:MOZ/doc",
u"Template:Multi-listen item/doc",
u"Template:NGA/doc",
u"Template:Non-free promotional/doc",
u"Template:NOR/doc",
u"Template:North America topic/doc",
u"Template:Northern Irish members of HMC",
u"Template:Party shading/Federalist/doc",
u"Template:Pashto language sidebar",
u"Template:PCN/doc",
u"Template:PD/doc",
u"Template:Platonism/doc",
u"Template:PLW/doc",
u"Template:PNG/doc",
u"Template:PRK/doc",
u"Template:Psychology subfields",
u"Template:Quentin Tarantino/sandbox",
u"Template:R30",
u"Template:Reference necessary/doc",
u"Template:S/c",
u"Template:SCref/doc",
u"Template:SEN/doc",
u"Template:Ship types",
u"Template:SLE/doc",
u"Template:Sockpuppetry/doc",
u"Template:Solar System table/doc",
u"Template:SOM/doc",
u"Template:Sony Pictures",
u"Template:Star/doc",
u"Template:Starbox character/doc",
u"Template:STP/doc",
u"Template:Substitution/doc",
u"Template:Succession box/doc",
u"Template:SVK/doc",
u"Template:SWE/doc",
u"Template:Swiss populations data CH-AR/doc",
u"Template:SYR/doc",
u"Template:Talk archive/doc",
u"Template:Tertiary source inline/doc",
u"Template:Time zones of Australia labeled",
u"Template:Tl2/belge",
u"Template:Tl2/doc",
u"Template:Tlsx/doc",
u"Template:Tlxs/doc",
u"Template:Topic (Asia)/doc",
u"Template:Topic (North America)/doc",
u"Template:UEFA Euro 1992 finalists",
u"Template:Unblock-auto/doc",
u"Template:URY/doc",
u"Template:User fr-ca-3",
u"Template:User fr-ca-3/doc",
u"Template:User Iran's PEACEFUL Nuclear Energy",
u"Template:User language category/doc",
u"Template:User ml",
u"Template:User ustrix la-2",
u"Template:User WPVG/doc",
u"Template:VAT/doc",
u"Template:Weather box/cold/sandbox",
u"Template:Weather box/colpastel/sandbox",
u"Template:Weather box/cols/sandbox",
u"Template:Weather box/cols/sandbox2",
u"Template:Weather box/oneline/sandbox",
u"Template:Web colors/doc",
u"Template:West Asia topic",
u"Template:YEM/doc",]
for i in mylist:
    a=purgquery(i)
    enpage=wikipedia.Page( wikipedia.getSite('en'),i )
    text=enpage.get()
    try:
        enpage.put(text,'bot:null edit')
    except:
        pass
