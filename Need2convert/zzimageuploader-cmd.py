#!/usr/bin/python
from __future__ import unicode_literals
# -*- coding: utf-8  -*-
# Reza (User:reza1615)
# Distributed under the terms of the CC-BY-SA 3.0 .
# Python 3
import scripts.imagetransfer as imagetransfer
import pywikibot,re,sys,json
from pywikibot import pagegenerators
from pywikibot import config

pywikibot.config.put_throttle = 0
pywikibot.config.maxthrottle = 0
faSite=pywikibot.Site('fa',fam='wikipedia')
enSite=pywikibot.Site('en',fam='wikipedia')
version=' (۴.۱)'
result={}
def encat_query(ImageTilte):
    cats=[]
    if ImageTilte=='':
        return []    
    ImageTilte=ImageTilte.replace(' ','_')
    queryresult = pywikibot.data.api.Request(site=enSite, action="query", prop="categories",titles=ImageTilte)
    queryresult=queryresult.submit()
    try:
        items=queryresult['query']['pages']
        for item in items:
            categoryha=queryresult['query']['pages'][item]['categories']
            break
        for cat in categoryha:
            cats.append(cat['title'])         
        return cats
    except: 
        print('coudnt get encat_query')
        return []

def make_image_description (faTitle,ImageTilte):
        categories=encat_query(ImageTilte)
        categories='\n'.join(categories)
        categories=categories.lower().replace('_',' ')
        license, template, description='','',''
        if 'album covers' in categories:
            license = 'جلد آلبوم'
            template = 'دلیل استفاده جلد آلبوم غیر آزاد'
            description = 'جلد'
        elif 'film poster' in categories or 'video covers' in categories or 'movie posters' in categories:
            license = 'جلد فیلم'
            template = 'دلیل استفاده جلد فیلم غیر آزاد'
            description = 'جلد'
        elif 'software covers' in categories:
            license = 'جلد نرم‌افزار غیر آزاد'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'جلد'
        elif 'game covers' in categories:
            license = 'جلد بازی'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'جلد'
        elif 'book covers' in categories:
            license = 'جلد کتاب'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'جلد'
        elif 'magazine covers' in categories or 'journal covers‎' in categories or 'newspaper covers‎' in categories:
            license = 'جلد مجله'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'جلد'
        elif 'stamp' in categories:
            license = 'نگاره تمبر'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'نگاره تمبر'
        elif 'currency' in categories:
            license = 'نگاره پول'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'نگاره پول'
        elif 'coat of arms' in categories:
            license = 'نشان غیر آزاد'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'نشان غیر آزاد'
        elif 'audio samples' in categories or 'audio clips‎' in categories:
            license = 'پرونده صوتی غیرآزاد'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'پروندهٔ صوتی برای'
        elif 'video samples' in categories :
            license = 'پرونده ویدئویی غیرآزاد'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'پروندهٔ ویدئویی برای'
        elif 'logos' in categories or 'symbols' in categories or 'seals' in categories:
            license = 'نگاره نماد'
            template = 'دلیل استفاده لوگو غیر آزاد'
            description = 'نماد'
        elif 'icon' in categories:
            license = 'آیکون برنامه رایانه‌ای غیر آزاد'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'آیکون'
        elif 'fair use character artwork' in categories:
            license = 'شخصیت غیرآزاد'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'تصویر'
        elif 'non-free posters' in categories:
            license = 'پوستر'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'پوستر'
        elif 'game covers' in categories:
            license = 'جلد بازی'
            template = 'دلیل استفاده جلد بازی غیر آزاد'
            description = 'جلد بازی'
        elif 'fair use in... images' in categories:
            license = 'منصفانه|عکس|عکاس یا ناشر آن'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'تصویر'
        elif 'fair use images' in categories or 'fair use media' in  categories:
            license = 'منصفانه|عکس|عکاس یا ناشر آن'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'تصویر'
        elif 'public domain' in categories:
            license = 'PD-USonly'
            template = 'اطلاعات'
            description = 'تصویر'
        elif 'abroad' in categories:
            license = 'PD-US-1923-abroad'
            template = 'اطلاعات'
            description = 'تصویر'
        else:
            license = 'منصفانه|عکس|عکاس یا ناشر آن'
            template = 'دلیل استفاده اثر غیر آزاد'
            description = 'تصویر'

        if template=='اطلاعات':
            our_discription='\n'.join([
            '{{اطلاعات',
            '| توضیحات     = '+ description + ' [[' + faTitle + ']]',
            '| منبع        = [[:en:' + ImageTilte.replace('پرونده:','File:') + '|ویکی‌پدیای انگلیسی]]',
            '| پدیدآور     = کاربران ویکی‌پدیای انگلیسی',
            '| اجازه‌نامه   = {{' + license + '}}',
            '}}'
            ])
        else:
            our_discription='\n'.join([
                '{{' + template,
                ' |توضیحات       = ' + description + ' [[' + faTitle + ']]',
                ' |منبع          = [[:en:' + ImageTilte.replace('پرونده:','File:') + '|ویکی‌پدیای انگلیسی]]',
                ' |مقاله         = ' + faTitle,
                ' |بخش یا قسمت   = در جعبه',
                ' |کیفیت پایین‌تر = بله',
                ' |دلیل          = استفاده در مقالهٔ [[' + faTitle + ']]',
                ' |جایگزین       = ندارد',
                ' |اطلاعات بیشتر  = ',
                '}}',
                '',
                '== اجازه‌نامه ==',
                '{{' + license + '}}'
            ])

        return our_discription

def clean_discription(imagename,page_title):
    page_title=page_title.replace('_',' ')
    faImagepage = pywikibot.Page(faSite, 'File:'+imagename)
    enImagepage = pywikibot.Page(enSite, 'File:'+imagename)
    image_discription=make_image_description (page_title,'File:'+imagename)
    if faImagepage.get():
        faImagepage.put(image_discription,'ربات:ترجمه و اصلاح متن پرونده'+version)
        result['msg']="پروندهٔ File:"+imagename+' با موفقیت بارگذاری شد!'
        print (json.dumps(result))
def upload_image(imagename,page_title):
        imagename=endig(imagename)
        if True:
        #try:
            imagepage = pywikibot.FilePage(enSite, 'File:'+imagename)
            int_imagepage = [imagepage]
            bot=imagetransfer.ImageTransferBot(int_imagepage, interwiki=False, targetSite=faSite,keep_name=True,ignore_warning=True)
            #bot.transferImage(imagepage)
            bot.run()
        #except:
        #   print('coudnt upload')
        #   return
        clean_discription(imagename,page_title)

def check_image(imagename):
    try:
        en_imagepage = pywikibot.Page(enSite, 'File:'+imagename)
        en_image_text=en_imagepage.get()
    except:
        msg="پروندهٔ File:"+imagename+' در ویکی‌پدیای انگلیسی موجود نبود!'
        result['msg']=msg
        print (json.dumps(result))
        return False
    #if True:
    try:
        fa_imagepage = pywikibot.Page(faSite, 'File:'+imagename)
        fa_image_text=fa_imagepage.get()
        msg="پروندهٔ File:"+imagename+' در ویکی‌پدیای فارسی وجود دارد!'
        result['msg']=msg
        print (json.dumps(result))
        return False
    except:
        print('coudnt do 2')
        pass

    list_templates=templatequery('File:'+imagename)
    if list_templates:
        balck_list=['Template:Db','Template:Duplicate','Template:Db-meta','Template:Deletable image','Template:Deletable file','Template:Copy to Wikimedia Commons']
        for i in balck_list:
            if  i in list_templates:
                msg="پروندهٔ File:"+imagename+' شرایط انتقال به ویکی‌پدیای فارسی را ندارد!'
                result['msg']=msg
                print (json.dumps(result))
                return False
        if 'Template:Non-free media' in list_templates:
            #try:
            fa_imagepage = pywikibot.Page(faSite, 'File:'+imagename)
            link_list=fa_imagepage.getReferences()
            counter=0
            for repage in link_list:
                if repage.title()!='ویکی‌پدیا:گزارش دیتابیس/مقاله‌های دارای پیوند به پرونده ناموجود':
                    counter+=-1
                counter+=1
                if counter>1:
                    msg="پروندهٔ File:"+imagename+' به جز فضای نام مقاله در فضای نام دیگری هم استفاده شده‌است و شرایط استفادهٔ منصفانه را ندارد.'
                    result['msg']=msg
                    print (json.dumps(result))
                    return False
                if repage.namespace()!=0 and repage.title()!='ویکی‌پدیا:گزارش دیتابیس/مقاله‌های دارای پیوند به پرونده ناموجود':
                    return False
            #except:
            #   return False
        return True
    else:
        msg="پروندهٔ File:"+imagename+' در ویکی‌پدیای انگلیسی الگوی استاندار ندارد.'
        result['msg']=msg
        print (json.dumps(result))
        return False

def endig(a):
    for i in range(0,10):
       b=a.replace('۰۱۲۳۴۵۶۷۸۹'[i], '0123456789'[i])
       a=b
    return b

def checksite(image):
    queryresult = pywikibot.data.api.Request(site=faSite, action="query", prop="imageinfo",titles='File:'+image.replace(" ","_"))
    queryresult=queryresult.submit()
    try:
        items=queryresult['query']['pages']
        for item in items:
            if queryresult['query']['pages'][item]['imagerepository']=='shared':
                return True
            else:
                return True
    except:
        print('coudnt checksite')
        return False

def templatequery(enlink):
    temps=[]
    enlink=enlink.replace(' ','_')
    categoryname = pywikibot.data.api.Request(site=enSite, action="query", prop="templates",titles=enlink,redirects=1,tllimit=500)
    categoryname=categoryname.submit()
    try:
        for item in categoryname['query']['pages']:
            templateha=categoryname['query']['pages'][item]['templates']
            break
        for temp in templateha:
            temps.append(temp['title'].replace('_',' '))         
        return temps
    except: 
        print('coudnt templatequery')
        return []

def main(page_name=False):
        if not page_name:
            categoryname = pywikibot.data.api.Request(site=faSite, action="query", meta="allmessages",ammessages="broken-file-category",amenableparser='')
            categoryname=categoryname.submit()
            categoryname = categoryname['query']['allmessages'][0]['*'] 
            pageslist = pywikibot.data.api.Request(site=faSite, action="query", list="categorymembers",cmlimit="max",cmtitle='Category:%s' % categoryname)
            pageslist=pageslist.submit()
            pageslist=pageslist['query']['categorymembers']
        else:
            pageslist=[page_name]

        for page_title in pageslist:
            if not page_name:
                page_title=page_title['title']
            else:
                page_title=page_title.replace(' ','_')
            if ':' in page_title:
               continue
            imagelist = pywikibot.data.api.Request(site=faSite, action="query", prop="images",imlimit="max",titles=page_title)
            imagelist=imagelist.submit()
            value=imagelist['query']['pages'].values()
            print(value)
            for image in list(value)[0]['images']:
                imagesinfo = pywikibot.data.api.Request(site=faSite, action="query", prop="imageinfo",titles=image['title'])
                imagesinfo=imagesinfo.submit()
                for imageinfo in imagesinfo['query']['pages'].values():
                    imagename = re.match(r'(?:' + '|'.join(faSite.namespace(6, all = True))\
                    + ')\:(.*)', image['title']).group(1)
                    if True:
                    #try:
                        if (imageinfo['missing']=="" and imageinfo['imagerepository']==""):
                            if check_image(imagename):
                                print(111)
                                upload_image(imagename,page_title)
                    '''
                    except:
                        msg="پروندهٔ File:"+imagename+' بدون تغییر رها شد!'
                        result['msg']=msg
                        print (json.dumps(result))
                    '''

main(sys.argv[1])

