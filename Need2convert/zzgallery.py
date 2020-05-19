#!/usr/bin/python
# -*- coding: utf-8 -*-
# BY: رضا (User:reza1615 on fa.wikipedia)
# Distributed under the terms of the CC-BY-SA 3.0.
import wikipedia
import pagegenerators,query,sys
import fa_cosmetic_changes
import re, os, codecs, catlib,login
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()    
secondwiki='en'
faSite = wikipedia.getSite('fa')
enSite = wikipedia.getSite(secondwiki)
txtTmp=''
faChrs = u'ءاآأإئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیًٌٍَُِّْٓيك'
msg = u'ربات: افزودن نگارخانهٔ آزاد به مقاله'
usernames=u'Fatranslator'    
_cache={}
def login_fa(usernames):    
    try:
        password_fa = open("/data/project/rezabot/pywikipedia/passfile2", 'r')
    except:
        password_fa = open("/home/reza/compat/passfile2", 'r')

    password_fa=password_fa.read().replace('"','').strip()
    passwords=password_fa.split('(')[1].split(',')[1].split(')')[0].strip()
    #-------------------------------------------
    botlog=login.LoginManager(password=passwords,username=usernames,site=faSite)
    botlog.login()

def englishdictionry( enlink ,firstsite,secondsite):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.split(u'#')[0].strip()
    enlink=enlink.replace(u' ',u'_')
    if _cache.get(tuple([enlink, 'englishdictionry'])):
        return _cache[tuple([enlink, 'englishdictionry'])]
    if enlink==u'':
        _cache[tuple([enlink, 'englishdictionry'])]=False
        return False    

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
        _cache[tuple([enlink, 'englishdictionry'])]=result
        return result
    except: 
        _cache[tuple([enlink, 'englishdictionry'])]=False
        return False

def text_translator(text):
        linken = re.findall(ur'\[\[.*?\]\]',text, re.S)
        for item in linken:
                itemmain=item
                item=item.replace(u'en:',u'')
                if item.find('user:')!=-1 or item.find('User:')!=-1 or item.find('template:')!=-1 or item.find('Template:')!=-1 or item.find('category:')!=-1 or item.find('Category:')!=-1 or item.find('Wikipedia:')!=-1 or item.find('wikipedia:')!=-1 or item.find('Talk:')!=-1 or item.find('talk:')!=-1 or item.find('Help:')!=-1 or item.find('help:')!=-1:
                    continue
                itemen=item.split(u'|')[0].replace(u'[[',u'').replace(u']]',u'').strip()
                if text.find(itemmain)!=-1:
                    itemfa=englishdictionry(itemen ,'en','fa')
                    wikipedia.output(itemen)
                else:
                    continue
                if itemfa==False:
                    itemen=item.replace(u'[[',u'').replace(u']]',u'').strip()
                    itemen=itemen.replace(u'[[',u'').replace(u']]',u'')
                    text=text.replace(u'[['+itemen+u']]',u'@1@'+itemen+u'@2@')
                    continue
                else:
                    text=text.replace(itemmain,u'@1@'+itemfa+u'@2@')
                linken = re.findall(ur'\[\[.*?\]\]',text, re.S)
        text=text.replace(u'@1@',u'[[').replace(u'@2@',u']]')
        return text
def checksite(gallery,text):
    commons_images,image_texts=[],[]
    for aa in range(0,30):        
        gallery=gallery.replace(u' |',u'|').replace(u'\t',u'')
    gallery=gallery.replace(u'\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n')
    images=gallery.replace(u'\r',u'').split(u'\n')

    for image in images:
        if image.strip()=="":    
            continue
        imagefa=image
        image=image.split(u'|')[0].strip()
        imagecheck=image.replace(u'File:',u'').replace(u'file:',u'').replace(u'Image:',u'').replace(u'image:',u'')
        imagecheck=imagecheck.replace(u'پرونده:',u'').replace(u'تصویر:',u'').replace(u'تصوير:',u'').replace(u'رسانه:',u'')
        if image=="":    
            continue
        if image.find(u'.ogg')!=-1 or image.find(u'>')!=-1 or image.find(u'.oga')!=-1 or image.find(u'.ogv')!=-1 or image.find(u'.mid')!=-1:
            continue    
        params = {
                'action': 'query',
                'titles': image,#Image name
                'prop': 'imageinfo'
        }
        try :
           extend=imagefa.split(u'|')[1]    
           image_text=imagefa.replace(image.split(u'|')[0]+u'|',image.split(u'|')[0]+u'|<!--')+u'-->'
        except:
           image_text=imagefa.split(u'|')[0].strip()+u'|'
        try:
            queryresult = query.GetData(params)
            items=queryresult['query']['pages']
            for item in items:
                if queryresult['query']['pages'][item]['imagerepository']=='shared':
                    if text.lower().find(imagecheck.lower())!=-1 or text.lower().find(imagecheck.replace(u'_',u' ').lower())!=-1:
                       continue
                    image_texts.append(image_text)      
                else:
                    continue
        except:
            continue
    if image_texts !=[]:
        gallery=u'<gallery>\n'       
        for item in image_texts: 
            gallery+=item+u'\n'
        gallery+=u'</gallery>\n'
        gallery=text_translator(gallery)
        wikipedia.output(u'\03{lightgreen}'+gallery+u'\03{default}')
        return gallery
    else:
        return False
def enwikiimagecheck(text_en2):
    try:
        im = re.search(ur'<(?:gallery)[^<>]*>[\S\s]*?</(?:gallery)>', text_en2)
        imagename=im.group(0).strip()
        return imagename.replace(u'<gallery>',u'<gallery>\n').replace(u'</gallery>',u'\n</gallery>')
    except:
        return False
def BotRun(page,text_fa,text_en):
    try:
        pagename=page.replace(u'Fa:',u'').replace(u'fa:',u'').replace(u'[[',u'').replace(u']]',u'').strip()
    except:    
        pagename=unicode(str(page),'UTF-8').replace(u'Fa:',u'').replace(u'fa:',u'').replace(u'[[',u'').replace(u']]',u'').strip()
    page=wikipedia.Page(faSite,pagename)
#--------------------------------------------------------------action that you want to do on pages-----------------
    text_fa2=text_fa.replace(u'\r',u'')
    text_en2=text_en.replace(u'\r',u'')
    imagename=u''
    try: 
        imagename=enwikiimagecheck(text_en2)
        if imagename:
            engallerry=checksite(imagename,text_fa)
            if engallerry:
               try:
                  imfa = re.search(ur'<(?:gallery)[^<>]*>[\S\s]*?</(?:gallery)>', text_fa2)
                  imagename=imfa.group(0).strip()
                  wikipedia.output( u"--fa wiki's page had gallery so it pass!--" )
                  return False
               except:
                    text_fa2=text_fa2.replace(u'\r',u'')    
                    if text_fa2.find(u'== جستارهای وابسته ==')!=-1 or text_fa2.find(u'==جستارهای وابسته==')!=-1 or text_fa2.find(u'== جُستارهای وابسته ==')!=-1 or text_fa2.find(u'==جُستارهای وابسته==')!=-1:
                       text_fa2=text_fa2.replace(u'==جستارهای وابسته==',u'== جستارهای وابسته ==').replace(u'== جُستارهای وابسته ==',u'== جستارهای وابسته ==').replace(u'==جُستارهای وابسته==',u'== جستارهای وابسته ==')
                       text_fa2=text_fa2.replace(u'== جستارهای وابسته ==',u'== نگارخانه ==\n'+engallerry+u'\n== جستارهای وابسته ==')
                       return text_fa2    
                    if text_fa2.find(u'== پانویس ==')!=-1 or text_fa2.find(u'==پانویس==')!=-1 :
                       text_fa2=text_fa2.replace(u'== پانویس ==',u'== نگارخانه ==\n'+engallerry+u'\n== پانویس ==')
                       return text_fa2    
                    if text_fa2.find(u'== منابع ==')!=-1 or text_fa2.find(u'==منابع==')!=-1 or text_fa2.find(u'==منبع==')!=-1 or text_fa2.find(u'==منبع‌ها==')!=-1 or text_fa2.find(u'== منبع ==')!=-1 or text_fa2.find(u'== منبع‌ها ==')!=-1:
                       text_fa2=text_fa2.replace(u'==منابع==',u'== منابع ==').replace(u'==منبع==',u'== منابع ==').replace(u'==منبع‌ها==',u'== منابع ==').replace(u'== منبع ==',u'== منابع ==').replace(u'== منبع‌ها ==',u'== منابع ==')
                       text_fa2=text_fa2.replace(u'== منابع ==',u'== نگارخانه ==\n'+engallerry+u'\n== منابع ==')
                       return text_fa2
                    if text_fa2.find(u'== پیوند به بیرون ==')!=-1 or text_fa2.find(u'==پیوند به بیرون==')!=-1 :
                       text_fa2=text_fa2.replace(u'== پیوند به بیرون ==',u'== نگارخانه ==\n'+engallerry+u'\n== پیوند به بیرون ==')
                       return text_fa2
                    if text_fa2.find(ur'رده:')!=-1:
                        num=text_fa2.find(ur'[[رده:')
                        text_fa2=text_fa2[:num]+u'== نگارخانه ==\n'+engallerry+'\n'+text_fa2[num:]
                    else:
                        m = re.search(ur'\[\[([a-z]{2,3}|[a-z]{2,3}\-[a-z\-]{2,}|simple):.*?\]\]', text_fa2)
                        if m:
                            if m.group(0)==u'[[en:Article]]':    
                                try:
                                    if string.count(text_fa2,u'[[en:Article]] --->')==1:
                                        text_fa2=text_fa2.split(u'[[en:Article]] --->')[0]+u'[[en:Article]] --->\n'+u'== نگارخانه ==\n'+engallerry+'\n'+text.split(u'[[en:Article]] --->')[1]
                                    else:
                                        text_fa2+='\n== نگارخانه ==\n'+engallerry    
                                except:
                                    text_fa2+='\n== نگارخانه ==\n'+engallerry
                            else:
                                num=text_fa2.find(m.group(0))
                                text_fa2=text_fa2[:num]+u'== نگارخانه ==\n'+engallerry+'\n'+text_fa2[num:]
                        else:                
                            text_fa2+='\n== نگارخانه ==\n'+engallerry
                    return text_fa2
            else:
                wikipedia.output( u"--en wiki's dosen't have gallery or images are locale!--" )
                return False
    except:
        wikipedia.output( u"--en wiki's dosen't have gallery or images are locale!--" )
        return False
#----------------------------------------------------------end of action that you want to do on pages---------------
def enpageget(interwiki):
            text_en=u' '
            for inter in interwiki:
                inters=str(inter)
                if inters.find(secondwiki+':')!=-1:
                    if inters.find('#')!=-1:    
                        return u' '
                    enSite = wikipedia.getSite(secondwiki)
                    page=wikipedia.Page(enSite,inter.title())
                    try:
                        if not page.canBeEdited():
                            wikipedia.output( u'Skipping locked page %s' % page.title() )
                            return u' '
                        text_en = page.get()#------------------------------geting pages content
                        return text_en
                    except wikipedia.NoPage:
                        wikipedia.output( u'Page %s not found' % page.title() )
                        continue
                    except wikipedia.IsRedirectPage:#----------------------geting pages redirects contents
                        pageRedirect = page.getRedirectTarget()
                        try:
                            text_en = pageRedirect.get()       
                            wikipedia.output( u'Page %s was Redirect but edited!' %  pageRedirect )
                            return text_en
                        except:
                            continue
                    except:
                         continue
                    return u' '
def run(generator):
        for pages in generator:
            if englishdictionry( pages ,'fa','en')==False:
                wikipedia.output( pages.title()+u' with out interwiki')    
                continue       
            try:
                pagename=unicode(str(pages),'UTF-8').replace(u'Fa:',u'').replace(u'fa:',u'').replace(u'[[',u'').replace(u']]',u'').strip()
            except:
               pagename=str(pages).replace(u'Fa:',u'').replace(u'fa:',u'').replace(u'[[',u'').replace(u']]',u'').strip()
            if pagename.find(u':')!=-1:
                continue
            pagefa=wikipedia.Page(faSite,pagename)
            try:
                if not pagefa.canBeEdited():    
                            wikipedia.output( u'Skipping locked page %s' % pagefa.title() )
                            continue
                text_fa = pagefa.get()#------------------------------geting pages content
                interwikis= pagefa.interwiki()
            except wikipedia.NoPage:
                wikipedia.output( u'Page %s not found' % pagefa.title() )
                continue
            except wikipedia.IsRedirectPage:#----------------------geting pages redirects contents
                 pageRedirect = pagefa.getRedirectTarget()
                 text_fa = pageRedirect.get()
                 interwikis= pagefa.interwiki()
                 wikipedia.output( u'Page %s was Redirect but edited!' %  pageRedirect )
            except:
                 continue
            if pagefa.namespace()!=0:
                wikipedia.output( u'---------------------------')
                wikipedia.output( pagename)
                wikipedia.output( u"names space is not article's namespace")
                continue
            if interwikis==[]:
                wikipedia.output( u'---------------------------')
                wikipedia.output( pagename)
                wikipedia.output( u"dosen't have english page!")
                continue
            text_en=enpageget(interwikis)
            try:
               test=text_en.replace(u'\n',u'')
            except:
                wikipedia.output( u'---------------------------')
                wikipedia.output( pagename)
                wikipedia.output( u"dosen't have english page!")
                continue    
            if text_en==u' ' or text_en==u'':
                wikipedia.output( u'---------------------------')
                wikipedia.output( pagename)
                wikipedia.output( u"dosen't have english page!")
                continue
            wikipedia.output( u'---------------------------')
            wikipedia.output( pagename)
            if text_fa.find(u'<gallery')!=-1 or text_fa.find(u'</gallery')!=-1:
                wikipedia.output( u'---------------------------')
                wikipedia.output( pagename)
                wikipedia.output( u"--fa wiki's page has gallery so it is passed")    
                continue
            pagesize=sys.getsizeof (text_fa)
            if pagesize>15000:#---------------------------------------------------مقالات خرد----------------
                wikipedia.output( u'---------------------------')
                wikipedia.output( pagename)
                wikipedia.output( u"--fa wiki's page is'nt SubArticle" )
                continue
  
            new_text=BotRun(pagename,text_fa,text_en)
            if new_text:
                savepart(pagename,new_text )#---------------saving changes in page with new_text content-----------------------------------
            else:
                wikipedia.output( u'Skipping %s ' %  pagename )
 
def savepart( page,new_text,msg=msg):     
            pagename=page.replace(u'Fa:',u'').replace(u'fa:',u'').replace(u'[[',u'').replace(u']]',u'').strip()
            page=wikipedia.Page(faSite,pagename)    
            new_text,cleaning_version,msg_clean=fa_cosmetic_changes.fa_cosmetic_changes(new_text,page,msg_short=False)
            if msg_clean:
                msg+=u' + '+msg_clean
            msg=msg.replace(u'+ +',u'+').strip()    
            try:
                page.put( new_text,msg ,watchArticle = None)   
            except wikipedia.EditConflict:
                wikipedia.output( u'Skipping %s because of edit conflict' % ( page.title() ) )
            except wikipedia.SpamfilterError,url:
                wikipedia.output( u'Cannot change %s because of blacklist entry %s' % ( page.title(),url ) )
def categorydown(listacategory):
    wikipedia.config.put_throttle = 0
    wikipedia.put_throttle.setDelay()
    count=1
    for catname in listacategory:
        count+=1
        if count==200:
            break
        gencat = pagegenerators.SubCategoriesPageGenerator(catname, recurse=False)
        for subcat in gencat:
            try:
                wikipedia.output(subcat)
            except:
                wikipedia.output(str(subcat))
            if subcat in listacategory:
                continue
            else:
                listacategory.append(subcat)
    return listacategory

def facatlist(facat):
    wikipedia.config.put_throttle = 0
    wikipedia.put_throttle.setDelay()
    count=0
    listenpageTitle=[]
    PageTitle=facat.replace(u'[[',u'').replace(u']]',u'').strip()
    language='fa'
    PageTitles =[PageTitle]  
    for PageTitle in PageTitles:
        cat = catlib.Category( wikipedia.getSite(language),PageTitle )
        listacategory=[cat]
        listacategory=categorydown(listacategory)
        for enpageTitle in listacategory:
                   enpageTitle=str(enpageTitle).split(u'|')[0].split(u']]')[0].replace(u'[[',u'').strip()
                   cat = catlib.Category( wikipedia.getSite(language),enpageTitle )
                   gent = pagegenerators.CategorizedPageGenerator( cat )
                   for pagework in gent:
                      count+=1
                      try:
                          link=str(pagework).split(u'|')[0].split(u']]')[0].replace(u'[[',u'').strip()
                      except:
                          pagework=unicode(str(pagework),'UTF-8')
                          link=pagework.split(u'|')[0].split(u']]')[0].replace(u'[[',u'').strip()
                      wikipedia.output(link)
                      fapagetitle=link
                      wikipedia.output(u'adding '+fapagetitle+u' to fapage lists')
                      listenpageTitle.append(fapagetitle)
    if listenpageTitle==[]:
        return False
    return listenpageTitle

def main():
    summary_commandline,template,gen = None,None,None
    exceptions,PageTitles,namespaces = [],[],[]
    cat=''
    autoText,autoTitle = False,False
    genFactory = pagegenerators.GeneratorFactory()
    arg=False#------if you dont want to work with arguments leave it False if you want change it to True---
    if arg==False:
        for arg in wikipedia.handleArgs():
            if arg == '-autotitle':
                autoTitle = True
            elif arg == '-autotext':
                autoText = True
            elif arg.startswith( '-page:' ):
                if len(arg) == 6:
                    PageTitles.append(wikipedia.input( u'Which page do you want to chage?' ))
                else:
                    PageTitles.append(arg[6:])
            elif arg.startswith( '-cat:' ):
                if len(arg) == 5:
                    cat=wikipedia.input( u'Which Category do you want to chage?' )
                else:
                    cat='Category:'+arg[5:]
            elif arg.startswith( '-template:' ):
                if len(arg) == 10:
                    template.append(wikipedia.input( u'Which Template do you want to chage?' ))
                else:
                    template.append('Template:'+arg[10:])
            elif arg.startswith('-except:'):
                exceptions.append(arg[8:])
            elif arg.startswith( '-namespace:' ):
                namespaces.append( int( arg[11:] ) )
            elif arg.startswith( '-ns:' ):
                namespaces.append( int( arg[4:] ) )    
            elif arg.startswith( '-summary:' ):
                wikipedia.setAction( arg[9:] )
                summary_commandline = True
            else:
                generator = genFactory.handleArg(arg)
                if generator:
                    gen = generator
    else:
        PageTitles = [raw_input(u'Page:> ').decode('utf-8')]
    if cat!='':
        facatfalist=facatlist(cat)
        if facatfalist!=False:
            run(facatfalist)    
    if PageTitles:
        pages = [wikipedia.Page(faSite,PageTitle) for PageTitle in PageTitles]
        gen = iter( pages )
    if not gen:
        wikipedia.stopme()
        sys.exit()
    if namespaces != []:
        gen = pagegenerators.NamespaceFilterPageGenerator( gen,namespaces )
    preloadingGen = pagegenerators.PreloadingGenerator( gen,pageNumber = 60 )#---number of pages that you want load at same time
    run(preloadingGen)
 
if __name__ == "__main__":
    login_fa(usernames)
    main()