#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2014
#
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
import pywikibot,re,codecs
from pywikibot.compat import query
pywikibot.config.put_throttle = 0
pywikibot.config.maxthrottle = 0
bot_version=u'۳.۰'
_cache={}
def translation(firstsite,secondsite,enlink):
    if _cache.get(tuple([enlink, firstsite,enlink, 'translation_en'])):
        return _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    if enlink.find('#')!=-1:
        _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=False
        return False
    if enlink==u'':
        _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=False
        return False    
    enlink=enlink.replace(u' ',u'_')
    site = pywikibot.Site(firstsite)
    sitesecond= pywikibot.Site(secondsite)

    try:
        categoryname = pywikibot.data.api.Request(site=site, action="query", prop="langlinks",titles=enlink,redirects=1,lllimit=500)
        categoryname=categoryname.submit()

        for item in categoryname[u'query'][u'pages']:
            case=categoryname[u'query'][u'pages'][item][u'langlinks']
        for item in case:
            if item[u'lang']==secondsite:
                intersec=item[u'*']
                break
        result=intersec
        if result.find('#')!=-1:
            _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=False
            return False
        _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=result
        return result
    except:
        _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=False
        return False

def Solve_linke_translation(fa_link,num):
    if num==1:#link is persian
        en_link=translation('fa','en',fa_link)
        if en_link:
            return u'[['+fa_link+u'|'+en_link+u']]'
        else:
            return u'[['+fa_link+u']]'

    if num==2:#link is english
        en_link=fa_link
        fa_link=translation('en','fa',en_link)

        if fa_link:
            return u'[['+fa_link+u'|'+en_link+u']]'
        else:
            return u'[['+en_link+u']]'

def Check_link(fa_link):
    fa_link=fa_link.split(u'|')[0].replace(u'[[',u'').replace(u']]',u'')
    fa_link_2 = re.sub(ur'[ءاآأإئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهييك]', ur'',fa_link)
    if fa_link_2!=fa_link:
        #pywikibot.output(u'The link '+fa_link+u' is persian!')
        return fa_link,1
    else:
        #pywikibot.output(u'The link '+fa_link+u' is english!')
        return fa_link,2

def check_ref_title_is_english(my_ref):
    my_ref_3=my_ref.replace(u'= ',u'=').replace(u' =',u'=').replace(u'{{ ',u'{{').replace(u' }}',u'}}').replace(u'\r',u'').replace(u'\n',u'').replace(u' |',u'|').replace(u'| ',u'|').replace(u'  ',u' ').replace(u'  ',u' ').replace(u'  ',u' ')
    if u'{{یادکرد' in my_ref_3:
        for item in [u'|عنوان',u'|نویسنده',u'|کتاب',u'|نام=',u'|نام خانوادگی=',u'|مقاله',u'|ک=',u'|ف=',u'|اثر']:
            if item in my_ref_3:
                ref_title=my_ref_3.split(item)[1].split(u'|')[0].strip()
                ref_title_2 = re.sub(ur'[ضصثقفغعهخحشسيبلاتنمظطزرذدپوکگجچژ]', ur"",ref_title)
                if ref_title_2!=ref_title:
                    #pywikibot.output(u'!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                    return False
                if ref_title.replace(u'=',u'').strip():
                    break
        return True
    elif (u'{{Cit' in my_ref_3) or (u'{{cit' in my_ref_3):
        for item in [u'|title',u'|first',u'|last',u'|work',u'|contribution',u'|publisher']:
            if item in my_ref_3:
                ref_title=my_ref_3.split(item)[1].split(u'|')[0].strip()
                ref_title_2 = re.sub(ur'[ضصثقفغعهخحشسيبلاتنمظطزرذدپوکگجچژ]', ur"",ref_title)
                if ref_title_2!=ref_title:
                    #pywikibot.output(u'!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                    return False
                if ref_title.replace(u'=',u'').strip():
                    break
        return True
    else:
        my_ref_3=my_ref_3.replace(u'[[',u'@1@').replace(u']]',u'@2@')
        if u'[' in my_ref_3:
            my_url=my_ref_3.split(u'[')[1].split(u']')[0]
            if u' ' in my_url:
                my_url_title=my_url.split(u' ')[1]
                my_url_title_2 = re.sub(ur'[ضصثقفغعهخحشسيبلاتنمظطزرذدپوکگجچژ]', ur"",my_url_title)
                if my_url_title_2!=my_url_title:
                     #pywikibot.output(u'!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                     return False
            else:
                #pywikibot.output(u'!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                return False
        else:
            my_ref_3= re.sub(ur'\@1\@.*?\@2\@', ur"",my_ref_3)
            my_ref_3_2 = re.sub(ur'[ضصثقفغعهخحشسيبلاتنمظطزرذدپوکگجچژ]', ur"",my_ref_3)
            if my_ref_3_2!=my_ref_3:
                #pywikibot.output(u'!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                return False
    return True

def run (text,sum):
    old_text=text
    RE=re.compile(r'<[\s]*ref[^>]*>([^<]*)<[\s]*\/[\s]*ref[\s]*>')
    all_refs=RE.findall(text.replace(u'\n',u'').replace(u'\r',u''))
    RE2=re.compile(ur'{{\s*(?:[Cc]ite|یادکرد)[\-_\s](?:{{.*?}}|[^}])*}}')
    all_refs2=RE2.findall(text.replace(u'\n',u'').replace(u'\r',u''))
    our_ref=[]
    if all_refs:
        our_ref=all_refs
    if all_refs2:
        our_ref+=all_refs2
    if not our_ref:
        return text,sum
    our_ref = list(set(our_ref))
    for refs in our_ref:
        if u'[[رده:' in refs:
            continue
        should_english=check_ref_title_is_english(refs)
        if should_english:
            RE=re.compile(ur'\[\[.*?\]\]')
            fa_links=RE.findall(refs)
            if fa_links:
                #pywikibot.output(u'----links----')
                for fa_link in fa_links:
                    fa_link_r,num=Check_link(fa_link)
                    if fa_link_r:
                        new_link=Solve_linke_translation(fa_link_r,num)
                        new_refs=refs.replace(u'[['+fa_link_r+u']]',new_link)
                        old_text=old_text.replace(refs,new_refs)
                        refs=new_refs
            else:
                #pywikibot.output(u'It doesnt have any wiki link!')
                continue
    if old_text!=text:
        return old_text,sum+u'+'+u'اصلاح ارجاع لاتین'
    else:
        return text,sum

def main(text,sum):
    sum2=u'اصلاح ارجاع لاتین'
    new_text,sum=run(text,sum)
    if sum:
       sum2=sum
    return new_text,sum2

if __name__ == "__main__":
    sum=u''
    PageTitle =raw_input('Page name > ').decode('utf-8')
    faSite=pywikibot.Site('fa',fam='wikipedia')
    fapage=pywikibot.Page(faSite,PageTitle)
    text=fapage.get()

    new_text,sum2=main(text,sum)

    if text!=new_text:
        fapage.put(new_text,u'ربات:اصلاح پیوندهای ارجاع لاتین')
        pywikibot.output(u"\03{lightgreen}Links of the page are updated!\03{default}")
    else:
        pywikibot.output(u"This Page doesn't need any change")
