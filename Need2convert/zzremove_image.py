# -*- coding: utf-8 -*-
import re
import wikipedia, pagegenerators
import codecs,config
import query,catlib
import urllib2,urllib
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
faSite = wikipedia.getSite('fa')

def is_deleted (image,wiki):
    image=image.replace(u' ',u'_')
    if wiki==u'commons':
        site = wikipedia.getSite(wiki,fam=u'commons')
    else:
        site = wikipedia.getSite(wiki)
    params = {
            'action': 'query',
            'list': 'logevents',
            'letitle': 'File:'+image.replace(u" ",u"_"),#ImageTilte
            'letype': 'delete'
    }
    try:
        queryresult = query.GetData(params,site)
        if len(queryresult['query']['logevents'])>0:
            return True
        else:
            return False
    except:
        return False

def is_exist(page_link, wiki):
    page_link=page_link.replace(u' ',u'_')

    if wiki==u'commons':
        site = wikipedia.getSite(wiki,fam=u'commons')
    else:
        site = wikipedia.getSite(wiki)
    params = {
        'action': 'query',
        'prop':'info',
        'titles': page_link
    }
    try:
        queryresult = query.GetData(params,site)
        for i in queryresult[u'query'][u'pages']:    
            redirect_link=queryresult[u'query'][u'pages'][i]['pageid']  
            return True# page existed
    except:
        return False# page not existed

def namespace_finder( page_link ,wiki):
    page_link=page_link.replace(u' ',u'_')
    site = wikipedia.getSite(wiki)
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': page_link,
        'redirects': 1,
        'lllimit':500,
    }
    try:
        queryresult = query.GetData(params,site)
        for item in queryresult[u'query'][u'pages']:
            page_namespace=queryresult[u'query'][u'pages'][item]['ns']
        return page_namespace
    except: 
        return False

def en_dig(a):
    for i in range(0,10):
       b=a.replace(u'۰۱۲۳۴۵۶۷۸۹'[i], u'0123456789'[i])
       a=b
    return b

def more(a,r):
    r=r+u"(?:.*?)\]\])"
    RE=re.compile(r)
    for aaa in RE.findall(a):
        a=a.replace(aaa+'\r\n',u'',1).replace(aaa+'\n\r',u'',1).replace(aaa+'\n',u'',1).replace(aaa+'\r',u'',1).replace(aaa,u'',1)
    return a

def clean_gallery(text):
    try:
        im = re.search(ur'<(?:gallery)[^<>]*>[\S\s]*?</(?:gallery)>', text)
        Gallery_old=im.group(0).strip()
        Gallery_new=Gallery_old.replace(u'\r',u'').replace(u'\n\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n')
        text=text.replace(Gallery_old,Gallery_new)
        return text
    except:
        return text
         
def uploadtext(text,page,oth,is_deleted_file,removed_from_gallery):    
    sum_extention_2=u''
    try:    
        text=text.replace(u'\r',u'').replace(u'{{audio||Play}}',u'').replace(u'<gallery>\n</gallery>',u'').replace(u'<gallery></gallery>',u'')
        text=clean_gallery(text)
        text=text.replace(u'تصویر:',u'پرونده:').replace(u'تصوير:',u'پرونده:').replace(u'پرونده:تصویر:',u'پرونده:')
        text=text.replace(u'پرونده:پرونده:',u'پرونده:').replace(u'پرونده:تصوير:',u'پرونده:').replace(u'File:',u'پرونده:').replace(u'file:',u'پرونده:')
        text=text.replace(u'تصویر:|\n',u'')
        text=text.replace(u'پرونده:|\n',u'')
        text=text.replace(u'تصوير:|\n',u'')
        if is_deleted_file==True:
            sum_extention=u'حذف شدهٔ'
        elif is_deleted_file=='commons':
            sum_extention=u'ویکی‌انبار حذف شدهٔ'
        else:
            sum_extention=u'ناموجود'
        if removed_from_gallery:
            sum_extention_2=u' از نگارخانه'
        edit_sum=u"ربات:حذف تصویر (۳.۱) "+sum_extention+u" [[:پرونده:"+ oth+u"]]"+sum_extention_2
        edit_sum=edit_sum.replace(u'&nbsp;',u' ')
        wikipedia.output(edit_sum)
        page.put(text,edit_sum)
    except Exception as inst:
        wikipedia.output(inst)
        pass

def remove_image(page):
    faTitle=page.title()  
    try:
        text = page.get()
        text2=text
        text=text.replace(u'پرونده:تصویر:',u'پرونده:')
        text=text.replace(u'پرونده:پرونده:',u'پرونده:').replace(u'پرونده:تصوير:',u'پرونده:').replace(u'پرونده:تصوير:',u'پرونده:')
        if text2!=text:
            page.put(text,u"ربات:اصلاح پیوندها")
        text=text.replace(u'File:',u'پرونده:').replace(u'file:',u'پرونده:').replace(u'|]]',u']]').replace(u'[[]]',u'').replace(u'تصویر:',u'پرونده:').replace(u'تصوير:',u'پرونده:')
    except wikipedia.NoPage:
        wikipedia.output(u"%s doesn't exist!" % page.title())
        return
    except wikipedia.IsRedirectPage:
        wikipedia.output(u"%s is a redirect, try later!" % page.title())
        return
    except:
        return
    if text.find(u'<gallery>')!=-1 and text.find(u'</gallery>')==-1:
        return
    wikipedia.output(u"----------------"+faTitle+u"------------------")
    urlr="https://fa.wikipedia.org/wiki/"+urllib.quote(faTitle.encode('utf8'))
    URLpage = urllib2.urlopen(urlr)
    htmlTxt=URLpage.read()
    removed_from_gallery=False
    if not 'wpDestFile=' in htmlTxt:
        wikipedia.output(u"\03{lightblue}There is no red Image on this page!\03{default}")
        if not '<div class="thumb" style="height:' in htmlTxt:
            return
        else:
            ImageList=htmlTxt.split('<div class="thumb" style="height:')
            removed_from_gallery=True
    else:
        ImageList=htmlTxt.split('wpDestFile=')
    
    number=0
    for ImageTilte in ImageList:

        number+=1
        if number==1:
            continue
        ImageTilte=ImageTilte.split('" class=')[0].split('</div>')[0]
        if ';">' in ImageTilte:
            ImageTilte=ImageTilte.split(';">')[1]
        ImageTilte=ImageTilte.replace('&nbsp;','_').replace(' ','_')
        ImageTilte=unicode(urllib2.unquote(ImageTilte),'UTF8')
        if not u'.' in ImageTilte:
            wikipedia.output(u"\03{lightyellow}File doesn't have . so it will pass\03{default}")
            return
        wikipedia.output(u"\03{lightblue}working on "+ImageTilte+u"\03{default}")
        if not is_deleted(ImageTilte,'fa'):
            if namespace_finder(faTitle,'fa')==0:
                if is_exist(u'File:'+ImageTilte, 'en'):
                    #go to upload
                    wikipedia.output(u">> \03{lightred}File:"+ImageTilte+u'\03{default} should be uploaded so it will pass')
                    continue
            if not is_deleted(ImageTilte,'commons'):
                is_deleted_file=False
            else:
                is_deleted_file=u'commons'
        else:
            is_deleted_file=True

        if re.search(u"[۰۹۸۷۶۵۴۳۲۱]",ImageTilte):
            if is_exist(u'File:'+en_dig(ImageTilte),'fa') or is_exist(u'File:'+en_dig(ImageTilte),'commons'):
                text_old=text    
                text=text.replace(ImageTilte.replace(u"_",u" "),en_dig(ImageTilte).replace(u"_",u" "))
                text=text.replace(ImageTilte,en_dig(ImageTilte))
                if text_old!=text:
                    wikipedia.output(u"ربات: تصحیح پیوند اشتباه به [[:پرونده:"+en_dig(ImageTilte)+"]]")      
                    page.put(text,u"ربات: تصحیح پیوند اشتباه به [[:پرونده:"+en_dig(ImageTilte)+"]]")
                continue
        lsf=[ImageTilte.replace(u"_",u" "),ImageTilte[0].lower()+ImageTilte[1:],ImageTilte[0].lower()+ImageTilte[1:].replace(u"_",u" "),ImageTilte,ImageTilte.replace(u"_",u"%20"),ImageTilte[0].lower()+ImageTilte[1:].replace(u"_",u"%20"),ImageTilte.replace(u"_",u"&nbsp;")]
        done=True
        for oth in lsf:
            original_text=text
            if text==original_text:
                escaped = re.escape(oth)    
                escaped = re.sub('\\\\[_ ]', '[_ ]',escaped)
                regexfa=ur'\[\[(?:پرونده|تصویر|[Ff]ile|[Ii]mage) *: *'+ escaped+ ur' *(?:\|(?:\[\[[^\]]+\]\]|[^\]])*) *\]\]'
                try:
                    REfa=re.compile(regexfa)
                    items=REfa.findall(text)
                    text=text.replace(items[0]+'\r\n',u'\r\n').replace(items[0]+'\n\r',u'\n\r').replace(items[0]+'\n',u'\n').replace(items[0]+'\r',u'\r').replace(items[0],u'')    
                    if text!=original_text:
                        uploadtext(text,page,oth,is_deleted_file,removed_from_gallery)
                        done=False
                        break
                except:
                    pass
            if text==original_text:
                escaped = re.escape(oth)    
                escaped = re.sub('\\\\[_ ]', '[_ ]',escaped)
                ggg=ur"(\[\[(?:پرونده|تصویر|[Ff]ile|[Ii]mage) *?: *?(?:"+escaped+ur")(?:[^\]]+)\]\])"
                try:
                    RE=re.compile(ggg)
                    for aaa in RE.findall(text):
                        wikipedia.output(aaa)
                        if aaa.count(ur"[[")>1:
                            text=more(text,ggg)
                        else:
                            text=text.replace(aaa+'\r\n',u'\r\n',1).replace(aaa+'\n\r',u'\n\r',1).replace(aaa+'\n',u'\n',1).replace(aaa+'\r',u'\r',1).replace(aaa,u'',1)
                    if text!=original_text:
                        uploadtext(text,page,oth,is_deleted_file,removed_from_gallery)    
                        done=False
                        break
                except:
                    wikipedia.output(u'rigex was wrong')    
        if text==original_text and u"<gallery" in text:
                for aa in text.split(u"<gallery")[1:]:
                    aa=aa.split("</gallery>")[0]
                    for oth in lsf:
                        escaped = re.escape(oth)    
                        escaped = re.sub('\\\\[_ ]', '[_ ]',escaped)
                        RE=re.compile(ur"((?:پرونده|تصویر|[Ff]ile|[Ii]mage) *?: *?(?:"+escaped+ur")(?:[^\n]+))(?:\n|$)")
                        for aaa in RE.findall(aa):
                            text=text.replace(aaa+'\r\n',u'\r\n',1).replace(aaa+'\n\r',u'\n\r',1).replace(aaa+'\n',u'\n',1).replace(aaa+'\r',u'\r',1).replace(aaa,u'',1)
        if text==original_text:
                for oth in lsf:
                    text=text.replace(oth,u'',1)
        if text!=original_text and done:    
            uploadtext(text,page,oth,is_deleted_file,removed_from_gallery)

#faTitle=u'کاربر:211mohsen/صفحه تمرین'
#fapage=wikipedia.Page(faSite,faTitle )
#gent=[fapage]


cat = catlib.Category( faSite,u'رده:صفحه‌های دارای پیوند خراب به پرونده' )
gent = pagegenerators.CategorizedPageGenerator(cat)

#gent = pagegenerators.NamespaceFilterPageGenerator(gent,0)
#gent = pagegenerators.PreloadingGenerator( gent,pageNumber = 60)
for fapage in gent:
    remove_image(fapage)