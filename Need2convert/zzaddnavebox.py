#!/usr/bin/python
# Reza (User:reza1615)
# -*- coding: utf-8 -*-
import fa_cosmetic_changes,re,query,sys
import wikipedia, pagegenerators,login
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
fasite = wikipedia.getSite('fa','wikipedia')
_cache={}
usernames=u'Fatranslator'
def login_fa(usernames):    
    try:
        password_fa = open("/data/project/rezabot/pywikipedia/passfile2", 'r')
    except:
        password_fa = open("/home/reza/compat/passfile2", 'r')

    password_fa=password_fa.read().replace('"','').strip()
    passwords=password_fa.split('(')[1].split(',')[1].split(')')[0].strip()
    #-------------------------------------------
    botlog=login.LoginManager(password=passwords,username=usernames,site=fasite)
    botlog.login()

def solve_redirect(tem,fapage,fapage_redi,delink):
    tem = wikipedia.Page(fasite,tem.title())  
    try:
        text=tem.get()
        text=text.replace(u'[[ ',u'[[').replace(u' ]]',u']]').replace(u' |',u'|').replace(u'[['+fapage.title()+u']]',u'[['+fapage_redi.title()+u'|'+fapage.title()+u']]')
        text=text.replace(u'[['+fapage.title()+u'|',u'[['+fapage_redi.title()+u'|')
        tem.put(text,u'ربات:اصلاح تغییرمسیر')
        wikipedia.output(u'\03{lightyellow}اصلاح تغیرمسیر درون الگو\03{default}')        
    except:
        pass
def link_filtering(tem_text,links):
    mytext=u'\n'
    tem_text_f=tem_text.replace(u'\r',u'')
    our_test_text=re.sub(ur'\{\{[Nn]ational.*?squad',u'',tem_text_f)
    if our_test_text!=tem_text_f:
        for i in tem_text_f.split(u'\n|'):
            if i.find(u'p1')==-1 and i.find(u'p2')==-1 and i.find(u'p3')==-1 and i.find(u'p4')==-1 and i.find(u'p5')==-1 and i.find(u'p6')==-1 and i.find(u'p7')==-1 and i.find(u'p8')==-1 and i.find(u'p9')==-1 and i.find(u'p0')==-1 and i.find(u'coach')==-1:
                wikipedia.output(i)
                mytext+=i
    else:
        for i in tem_text_f.split(u'\n|'):
            if i.find(u'list1')==-1 and i.find(u'list2')==-1 and i.find(u'list3')==-1 and i.find(u'list4')==-1 and i.find(u'list5')==-1 and i.find(u'list6')==-1 and i.find(u'list7')==-1 and i.find(u'list8')==-1 and i.find(u'list9')==-1 and i.find(u'list0')==-1 and i.find(u'فهرست۰')==-1 and i.find(u'فهرست۹')==-1 and i.find(u'فهرست۸')==-1 and i.find(u'فهرست۷')==-1 and i.find(u'فهرست۶')==-1 and i.find(u'فهرست۵')==-1 and i.find(u'فهرست۴')==-1 and i.find(u'فهرست۳')==-1 and i.find(u'فهرست۲')==-1 and i.find(u'فهرست۱')==-1:
                wikipedia.output(i)
                mytext+=i    
    black_text=u' '
    dict={u'<noinclude>':u'</noinclude>',u'{{یادکرد':u'}}',u'<ref':u'</ref',u'{{cite':u'}}',u'{{Cite':u'}}'}
    for a in dict:
        count=0
        for i in mytext.split(a):
            count+=1
            if count>1:
               black_text+=i.split(dict[a])[0]
    black_links = re.findall(ur'\[\[.*?\]\]',black_text+mytext, re.S)
    black_links2=[]
    for i in black_links:
        black_links2.append(i.replace(u']]',u'').replace(u'[[',u'').strip().split(u'|')[0])
    new_links,delink=[],[]
    for i in links:    
        if (i.title() in black_links2) or (i.title() in new_links) or i.namespace()!=0:    
            continue
        else:  
            itest=i.title().split(u'|')[0]
            if i.title()==u'آذرشهر':    
                new_links.append(i)
                continue
            for b in u'۱۲۳۴۵۶۷۸۹۰1234567890':
                itest=itest.replace(b,u'')
            for b in [u'کاپیتان (فوتبال)',u'استان',u'دهستان',u'کشور',u'شهر',u'شهرستان',u'بخش',u'فروردین',u'اردیبهشت',u'خرداد',u'تیر',u'مرداد',u'شهریور',u'مهر',u'آبان',u'آذر',u'دی',u'بهمن',u'اسفند',u'ژانویه',u'فوریه',u'مارس',u'ژوئیه',u'ژوئن',u'آوریل',u'اوت',u'سپتامبر',u'نوامبر',u'دسامبر',u'می',u'اکتبر']:
                itest=itest.replace(b,u'')
            itest=itest.replace(u'(میلادی)',u'').replace(u'(قمری)',u'').replace(u'(پیش از میلاد)',u'').replace(u'(قبل از میلاد)',u'').strip()
            if itest==u'' or itest==u' ':
                delink.append(i.title())
            else:
                new_links.append(i)
    for i in new_links:
        wikipedia.output(i.title())
    return new_links,delink
 
def addtext (fapage,text,addtemplate,msg_clean):
                if text.find(u'{{ابهام‌زدایی}}')!=-1:
                    return
                text=text.replace(addtemplate+u'\n',u'')
                if text.find(u'رده:')!=-1:    
                    num=text.find(u'[[رده:')
                    text=text[:num]+addtemplate+u'\n'+text[num:]
                else:
                    m = re.search(ur'\[\[([a-z]{2,3}|[a-z]{2,3}\-[a-z\-]{2,}|simple):.*?\]\]', text)
                    if m:
                        if m.group(0)==u'[[en:Article]]':    
                            try:
                                if string.count(text,u'[[en:Article]] --->')==1:    
                                    text=text.split(u'[[en:Article]] --->')[0]+u'[[en:Article]] --->\n'+addtemplate+text.split(u'[[en:Article]] --->')[1]
                                else:
                                    if fapage.namespace()!=0:
                                        return    
                                    text+='\n'+addtemplate                                
                            except:
                                if fapage.namespace()!=0:
                                    return
                                text+='\n'+addtemplate
                        else:
                            num=text.find(m.group(0))
                            text=text[:num]+addtemplate+'\n'+text[num:]
                    else:
                        if fapage.namespace()!=0:    
                            return                        
                        text+='\n'+addtemplate
                text,cleaning_version,msg_clean2=fa_cosmetic_changes.fa_cosmetic_changes(text,fapage)
                try:                
                    fapage.put(text,u'ربات:افزودن الگو ناوباکس '+addtemplate+msg_clean)
                except:
                    pass    
                return
def templatequery(enlink):
    temps=[]
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.split(u'#')[0].strip()
    enlink=enlink.replace(u' ',u'_')
    if _cache.get(tuple([enlink, 'templatequery'])):
        return _cache[tuple([enlink, 'templatequery'])]
    if enlink==u'':
        _cache[tuple([enlink, 'templatequery'])]=False
        return False    

    params = {
            'action': 'query',
            'prop':'templates',
            'titles': enlink,
            'redirects': 1,
            'tllimit':500,
    }
 
    try:
        categoryname = query.GetData(params,fasite)
        for item in categoryname[u'query'][u'pages']:
            templateha=categoryname[u'query'][u'pages'][item][u'templates']
            break
        for temp in templateha:
            temps.append(temp[u'title'].replace(u'_',u' ').replace(u'الگو:',u'').replace(u'template:',u'').strip())  
        _cache[tuple([enlink, 'templatequery'])]=temps
        return temps
    except: 
        _cache[tuple([enlink, 'templatequery'])]=False
        return False


def check_user_edits(username):
    username=username.replace(u' ',u'_')
    if _cache.get(tuple([username, 'check_user_edits'])):
        return _cache[tuple([username, 'check_user_edits'])]
    params = {
        'action': 'query',
        'list': 'users',
        'ususers': username,
        'usprop':'editcount'    
    }
    try:
        usernamequery = query.GetData(params,fasite)
        if usernamequery[u'query'][u'users'][0][u'editcount']>1000:
            _cache[tuple([username, 'check_user_edits'])]=True
            return True
        else:
            _cache[tuple([username, 'check_user_edits'])]=False
            return False
    except:
        _cache[tuple([username, 'check_user_edits'])]=False
        return False    


def check_user(fapage):
    First_user=''
    try:
        text=fapage.get()
        page_history=fapage.getVersionHistory()
        First_user=page_history[-1][2]
        if check_user_edits(First_user):
            return True,First_user
        else:
            return False,First_user
    except:
        return False,First_user

def add_nav(preloadingGen):
    for tem in preloadingGen:
        user_pass,First_user=check_user(tem)
        if not user_pass:
            wikipedia.output(u'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            wikipedia.output("\03{lightgreen}Template creator does not have more than 1000 edits! so it is passed\03{default}")
            wikipedia.output(u'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            continue
        else:
            wikipedia.output(u'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++') 
            wikipedia.output(u"\03{lightgreen}User:"+First_user+u"\03{default} and s/he has more than\03{lightgreen} 1000\03{default} edits so it is ok!")
            wikipedia.output(u'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        passport=True
        enchar=u'qwertyuiopasdfghjklzxcvbnm'
        for i in enchar:
            if tem.title().replace(u'الگو:',u'').replace(u'template:',u'').replace(u'Template:',u'').find(i)!=-1:
                passport=False
                break
        if not passport:
            continue
        if tem.title().find(u'/')!=-1 or tem.title().find(u'\\')!=-1:
            continue  
        try:
            tem_text=tem.get()
        except:
            continue
        tem_text=tem_text.replace(u'{{ ',u'{{').replace(u'{{ ',u'{{').replace(u'{{الگو:',u'{{').replace(u'{{Template:',u'{{').replace(u'{{template:',u'{{')
        TempTemplates=templatequery(tem.title())
        if not TempTemplates:
            continue
        if not u'Navbox' in TempTemplates:
            continue
        #if tem_text.find(u'{{جعبه گشتن')==-1 and tem_text.find(u'{{navbox')==-1 and tem_text.find(u'{{Navbox')==-1 and tem_text.find(u'{{National squad')==-1 and tem_text.find(u'{{national squad')==-1:
        #    continue
        wikipedia.output(tem)
        added_template=tem.title().replace(u'الگو:',u'').replace(u'template:',u'').replace(u'Template:',u'')
        if tem.namespace()!=10:
            continue
        redirects=tem.getReferences(redirectsOnly=True)
        redirect_list=[]
        for i in redirects:
            redirect_list.append(i.title().replace(u'الگو:',u'').replace(u'template:',u'').replace(u'Template:',u''))
        links=tem.linkedPages()
        links,delink=link_filtering(tem_text,links)
        wikipedia.output(u'-----------------------------------------')    
        old_tem_text=tem_text
        for nonlink in delink:
            tem_text=tem_text.replace(u'[['+nonlink+u']]',nonlink.split(u'|')[0])
        if old_tem_text!=tem_text:
            wikipedia.output(u'\03{lightred}delinking\03{default}')
            tem.put(tem_text,u'ربات:برداشتن پیوندهای نالازم')
        for fapage in links:
            try:
                text=fapage.get()
            except wikipedia.IsRedirectPage:
                fapage_redi = fapage.getRedirectTarget()
                try:
                    text=fapage_redi.get()
                    solve_redirect(tem,fapage,fapage_redi)
                    fapage=fapage_redi
                except:
                    continue
            except:
                wikipedia.output(u'\03{lightred}link was red\03{default}')
                continue
            wikipedia.output(u'\03{lightblue}--'+fapage.title()+u'---------\03{default}')
            msg=u' '
            text,cleaning_version,msg_clean=fa_cosmetic_changes.fa_cosmetic_changes(text,fapage,msg)
            old_text=text
            for i in redirect_list: 
                text=text.replace(u'{{'+i+u'}}',u'{{'+added_template+u'}}').replace(u'{{'+i+u'|',u'{{'+added_template+u'|')
            fatemplates=templatequery(fapage.title())
            text=text.replace(u'{{ ',u'{{').replace(u' }}',u'}}').replace(u'{{الگو:',u'{{').strip()
            if not fatemplates:
                continue
            if text.find(u'{{'+added_template+u'}}')==-1 and (not added_template in fatemplates):
               addtemplate=u'{{'+added_template+u'}}'
               addtext (fapage,text,addtemplate,msg_clean)
               wikipedia.output(u'added= {{\03{lightpurple}'+added_template+u'\03{default}}}')    
               continue
 
            if old_text!=text:
                try:
                    fapage.put(text,u'ربات:اصلاح تغییرمسیر ناوباکس‌')
                    wikipedia.output(u'\03{lightpurple}ربات:اصلاح تغییرمسیر ناوباکس\03{default}')
                except:
                    pass    
                continue
 
def main():    
    gen = None
    genFactory = pagegenerators.GeneratorFactory()    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-newtem'):    
            arg=arg.replace(':','')
            if len(arg) == 7:
                genfa = pagegenerators.NewpagesPageGenerator(100, False, None,10)
            else:
                genfa = pagegenerators.NewpagesPageGenerator(int(arg[8:]), False, None,10)
            gen = pagegenerators.PreloadingGenerator( genfa,60)
        else:
            gen = genFactory.handleArg( arg )    
 
    if not gen:
        wikipedia.stopme()
        sys.exit()
    preloadingGen = pagegenerators.PreloadingGenerator(gen,pageNumber = 60)    
    #preloadingGen = pagegenerators.NamespaceFilterPageGenerator(gen,10)
    add_nav(preloadingGen)
if __name__ == "__main__":
    login_fa(usernames)
    main()
