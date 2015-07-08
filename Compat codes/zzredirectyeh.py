#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2011
#
# Distributed under the terms of the CC-BY-SA 3.0 .
#!/usr/bin/python
# -*- coding: utf-8  -*-

import sys, re, codecs,os
import wikipedia, pagegenerators
import config,login,query
import MySQLdb as mysqldb
from datetime import timedelta,datetime
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
fasite = wikipedia.getSite('fa','wikipedia')
#---------------------------------------------------------
bot_address=u'/data/project/rezabot/pywikipedia/'
my_password=''
my_username='fawikibot'
#---------------------------------------------------------
botVersion=u'۶.۰'
_cache={}

def get_cache():
    try:
        import _cache_redirect
        return _cache_redirect._cache,_cache_redirect.last_timestamp
    except:
        return {},0

def put_cache(my_cache,last_timestamp):
    with codecs.open('_cache_redirect.py' ,mode = 'w',encoding = 'utf8' ) as f:
        f.write(u'_cache='+str(my_cache)+u'\nlast_timestamp='+str(last_timestamp))

def login_fa(my_password): 
    if not my_password:   
        try:
            password_fa = open("/data/project/rezabot/pywikipedia/passfile2", 'r')
        except:
            password_fa = open("/home/reza/compat/passfile2", 'r')
        my_password=password_fa.read().replace('"','').strip().split('(')[1].split(',')[1].split(')')[0].strip()
    botlog=login.LoginManager(password=my_password,username=my_username,site=wikipedia.getSite('fa'))
    botlog.login()

def redirect_find(falink):
    try:
        falink=unicode(str(falink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        falink=falink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'') 
    falink=falink.replace(u' ',u'_')
    if _cache.get(tuple([falink, 'redirect_find'])):
        return _cache[tuple([falink, 'redirect_find'])]
    params = {
        'action': 'query',
        'prop': 'info',
        'titles': falink
    }
    categoryname = query.GetData(params,fasite)
    try:
            fanamespace=categoryname[u'query'][u'pages'][0]['redirect']
            wikipedia.output(u'it is redirect')  
            _cache[tuple([falink, 'redirect_find'])]=True
            return True
    except:
            _cache[tuple([falink, 'redirect_find'])]=False
            return False
def get_query():
        wikipedia.output(u'----get Query of page title ---')
        os.system(u'sql fawiki "SELECT page_title FROM page WHERE page_namespace = 0;" >'+bot_address+u'list_of_article_title.txt')
        text = codecs.open( bot_address+u'list_of_article_title.txt','r' ,'utf8' )
        text = text.read()
        text=text.replace(u'_',u' ').replace(u'\r',u'')
        wikipedia.output(u'----Query id Done ---')
        return text

def creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg):
    New_redirect_name=New_redirect_name.replace(u'  ',u' ')
    if New_redirect_name.strip() and pagetitle_source.strip() and msg.strip():
        wikipedia.output(u'--------------------'+pagetitle_source+u'----------------------')
        wikipedia.output(u'Source Tilte is ='+pagetitle_source)
        wikipedia.output(u'\03{lightgreen}Redirect Tilte is ='+New_redirect_name+u'\03{default}')
        if New_redirect_name!=pagetitle_source:
            New_redirect_page= wikipedia.Page(fasite,New_redirect_name)
            New_redirect_page.put(u"#تغییرمسیر [["+pagetitle_source+u"]]",msg)
            fa_page_title_list+=u'\n'+New_redirect_name.strip()+u'\n'
        else:
            wikipedia.output(u'\03{lightred}Redirect and Target are the same\03{default}')
    return fa_page_title_list

def add_text(generator):
    fa_page_title_list=get_query()
    for page in generator:
        if _cache.get(tuple([page.title(), 'add_text'])):
            wikipedia.output(u'\03{lightred}>>> Page '+page.title()+u' was checked before so it will pass\03{default}')
            continue
        original_text=u''
        if page.namespace()!=0:    
            continue
        try:
            pagetitle_source=page.title()
            original_text = page.get()
            pagetitle= pagetitle_source
            redirection=0
        except wikipedia.NoPage:
            wikipedia.output(u"%s doesn't exist, skip!" % page.title())
            continue
            
        except wikipedia.IsRedirectPage:
            wikipedia.output(u"%s is a redirect, skip!" % page.title())    
            pagemain=page.getRedirectTarget()
            try:
                original_text=pagemain.get()
            except:
                wikipedia.output(u"%s doesn't exist, skip!" % pagemain.title())
                continue
            pagetitle_source=pagemain.title()    
            pagetitle= page.title()
            redirection=1
        except:
            continue

        pagetitle3=re.sub(ur'[qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM]', ur"",pagetitle)
        if pagetitle3!=pagetitle:
           continue

        if pagetitle.find(u'در حال ویرایش')!=-1:
            continue
        _cache[tuple([page.title(), 'add_text'])]=1
        if original_text:
            if redirection==0:
                wrong_words=ur'ًٌٍَُِّْٔ'+u'يٰك'+u"@#$%^&*'‍‍~`"
                pagetitle2=re.sub(ur'['+wrong_words+ur']', ur"",pagetitle)
                passp=redirect_find(pagetitle)
                if not passp:
                    if pagetitle!=pagetitle2:
                        for vowel in wrong_words:
                            if vowel in pagetitle:
                                break
                        passport=False
                        text=u'{| class="wikitable plainlinks"\n|-\n'
                        page = wikipedia.Page(fasite,u"user:fawikibot/movearticles2")
                        text_fa=page.get()
                        if not pagetitle in text_fa:
                                text+=u"|[["+pagetitle+u"]] ||«"+vowel+u"»\n|-\n"
                                passport=True
                        text+=u'\n|}\n'
                        if passport:
                            page.put(text_fa+u'\n'+text,u"ربات:مقاله‌ها برای انتقال")
            try:
                #-------------------------1----------------------------------
                if u"ی" in pagetitle or u"ک" in pagetitle:
                    if not u"‌" in pagetitle:    
                        New_redirect_name=pagetitle.replace(u"ی",u"ي").replace(u"ک",u"ك")                       
                        if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                            msg=u"ربات:تغییرمسیر از ی و ک عربی به ی و ک فارسی ("+botVersion+u")"
                            fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                    else:
                        New_redirect_name=pagetitle.replace(u"ی",u"ي").replace(u"ک",u"ك").replace(u"‌",u" ")
                        if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                            msg=u"ربات:تغییرمسیر از ی و ک عربی به ی و ک فارسی و فاصله به فاصلهٔ مجازی ("+botVersion+u")"
                            fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------2----------------------------------
                if u"‌" in pagetitle:
                    New_redirect_name=pagetitle.replace(u"‌",u" ")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                            msg=u"ربات:تغییرمسیر از فاصله به فاصلهٔ مجازی ("+botVersion+u")"
                            fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------3----------------------------------
                if u"آ" in pagetitle:
                    New_redirect_name=pagetitle.replace(u"آ",u"ا")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر از ا به آ ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------3----------------------------------
                if u"أ" in pagetitle:
                    New_redirect_name=pagetitle.replace(u"أ",u"ا")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر از ا به أ ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)               
                #-------------------------3.5----------------------------------
                if u"ء" in pagetitle:
                    New_redirect_name=pagetitle.replace(u"ء",u"")    
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر از ء به  ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------3.5----------------------------------
                if (u"," or u"،" or u"(" )in pagetitle:
                    New_redirect_name=pagetitle.replace(u",",u" ").replace(u"،",u" ").replace(u")",u" ").replace(u"(",u" ").replace(u"  ",u" ").strip()
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر از ,()، به  ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------3.5----------------------------------
                if (u"(" or u"،" or u",") in pagetitle:
                    New_redirect_name=pagetitle.replace(u" ،",u"،").replace(u" ,",u",").replace(u"،",u"، ").replace(u",",u", ").replace(u"(",u" (").replace(u")",u") ").replace(u"  ",u" ").strip()
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر فاصله برای سجاوندی ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------3.5----------------------------------
                if u"ة" in pagetitle:
                    New_redirect_name=pagetitle.replace(u"ة",u"ه")    
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر از  ه به ة ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)   
                #-------------------------4----------------------------------
                if u"،" in pagetitle:
                    New_redirect_name=pagetitle.replace(u" ،",u"،")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر سجاوندی درست  برای ویرگول("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------5----------------------------------
                if u"," in pagetitle:    
                    New_redirect_name=pagetitle.replace(u",",u"،")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر سجاوندی درست برای ویرگول غیرفارسی ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------5.5----------------------------------
                b=-1
                sources=[u'اول',u'یکم',u'ثانی',u'ثالث',u'نخستین',u'اولین']
                targets=[u'یکم',u'اول',u'دوم',u'سوم',u'اولین',u'نخستین']
                for i in sources:
                    b+=1
                    j=targets[b]
                    if i in pagetitle:    
                        New_redirect_name=(u' '+pagetitle+u' ').replace(u' '+i+u' ',u' '+j+u' ').strip()
                        if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                            msg=u"ربات:تغییرمسیر از "+j+u" به "+i+u" ("+botVersion+u")"
                            fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------6----------------------------------
                if u"ؤ" in pagetitle:    
                    New_redirect_name=pagetitle.replace(u"ؤ",u"و")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر و به ؤ ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)                      
                #-------------------------6----------------------------------
                if u"کامپیوتر" in pagetitle:    
                    New_redirect_name=pagetitle.replace(u"کامپیوترها",u"رایانه‌ها").replace(u"کامپیوتری",u"رایانه‌ای").replace(u"کامپیوتر",u"رایانه")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر رایانه به کامپیوتر ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------7----------------------------------
                if u"ه‌ی" in pagetitle:    
                    New_redirect_name=pagetitle.replace(u"ه‌ی",u"ه")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر  ه‌ به ه‌ی ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------8----------------------------------
                if u"ه " in pagetitle and redirection==0 and pagetitle.find(u'كه ')==-1 and pagetitle.find(u'اه ')==-1 and pagetitle.find(u'ه اي ')==-1 and pagetitle.find(u'ه ای ')==-1 and pagetitle.find(u'که ')==-1 and pagetitle.find(u'راه ')==-1 and pagetitle.find(u'ه با ')==-1 and pagetitle.find(u'گروه ')==-1 and pagetitle.find(u'ه که ')==-1 and pagetitle.find(u'ه كه ')==-1 and pagetitle.find(u'ه در ')==-1 and pagetitle.find(u'ه براي ')==-1 and pagetitle.find(u'ه برای ')==-1 and pagetitle.find(u'ه از ')==-1 and pagetitle.find(u'ه ;')==-1 and pagetitle.find(u'علیه ')==-1 and pagetitle.find(u'عليه ')==-1 and pagetitle.find(u'ه و ')==-1 and pagetitle.find(u'ه :')==-1 and pagetitle.find(u'شاه ')==-1 and pagetitle.find(u'به ')==-1 and pagetitle.find(u'الله ')==-1 and pagetitle.find(u'ه (')==-1 and  pagetitle.find(u'گه ')==-1 and pagetitle.find(u'ه -')==-1 and pagetitle.find(u'ه-')==-1:
                    New_redirect_name=pagetitle.replace(u"ه ",u"هٔ ")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر  هٔ به ه ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------9----------------------------------
                if u"‌ها " in pagetitle and redirection==0 and pagetitle.find(u'ها (')==-1  and pagetitle.find(u'ها براي ')==-1 and pagetitle.find(u'ها برای ')==-1 and pagetitle.find(u'ها با ')==-1 and pagetitle.find(u'ها در ')==-1 and pagetitle.find(u'ها از ')==-1 and pagetitle.find(u'ها كه ')==-1 and pagetitle.find(u'ها که ')==-1 and pagetitle.find(u'ها و ')==-1 and pagetitle.find(u'ها :')==-1 and pagetitle.find(u'ها ;')==-1:
                    New_redirect_name=pagetitle.replace(u"ها ",u"های ")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر های به ها ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------10----------------------------------
                if u"‌‌ها" in pagetitle:
                    New_redirect_name=pagetitle.replace(u"‌ها",u"ها")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر فاصلهٔ مجازی+ها به ها ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------10.5----------------------------------
                if u"‌‌ها" in pagetitle:
                    New_redirect_name=pagetitle.replace(u"‌ها",u" ها")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر فاصلهٔ مجازی+ها به فاصله+ها ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------11----------------------------------
                if  u"‌‌می‌" in pagetitle  or  u"‌‌مي" in pagetitle :
                    New_redirect_name=pagetitle.replace(u"می‌",u"می").replace(u"مي‌‌",u"مي")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر می+فاصلهٔ مجازی به می ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------12----------------------------------
                farsinum=[u'۰',u'۱',u'۲',u'۳',u'۴',u'۵',u'۶',u'۷',u'۸',u'۹']
                counters=-1
                pagetitle2=pagetitle
                for num in farsinum:    
                    counters+=1    
                    pagetitle2=pagetitle2.replace(num,str(counters))
                if pagetitle2!=pagetitle:
                        if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                            msg=u"ربات:تغییرمسیر عدد لاتین به عدد فارسی ("+botVersion+u")"
                            fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                #-------------------------13----------------------------------
                if u"ایالات متحده آمریکا" in pagetitle:
                    New_redirect_name=pagetitle.replace(u"ایالات متحده آمریکا",u"ایالات متحده")
                    if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                        msg=u"ربات:تغییرمسیر ("+botVersion+u")"
                        fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                elif u"آمریکا" in pagetitle :
                    if not u"آمریکایی" in pagetitle:
                        New_redirect_name=pagetitle.replace(u"آمریکا",u"ایالات متحده")
                        if fa_page_title_list.find(u'\n'+New_redirect_name.strip()+u'\n')==-1:
                            msg=u"ربات:تغییرمسیر ("+botVersion+u")"
                            fa_page_title_list=creat_redirect(fa_page_title_list,New_redirect_name,pagetitle_source,msg)
                pagetitle_source,New_redirect_name,msg=u'',u'',u''
            except:
                continue    
def main():
    summary_commandline,gen,template = None,None,None
    namespaces,PageTitles,exceptions = [],[],[]    
    encat=''
    autoText,autoTitle = False,False
    recentcat,newcat=False,False
    genFactory = pagegenerators.GeneratorFactory()
    for arg in wikipedia.handleArgs():
        if arg == '-autotitle':
            autoTitle = True
        elif arg == '-autotext':
            autoText = True
        elif arg.startswith( '-except:' ):
            exceptions.append( arg[8:] )
            
        elif arg.startswith('-start'):
            firstPageTitle = arg[7:]
            if not firstPageTitle:
                firstPageTitle = wikipedia.input(
                    u'At which page do you want to start?')
            firstPageTitle = wikipedia.Page(fasite,firstPageTitle).title(withNamespace=False)
            gen = pagegenerators.AllpagesPageGenerator(firstPageTitle, 0,
                                        includeredirects=True)    
        elif arg.startswith( '-template:' ):
            template = arg[10:]
        elif arg.startswith( '-namespace:' ):
            namespaces.append( int( arg[11:] ) )
        elif arg.startswith( '-summary:' ):
            wikipedia.setAction( arg[9:] )
            summary_commandline = True
        else:
            generator = genFactory.handleArg( arg )
            if generator:
                gen = generator
    if not gen:
        wikipedia.stopme()
        sys.exit()
    if namespaces != []:
        gen = pagegenerators.PreloadingGenerator(gen,pageNumber = 60)    
        preloadingGen = pagegenerators.NamespaceFilterPageGenerator( gen,namespaces )
    else:
         preloadingGen = pagegenerators.PreloadingGenerator(gen,pageNumber = 60)
    _cache,last_timestamp=get_cache()
    add_text(preloadingGen)

    now = str(datetime.now())
    todaynum=int(now.split('-')[2].split(' ')[0])+int(now.split('-')[1])*30+(int(now.split('-')[0])-2000)*365

    if last_timestamp+3 < todaynum:
        put_cache(_cache,todaynum)
    else:
        put_cache({},0)
if __name__ == "__main__":
        login_fa(my_password)
        main()