#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2011
#
# Distributed under the terms of the CC-BY-SA 3.0.

import query,re,wikipedia,zz_ref_link_correction
import codecs,config,time,login
import MySQLdb as mysqldb
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
mysite='fa'
BotVersion=u'۸.۱'
_cache={}

def login_fa():    
    try:
        password_fa = open("/data/project/rezabot/pywikipedia/passfile2", 'r')
    except:
        password_fa = open("/home/reza/compat/passfile2", 'r')

    password_fa=password_fa.read().replace('"','').strip().split('(')[1].split(',')[1].split(')')[0].strip()
    botlog=login.LoginManager(password=password_fa,username='Fatranslator',site=wikipedia.getSite('fa'))
    botlog.login()

def Check_Page_Exists(page_link):
    page_link=page_link.replace(u' ',u'_')
    if _cache.get(tuple([page_link, 'Check_Page_Exists'])):
        return _cache[tuple([page_link, 'Check_Page_Exists'])]
    site = wikipedia.getSite(mysite)
    params = {
        'action': 'query',
        'prop':'info',
        'titles': page_link
    }
    query_page = query.GetData(params,site)
    try:
        for i in query_page[u'query'][u'pages']:    
            redirect_link=query_page[u'query'][u'pages'][i]['pageid']  
            _cache[tuple([page_link, 'Check_Page_Exists'])]=True
            return True# page existed
    except:
        _cache[tuple([page_link, 'Check_Page_Exists'])]=False
        return False# page not existed

def namespacefinder( enlink ,firstsite):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'') 
    enlink=enlink.replace(u' ',u'_')
    if _cache.get(tuple([enlink,firstsite, 'namespacefinder'])):
        return _cache[tuple([enlink,firstsite, 'namespacefinder'])]
    site = wikipedia.getSite(firstsite)
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': enlink,
        'redirects': 1,
        'lllimit':500,
    }
    a=1    
    if a:
        categoryname = query.GetData(params,site)
        for item in categoryname[u'query'][u'pages']:
            fanamespace=categoryname[u'query'][u'pages'][item]['ns']
        _cache[tuple([enlink,firstsite, 'namespacefinder'])]=fanamespace
        return fanamespace
    else: 
        _cache[tuple([enlink,firstsite, 'namespacefinder'])]=False
        return False

def redirect_find( page_link):
    page_link=page_link.replace(u' ',u'_')
    if _cache.get(tuple([page_link, 'redirect_find'])):
        return _cache[tuple([page_link, 'redirect_find'])]
    params = {
        'action': 'query',
        'redirects':"",
        'titles': page_link
    }
    query_page = query.GetData(params,wikipedia.getSite('en'))
    try:
        redirect_link=query_page[u'query'][u'redirects'][0]['to']
        _cache[tuple([page_link, 'redirect_find'])]=False
        return False
    except:
        if 'missing=""' in str(query_page):
            _cache[tuple([page_link, 'redirect_find'])]=False
            return False
        else:
            _cache[tuple([page_link, 'redirect_find'])]=True
            return True

def englishdictionry( enlink ,firstsite,secondsite):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(unicode(mysite,'UTF-8')+u':',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(unicode(mysite,'UTF-8')+u':',u'')
    enlink=enlink.replace(u' ',u'_')
    if _cache.get(tuple([enlink,firstsite, 'englishdictionry'])):
        return _cache[tuple([enlink,firstsite, 'englishdictionry'])]
    if enlink.find('#')!=-1:
        _cache[tuple([enlink,firstsite, 'englishdictionry'])]=False
        return False
    if enlink==u'':
        _cache[tuple([enlink,firstsite, 'englishdictionry'])]=False
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
        if result.find('#')!=-1:
            _cache[tuple([enlink,firstsite, 'englishdictionry'])]=False
            return False
        _cache[tuple([enlink,firstsite, 'englishdictionry'])]=result
        return result
    except: 
        _cache[tuple([enlink,firstsite, 'englishdictionry'])]=False
        return False

def switchnamespace(namespace):
    if namespace==0:
       return u' '
    if namespace==4:
       return u'wikipedia:'
    if namespace==10:
       return u'template:'
    if namespace==12:
       return u'help:'
    if namespace==14:
       return u'category:'
    return False

def revert(text2,text):
    Regexs=re.compile(ur'\{\{\s*(?:[Cc]ite|[Cc]itation)(?:\{\{.*?\}\}|.)*?\}\}') 
    citebase = Regexs.findall(text)
    citetarget = Regexs.findall(text2)
    i=-1
    for m in citebase:
           i+=1
           text2=text2.replace(citetarget[i],citebase[i])
    return text2

def getlinks(enlink,falink,first,mysite):
        site = wikipedia.getSite(mysite)
        enlink_2=re.sub(ur'[1234567890۱۲۳۴۵۶۷۸۹۰\(\)\,\،\.]',ur'', enlink).strip()
        falink_2=re.sub(ur'[1234567890۱۲۳۴۵۶۷۸۹۰\(\)\,\،\.]',ur'', falink).strip()
        if not enlink_2:
            return
        if not falink_2:
            return
        try:
            page = wikipedia.Page(site,enlink)
            linktos=page.getReferences()
        except:
            return False
        for page in linktos:
                namespacefa=page.namespace()
                if namespacefa==1 or namespacefa==2 or namespacefa==3 or namespacefa==5 or namespacefa==7 or namespacefa==8 or namespacefa==9 or namespacefa==11 or namespacefa==13 or namespacefa==15 or namespacefa==101:
                        continue
                if first:
                    if namespacefa==0:    
                        continue
                try:
                    text=page.get()
                except :
                    continue
                if _cache.get(tuple([page.title(),enlink,'getlinks'])):
                    continue
                else:
                    _cache[tuple([page.title(),enlink,'getlinks'])]=1
                time.sleep(2)    
                wikipedia.output(u'checking '+page.title()+u' .....')    
                enlink=enlink.strip()
                text2=text
                fanum=enlink.replace(u'1',u'۱').replace(u'2',u'۲').replace(u'3',u'۳').replace(u'4',u'۴').replace(u'5',u'۵')
                fanum=fanum.replace(u'6',u'۶').replace(u'7',u'۷').replace(u'8',u'۸').replace(u'9',u'۹').replace(u'0',u'۰')    
                fanum_text=re.sub(ur'[1234567890۱۲۳۴۵۶۷۸۹۰\(\)\,\،\.]',ur'', fanum).strip()

                if  fanum_text and fanum!=enlink:
                    search_list=[enlink,enlink.lower(),enlink.upper(),enlink.replace(u',',u'،')]
                else:
                    search_list=[enlink,enlink.lower(),enlink.upper(),enlink.replace(u',',u'،'),fanum]

                if text.find(enlink)!=-1:   
                    for enlink in search_list:     
                        text2=text2.replace(u'[['+enlink+u']]',u'[['+falink+u']]').replace(u'[['+enlink+u'|',u'[['+falink+u'|').replace(u'\r',u'')
                        text2=text2.replace(u'[[ '+enlink+u']]',u'[['+falink+u']]').replace(u'[[ '+enlink+u'|',u'[['+falink+u'|')
                        text2=text2.replace(u'[[ '+enlink+u' ]]',u'[['+falink+u']]').replace(u'[[ '+enlink+u' |',u'[['+falink+u'|')
                        text2=text2.replace(u'[['+enlink+u' ]]',u'[['+falink+u']]').replace(u'[['+enlink+u' |',u'[['+falink+u'|')
                        text2=text2.replace(u'[[  '+enlink+u' ]]',u'[['+falink+u']]').replace(u'[[  '+enlink+u' |',u'[['+falink+u'|')
                        #-------------------------------------------for cats-----------------------------------
                        text2=text2.replace(u'[[:'+enlink+u']]',u'[[:'+falink+u']]').replace(u'[[:'+enlink+u'|',u'[[:'+falink+u'|')
                        text2=text2.replace(u'[[: '+enlink+u']]',u'[[:'+falink+u']]').replace(u'[[: '+enlink+u'|',u'[[:'+falink+u'|')
                        text2=text2.replace(u'[[: '+enlink+u' ]]',u'[[:'+falink+u']]').replace(u'[[: '+enlink+u' |',u'[[:'+falink+u'|')
                        text2=text2.replace(u'[[:'+enlink+u' ]]',u'[[:'+falink+u']]').replace(u'[[:'+enlink+u' |',u'[[:'+falink+u'|')
                        text2=text2.replace(u'[[ :'+enlink+u' ]]',u'[[:'+falink+u']]').replace(u'[[ :'+enlink+u' |',u'[[:'+falink+u'|')
                        text2=text2.replace(u'[[ : '+enlink+u' ]]',u'[[:'+falink+u']]').replace(u'[[ : '+enlink+u' |',u'[[:'+falink+u'|')
                    #if string.count(text2,enlink)==1 and text2.find(enlink+u'#')==-1:    
                        #text2=text2.replace(enlink,falink,1)        
                    if text2.find(falink)==-1:
                        wikipedia.output(u'\03{lightblue}could not find any link\03{default}')
                    text2=revert(text2,text)
                    msg=u''
                    if text!=text2:
                        text2,msg=zz_ref_link_correction.main(text2,u'')
                        if msg:
                           msg=u'+'+msg
                        try:
                            page.put(text2,u'ربات :جایگزینی پیوند قرمز [['+enlink+u']] > [['+falink+u']] ('+BotVersion+')'+msg)
                            wikipedia.output(u'\03{lightgreen}the page '+page.title()+u' had replcae item [['+enlink+u']] > [['+falink+u']]\03{default}')
                        except:
                            wikipedia.output(u'\03{lightred}the page '+page.title()+u' could not replaced so it passed\03{default}')
                            continue
                else:
                     wikipedia.output(u'\03{lightred}could not find andy link\03{default}')        
        return True
login_fa()
#------------------------------------------------------------ sql part
querys='SELECT /* SLOW_OK */ DISTINCT pl_title,pl_namespace FROM pagelinks INNER JOIN page ON pl_from = page_id WHERE pl_title NOT IN(SELECT page_title FROM page WHERE page_namespace = 0) AND pl_namespace = 0 AND page_namespace = 0;'
wikipedia.output(querys)
site  = wikipedia.getSite(mysite)
conn = mysqldb.connect(mysite+"wiki.labsdb", db = site.dbName(),
                       user = config.db_username,
                       passwd = config.db_password)
cursor = conn.cursor()
cursor.execute(querys)
results = cursor.fetchall()
#------------------------------sql finsh------------------
#++++++++++++++++++++++

our_text=u'\n'
for i in results:
    our_text+=switchnamespace(i[1])+unicode(i[0],'UTF-8')+u'\n'

with codecs.open('zzredlinks.txt' ,mode = 'w',encoding = 'utf8' ) as f:
    f.write(our_text)
del f,conn,cursor,our_text

#+++++++++++++++++++++++

#results=[['Shiraz, Iran',0],['Book',0],['book',0]]
for enlink in results:
    if switchnamespace(enlink[1]):    
        enlink=switchnamespace(enlink[1])+unicode(enlink[0],'UTF-8').strip()
        enlink=enlink.replace(u'_',u' ').strip()
        enlink2=re.sub(u'[ابضصثقفغعهخحجچشسیلتنمکگظطزرذدپو]',ur'', enlink)
        if enlink2==enlink:
            count=-1
            for i in u'۰۱۲۳۴۵۶۷۸۹':
                count+=1
                enlink=enlink.replace(i,str(count))
            #if not redirect_find( enlink):
            #   wikipedia.output(u'it was redirect so aborted!')    
            #   continue
            falink=englishdictionry( enlink ,'en',mysite)
            if falink:
                if namespacefinder( enlink ,'en')!=namespacefinder( falink ,'fa'):
                    continue    
                wikipedia.output(u'---------------------------------------------')
                wikipedia.output(enlink+u' > '+falink)
                a=getlinks(enlink,falink,True,mysite)
del results,enlink
#------------------------------------------------------------ sql part    
querys='SELECT /* SLOW_OK */ DISTINCT pl_title,pl_namespace FROM pagelinks INNER JOIN page ON pl_from = page_id WHERE pl_title NOT IN(SELECT page_title FROM page WHERE page_namespace = 0) AND pl_namespace = 0 AND page_namespace = 0;'
wikipedia.output(querys)
site  = wikipedia.getSite(mysite)
conn = mysqldb.connect(mysite+"wiki.labsdb", db = site.dbName(),
                       user = config.db_username,
                       passwd = config.db_password)
cursor = conn.cursor()
cursor.execute(querys)
results = cursor.fetchall()
#------------------------------sql finsh------------------
#+++++++++++++++++++++++
our_text=u'\n'
for i in results:
    our_text+=switchnamespace(i[1])+unicode(i[0],'UTF-8')+u'\n'

with codecs.open('zzredlinks.txt' ,mode = 'w',encoding = 'utf8' ) as f:
    f.write(our_text)
del f,conn,cursor,our_text
#+++++++++++++++++++++++

#---------------------------------for checking articles after while !!-----------------------------------------
for enlink in results:
    if switchnamespace(enlink[1]):
        enlink=switchnamespace(enlink[1])+unicode(enlink[0],'UTF-8').strip()
        enlink=enlink.replace(u'_',u' ').strip()  
        enlink2=re.sub(u'[ابضصثقفغعهخحجچشسیلتنمکگظطزرذدپو]',ur'', enlink)
        if enlink2==enlink:
            count=-1
            for i in u'۰۱۲۳۴۵۶۷۸۹':
                count+=1
                enlink=enlink.replace(i,str(count))
            #if not redirect_find( enlink):
            #    continue 
            falink=englishdictionry( enlink ,'en',mysite)
            if falink:
                if namespacefinder( enlink ,'en')!=namespacefinder( falink ,'fa'):
                    continue  
                wikipedia.output(u'---------------------------------------------')
                wikipedia.output(enlink+u' > '+falink)
                a=getlinks(enlink,falink,False,mysite)