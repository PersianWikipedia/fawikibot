#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Z    (User:ZxxZxxZ) Base of the code + Word Dictionaries and some of Regexs
# Reza (User:Reza1615) Code structure + Developing the code
# Amir (User:Ladgroups) Category sorting part
# Ebraminio (User:Ebraminio) Some of Regexs
#
# Distributed under the terms of MIT License (MIT)
#
# for calling this bot you can use  fa_cosmetic_changes_core(text,page) function
import pywikibot
from pywikibot import pagegenerators
from pywikibot import config
import string
from pywikibot.compat import query
from datetime import datetime
import re
from pywikibot import cosmetic_changes
import urllib
import ref_link_correction_core
import signal

pywikibot.config.put_throttle = 0
pywikibot.config.maxthrottle = 0

testpass=False
cleaning_version=u'۱۴.۹ core'
msg=u'('+cleaning_version +u')' 
faSite=pywikibot.Site('fa',fam='wikipedia')
_cache = {}
#-----------------
tags = ur'b|big|blockquote|charinsert|code|comment|del|div|em|gallery|hyperlink|i|includeonly|imagemap|inputbox|link|math|noinclude|nowiki|pre|ref|s|small|source|startspace|strong|sub|sup|template|timeline'
faChrs = u'ءاآأإئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیيككﮑﮐﮏﮎﻜﻛﻚﻙىىىﻴﻳﻲﻱﻰىىﻯيکیہەھ'
langs = u'بلغاری|بنگالی|پارسی باستان|پارسی میانه|پالی|پرتغالی|پشتو|پنجابی|پین‌یینی|تاگالوگ|تامیلی|تاهیتی|تایلندی|ترکمنی|ترکی|ترکی استانبولی|ترکی آذربایجانی|تلگو|جاوه‌ای|چکی|چینی|چینی ساده‌شده|چینی سنتی|دانمارکی|دوناگری|روسی|رومانیایی|ژاپنی|سامی|سانسکریت|سریانی|سکایی|سواحلی|سواحیلی|سوندایی|سوئدی|سیسیلی|صربی|عبری|عربی|فارسی افغانستان|فارسی ایران|فارسی تاجیکی|فارسی سره|فرانسوی|فنلاندی|فیلیپینی|کاتالان|کردی|کره‌ای|کروات|کرواسی|گالیسی|گجراتی|گرجی|گرینلندی|لاتین|لتونیایی|لیتوانیایی|مازندرانی|مالایی|مالزیایی|مجاری|مراتی|مصری|مغولی|مقدونی|نپالی|نروژی|نروژی نو|نورمنی|هاوائی|هائیتیایی|هلندی|هندی|هواسایی|ولزی|ویتنامی|یونانی|یونانی باستان'
zaed = ur"''متن مورب''|'''متن ضخیم'''|\[\[پرونده:مثال\.jpg]]|=+ متن عنوان =+|:خط تو رفته\n?|<nowiki>اینجا متن قالب‌بندی‌نشده وارد شود</nowiki>|\# مورد فهرست شماره‌ای\n?|\* مورد فهرست گلوله‌ای|<sub>متن زیرنویس</sub>|<sup>متن بالانویس</sup>|<small>متن کوچک</small>|<big>متن بزرگ</big>|#(؟:تغییرمسیر|REDIRECT) \[\[(?:نام صفحه مقصد|نام صفحه)]]|\{\| class=\.wikitable\.\n\|-\n! متن عنوان !! متن عنوان !! متن عنوان\n\|-\n\| مثال \|\| مثال \|\| مثال\n\|-\n\| مثال \|\| مثال \|\| مثال\n\|-\n\| مثال \|\| مثال \|\| مثال\n\|}|<gallery>\nپرونده:مثال\.jpg\|عنوان ۱\nپرونده:مثال.jpg\|عنوان ۲\n</gallery>|<ref>{{یادکرد\|نویسنده = \|عنوان = \| ناشر = \|صفحه = \|تاریخ = }}</ref>|<ref>{{یادکرد وب\|نویسنده = \|نشانی = \|عنوان = \| ناشر = \|تاریخ = \|تاریخ بازدید = }}</ref>|<ref>{{یادکرد خبر\|نام = \|نام خانوادگی = \|همکاران = \|پیوند = \|عنوان = \|اثر = \| ناشر = \|صفحه = \|تاریخ = \|بازیابی = }}</ref>|\[\[رده:]]|\[\[en:]]|\[\[fa:.*?]]|\[\[عنوان پیوند]]|\{\{\s*}}|\[\[\s*\|?\s*]]|<!-- *?-->|\'\'\'متن ضخیم'\'\'\|'\'متن مورب\'\'|\'\'\'متن پررنگ\'\'\'"#-----------------
bnMazi = u'[آا]راست|[آا]را?مید|[آا]زرد|[آا]زمود|[آا]سود|[آا]شامید|[آا]شفت|[آا]فرید|[آا]لا[یئ]ید|[آا]لود|[آا]ما[هس]ید|[آا]مد|[آا]مرزید|[آا]م[یو]خت|آورد|[آا][هو]یخت|[آا]غ[شس]ت|ارزید|افتاد|افراشت|ا?فروخت|افزود|افسرد|ا?فشاند|اف[کگ]ند|انجامید|اند[او]خت|اندیشید|ان[بگ]اشت|نگاشت|انگیخت|ایستاد|با[خف]ت|با[لر]ید|[شب]ایست|بخش[یو]د|برازید|ب[ور]د|[چبپ]رید|[رجشب]ست|بلعید|پ[وا]شید|پخت|پذیرفت|پرا[کگ]ند|پرداخت|پرست?ید|پرورد|پرید|پژمرد|پژوهید|پسندید|پنداشت|[بپ]و[سشی]ید|پیچید|پیراست|پیمود|پیوست|تا[فخ]ت|تپید|ترا[وش]ید|تر[سشک]ید|تکانی?د|تنید|توانست|جن[بگ]ید|[جد]وش?ید|چرخید|چسبید|چ[مکشر]?ید|خر[او]شید|خ[مرز]ید|خشکید|خوابید|خو?است|خواند|خورد|خیسید|داد|داشت|[مد]انست|درخشید|دزدید|دوخت|ربود|راند|ر[مس]ید|رو?فت|رنجید|رو[یئ]ید|ریخت|زد|زدود|زیست|س[وا]خت|سپرد|س[تر]ود|ستیزید|سرشت|سزید|سنجید|ش[تکگ]افت|شد|شک?ست|ش[کگ]فت|شمرد|شناخت|شنید|شورید|طلبید|غلطید|فرستاد|فر[مس]ود|فریفت|فشرد|فهمید|قبولاند|کا[سش]ت|کاوید|ک[نر]د|کشت|کشید|کو[چش]ید|کوفت|گداخت|گذا?شت|گرا[یئ]ید|گردید|گرفت|گروید|گری[خس]ت|گزارد|گزید|گس[تا]رد|گسست|گ[فش]ت|گشود|گماشت|گنجید|ل[رغ]زید|ما[لس]ید|ماند|مرد|نا[مل]ید|نشست|نکوهید|نگاشت|ن?گریست|نمود|نواخت|نوردید|نوشت|نهاد|نهفت|نی?وشید|ور?زید|هراسید|هلید|یازید|یافت'
bnMzare = u'[آا]را[یم]|[آا]زار|[آا]ماس|[آا]ز?مای|[آا]سای|[آا]شام|[آا]شوب|[آا]غا[رز]|[آا]فرین|[آا]گن|[آا]لای|[آا]ی|[آا]م[یور]ز|[آا]و?ر|[آا]ویز|[آا]هنج|ارز|افت|افر[او]ز|افزای|افسر|ا?فشان|اف[کگ]ن|انبار|انجام|اندا[یز]|اندوز|اندیش|ا?نگار|انگیز|اوبار|ایست|با[فلیشرز]|بخشای|بخش|براز|ب[َُ]?ر|بند|بساو|بسیج|بلع|بو[یس]?|بیز|پاش|پالای|پ[رز]|پذیر|پرا[کگ]ن|پرداز|پرست?|پرور|پژمر|پژوه|پسند|پلاس|پلک|پناه|پندار|پو[سشیک]|پیچ|پی[مر]ای|پیوند|تا[پز]|تو?پ|ترا[شو]|تر[سشک]|تکان|تن|توان|[نلجد]ه|جن[بگ]|جو[یش]?|چا[یپ]|چ[مکپشفر]|چر[خب]?|چسب?|چلان|چین|خا[یر]|خرا[مش]|خس[بت]|خشک|خروش|خ[ملرز]|خوا[نبه]|خو[فر]|خی[سز]|دا[نر]|درخش|درو?|دزد|[لد]م|دو[شز]?|ربای|ران|رخش|ر[سمه]|رو[یب]?|رشت|رقص|رنج|[بر]ی[نز]|زا[یر]|ز[ین]|زدای|ساز|سپا?ر|سپ؟وز|ستان|ستر|ستیز|سرای|سرشت|س[رز]|سنب|سگال|سنج|سای|شا[شی]|شتاب|شوی?|شک[او]ف|شکن|شکیب|ش[مو]ر|شناس|شنو|طلب|طوف|غارت|غرّ?|غلط|غنو|فرست|فر[سم]ای|فروش|فریب|فشر|فهم|قاپ|قبولان|کا[هرو]|ک[َُِ]?ش|ک[نف]|کو[چشب]|گای|گداز|گذا?ر|گرا[یز]|گرد|گیر|گرو|گریز?|گزار|گز|گزین|گس[تا]ر|گسی?ل|گشای|گو[یز]|گن[جد]|گ[مو]ار|ل[غر]ز|لن[گد]|لیس|ما[سلن]|میر|مک|مو[یل]|نا[زلم]|ن?شین|نکوه|نگا?ر|نمای|نواز|نورد|نویس|نهنب|نی?وش|ور?ز|هراس|هل|یا[برز]'
noAlef = u'باجی|بادانی?|بادی?|بار|باژور|بافت|با[لن]|بانگا[نه]|بتاب|بجی?|بچین|بخس[بت]|بخواره|بخور[دشی]?|بخوست|بخیز|بدارچی|بدارخانه|بدار[وکی]?|بدستان|بدستی?|بدندان|بدنگ|بده|بدیده|براهه?|برفت|برو[دن]|بریز|بریزگان|بزن|بز[یه]|بژ|بسال|بسالان|بست|بستره|بست[نه]|بسکون|بسه|بسوار|بشار|بشتگاه|بشتن?|بشخور|بش[نیش]|بشنگ|بغوره|بفت|بک|بکار|ب‌?کافت|بکا[نم]ه|بکش|بکشین|بکند|بکوهه|بکی|بگاه|بگرد|بگردان|بگز|بگوشت|بگون|بگیر|بگینه|بلوج|بنوس|بوند|بونمان|بونه|بیار|پارات|پارتاید|پارتمان|پاراتی|پاندیس|پاندیسیت|تربان|ترمه|تروپین|تریاد|تشبار|تشبان|تشپا|تشخوار|تشدان|تشفشان|تشک|تشکده|تشگاه|تش[هی]?|تشیزه|تشین|تلیه|ته|تورپات|تیه|ثار|ثام|جاردن|جان|جودان|جید[نه]|جیل|جین|چار|چاردن|چارکشی|چمز|حاد|خال|خت[نه]|خر|خرالامر|خرالزمان|خرت|خردست|خرزمان|خریا؟ن|خ[سش]مه|خشیج|خشیجان|خشیگ|خور|خورچرب|خورخشک|خورسنگین|خوندبازی|خوندک?|دا[بشک]|دامس|دخ|درس|درمه?|درنگ|دمک|دمیت|دمیرال|دمیزاد|دنیس|دیش|دیند?ه|ذار|ذری?|ذربایجانی?|ذربو|ذرجشن|ذرخش|ذریو?ن|ذوقه|ذین|را[یء]|راستن|راسته|رام|رامانیدن|رامش|رامگاه|رامی|رامیدن|رایش|رایشگاه|رایشگر|راییدن|رتروز|رتزین|رتیست|رتیشو|رخالق|ردبیز|رده|ردینه|رزم|رزو|رزوخواه|رزومندی?|رشه|رشیتکت|رشیو|رغ|رغده|رگون|رمان|رمان‌?شهر|رمیچر|رمید[هن]|رن|رنائوت|رنج|رنگ|رواره|روبند|روغ|ری|ریا|ریستوکرات|ریستوکراسی|ریغ|زادگان|زادگی|زادمرد|زاد[یه]?|زادوار|زادی‌?خواه|زار|زارتلخه|زا?رد[نه]|زارنده|زاریدن|زال|زجوی|زخ|زدن|زرد|زردگی|زرم|زرمجو|زرمگین|زری|زغ|زفنداک|زگار|زما|زمایش|زمایشگاه|زماینده|زمایه|زمندی?|زمودگی|زمود[نه]|زمون|زناک|زور|زوغ|زوقه|زیدن|زیر|ژان|ژانس|ژخ|ژدار|ژده|ژغ|ژفنداک|ژگن|ژن[دگ]|ژندن|ژندیدن|ژیانه|ژید[نه]|ژیر|ژیرنده|ژیریدن|ژینه|سان|سانسور|سانی|سایش|سایشگاه|ساینده|ساییدن|سبان|سپیرین|ستانه|ستر|ستیگماتیسم|ستی[من]ه?|سدست|سغده|سفالت|سکاریس|سمانخانه|سمانخراش|سمان[هی]?|سموغ|سه|سودگی|سود[نه]|سیابان|سیاچرخ|سیازنه|سیاکردن|سیا[وب]?|سیایی|سیب|سیل|سی[من]ه|سیون|شا[بم]|شامیدن|شانه|شپز|شپزخانه|شتالنگ|شت[می]|شخال|شخانه|شردن|شرمه|شفتگی|شفت[نه]?|شکار|شکارساز|شکاره|شکوبه|شکو[بخ]?|شکوخیدن|شگر|شمالی?|شموغ|شنا|شناگر|شنا[هو]|شناوری|شنایی|شوب|شوب‌?گر|شوبیدن?|شور|شوردن|شوریده|شوغ|شوفتن|شیانه|شیهه|صال|غُش|غا|غاجی|غار|غاردن|غاری|غاریدن|غازگر|غاز[هی]?|غازیدن|غالش?|غالنده|غالید[نه]|غچه|غردن|غری?|غز|غ[سش]ت[نه]|غل|غندن|غنده|غو[زشل]|غوشیدن|غیل|فا[تق]|فاقی|فتاب[هی]?|فتومات|فدم|فرنگ|فروشه|فریدگار|فرید[نه]|فرین|فرینگان|فریننده|فگانه|فل|فند|فندیدن|فیش|ق|قا|قازاده|قاسی|ق‌?بانو|قچه|قسنقر|قشام|قطی|قورایی|قوش|کادمیک?|کاردئون|کام|ک[بپج]|کبند|کتریس|کتور|کروبات|کروباسی|کستن|ککرا|کله|کند[نه]|کنش|کنه|کنیدن|کواریوم|کوستیک|کولاد|کومولاتور|گاهاندن|گاهی?|گ[پج]|گراندیسمان|گرمان|گشتن|گفت|گنج|گنده|گهی|گو|گور|گورگر|گو[شن]|گیشیدن|گی[من]|لاپلنگی|لات|لاچیق|لاخون|لاس|لاسکا|لاگارسون|لامد?|لاوه?|لایش|لاییدن|لبالو|لبوم|لبومین|لپر|لت|لترناتیو|لر|لرژی|ل[شغ]|لغده|لفا|لفت[نه]|لکالویید|لگرو|لگونه|لوچه|لودگی|لود[نه]|لوسن|لومین|لومینیوم|لو[ئن]ک|لیاژ|لیداد|لیزیدن|ماتور|ماج|ماجگاه|مادگی|ماده|مار|مارگر|ماریدن|ماریلیس|ماس|ماسانیدن|ماسیدن|ماق|مال|مانی|ماهانیدن|ماهیدن|مبولانس|مپر|مپرسنج|مپلی|مپول|مپی|مخته|مدگان|مدن?|مرانه|مرزش|مرزگار|مرزنده|مرزیدن|مرزیده|مرغ|مریکا|مریکایی?|مفی|مفیبول|مه|موت|موخت[نه]|مود[نه]|موزانه|موزشی?|موزشیار|موزگا[رن]|موزنده|موزه|موق|موکسی|مولن|مون|مونیاک|میب|میختگی|میخت[نه]|میز[شه]?|میزگاری?|میغه?|نابولیسم|نات?|ناتومی|نارشی|نارشیس[تم]ی?|ناس|نالوگ|نالیز|نام|ناناس|نتراکت|نتریک|نت[نی]|نتیک|نجا|نچت?|ندوتوکسین|ندودرم|ندوسپرم|ندوسکوپی|ندون|نرمال|نزیم|نژین|نژیوکت|نژیوگرافی|نسه|نسیلین|نک|نگلوفیل|نوریسم|نیلین|نین|نیه|نیون|هار|هاردن|هازیدن|هستگی|هسته|هک|همند|هنج|هنجیدن|هنگ[ری]?|هنگساز|هنین|هو|هوانگیز|هوپا|هوتک|هوچشم|هودل|هوفغند|هومند|هون|هیانه|هیختن|واخ|وارگی|وا[رز]ه?|واشناسی|واکس|وام|وانتاژ|وانس|وانگارد|وانویسی|وردجو|وردگا؟ه|وردن|وردیدن|ورک|ورنجن|وری|وریدن|وریل|ونگ|ونگان|ونگون|ویخت[نه]|ویزش?|ویزگ?ان|وی[زژ]ه|ویزون|ویشن|یا[تن]?|یبک|یتم?|یزنه|یژ|یفت|یفون|ینده|یه|ییژ|یین|[یئ]?ینه|ئورت'
tnvindar = u'(الزاما|لزوما|یقینا|قطعا|حتما|قاعدتا|طبیعتا|طبعا|قهرا|جدّا|حقیقتا|واقعا|مطمئنا|واضحا|مسلما|تماما|کاملا|عینا|اکیدا|مطلقا|دقیقا|مستقیما|اصولا|اصلا|اصالتا|نسبا|نسبتا|تقریبا|حدودا|معمولا|قانونا|شرعا|اخلاقا|خلقا|احتمالا|استثنائا|اساسا|کلّا|جزئا|مجموعا|جمعا|اجماعا|شدیدا|نهایتا|اقلا|اکثرا|غالبا|عمدتا|ندرتا|بعضا|گاها|صریحا|صراحتا|عموما|اختصاصا|خصوصا|مجملا|اجمالا|اختصارا|مختصرا|مشروحا|ظاهرا|باطنا|عمیقا|ذاتا|فطرتا|روحا|جسما|ابتدائا|مقدمتا|بدوا|بعدا|قبلا|جدیدا|سابقا|اخیرا|ابدا|عمرا|تلویحا|علنا|حضورا|غیابا|نیابتا|لطفا|اجبارا|اختیارا|عالما|عمدا|عامدا|تعمدا|متعمدا|عادتا|مستقلا|احتیاطا|احیانا|غفلتا|سهوا|اشتباها|عاجلا|عجالتا|مرتجلا|ارتجالا|سریعا|فورا|دا[یئ]ما|ضرورتا|نقدا|منحصرا|صرفا|دفعتا|کرارا|مکررا|مجددا|مرتبا|مستمرا|متواترا|تدریجا|تصادفا|عملا|فعلا|موقتا|ضمنا|نتیجتا|نوعا|اصطلاحا|جسارتا|بالا ?غیرتا|م[وؤ]کدا|ذیلا|شخصا|مشترکا|مفصلا|رسما|ترجیحا|قلبا|ر[اأ]سا|تو[اأ]ما|متناوبا|متوالیا|متقابلا|متعاقبا|متّ?فقا|مثلا|فرضا|ایضا|مضافا|مصرّ?ا|ارفاقا|انصافا|جهارا|طولا|متدرجا|غانما|احتراما|ناچارا|سفارشا|تلفنا|زبانا|کتبا|شفاها|اولا|سوما|چهارما|ثانیا|ثالثا|رابعا|خامسا|سادسا|سابعا|ثامنا|تاسعا|عاشرا)'#اکساندر دوما!
sametH = ur'فرمانده|زره|کوه|گره|گنه|سپه|مکروه|م?ت?وجّ?ه|منزّ?ه|نزه|ابله|مرفّ?ه|شبیه|مت?شابه|کریه|پادشه|اللّ?ه|اله|[آکبتدرزشلم]ه' #e: صامت هـ
spcBfre = u'.،,:؛;؟٫)}]»》”，·。一ｰ・、：（）「」〜？！ء'
spcAftr = u'({[«《“，·。一ｰ٫・、：（）「」〜？！'
bLA = u'(?!['+faChrs+u'])'
bLB = u'(?<!['+faChrs+u'])'
site_category=ur'رده'
boxes=[u'infobox',u'Geobox',u'Taxobo', u'جعبه']
#--------------------------------------fa_replaceExcept---------------------
TEMP_REGEX = re.compile(
    '{{(?:msg:)?(?P<name>[^{\|]+?)(?:\|(?P<params>[^{]+?(?:{[^{]+?}[^{]*?)?))?}}')

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def autoEdISBN(txt,msg):
    txt2=txt
    persianDigits=u'۰۱۲۳۴۵۶۷۸۹'
    #ISBN, ISSN and PMID's numbers should in english
    txt_old=re.sub(ur'\/\/.*?(?=[\s\n\|\}\]<]|$)',u'',txt)
    AllISBN=  re.findall(ur'(\b(ISBN|ISSN|PMID|PubMed) *:? *([۱۲۳۴۵۶۷۸۹۰0-9–—−ـ_\-]+)([^۱۲۳۴۵۶۷۸۹۰0-9–—−ـ_\-]|$))',txt_old, re.S)
    if AllISBN:
        for item in AllISBN:
            item=item[0]
            item_old=item
            for i in range(0,10):
                item=item.replace(persianDigits[i], str(i))
                item=item.replace(u'–',u'-')
                item=re.sub(ur'[–—−ـ_\-]+',u'-',item)
                item=item.replace(ur'\b(ISBN|ISSN|PMID|PubMed) *:? *([۱۲۳۴۵۶۷۸۹۰\-0-9]+)([^۱۲۳۴۵۶۷۸۹۰\-0-9]|$)',ur'\1 \2\3')
                item=item.replace(u'PubMed',u'PMID')
            txt=txt.replace(item_old,item)
    #Allows WikiMagic to work with ISBNs
    txt = txt.replace(ur'ISBN *\-10:|ISBN *\-13:|ISBN *\-10|ISBN *\-13|ISBN:',u"ISBN")
    #ISSN regexs from [[:en:Wikipedia:AutoWikiBrowser/Settings/ISSN]]
    txt = txt.replace(ur'ISSN\s*(\d)',u"ISSN \1")
    txt = txt.replace(ur'ISSN (\d)(\d)(\d)(\d)[\.\: ~\=]*(\d)(\d)(\d)([\dx])',u"ISSN \1\2\3\4-\5\6\7\8 ")
    txt = txt.replace(ur'ISSN (\d)(\d)(\d)(\d)\-(\d)(\d)(\d)x',u"ISSN \1\2\3\4-\5\6\7X")
    txt = txt.replace(ur'ISSN (\d)(\d)(\d)(\d)\-(\d)(\d)(\d)x',u"ISSN \1\2\3\4-\5\6\7X")
    #ISBN regexs from [[:Wikipedia:AutoWikiBrowser/Settings/ISBN-hyph]]
    txt = txt.replace(ur'ISBN(\d)',u"ISBN \1")
    txt = txt.replace(ur'\[\[ *(ISBN [\d\-x]{10,13}) *\]\]',u"\1")
    txt = txt.replace(ur'\[\[ISBN\|(ISBN\s*[^\]]*)\]\]',u"\1")
    txt = txt.replace(ur'\[*ISBN\]*\:*[ \t]+([0-9X\-]+)',u"ISBN \1")
    txt = txt.replace(ur'ISBN +([\d-]{1,9}) (\d+|X\W)',u"ISBN \1\2")
    txt = txt.replace(ur'\[*ISBN\]*\:* *\[\[Special\:Booksources\/\d*\|([\dxX\- ]+)\]\]',u"ISBN \1")
    txt = txt.replace(ur'\[isbn\]\:* *(\d)',u"ISBN \1")
    txt = txt.replace(ur'ISBN (\d{10,10}) - *(\d)',u"ISBN \1 ,\2")
    loopcount = 0
    while (loopcount<10):
        txt = txt.replace(ur'ISBN (\d{1,9}) (\d|x)',u"ISBN \1\2")
        loopcount+=1
    txt = txt.replace(ur'ISBN (\d{1,9})(x)',u"ISBN \1X")
    txt = txt.replace(ur'ISBN (\d\d\d\d\d\d\d\d\d(\d|x)) +(\d)',u"ISBN \1, \3")
    txt = txt.replace(ur'ISBN ([\d-]{12,12}) (\d|x)',u"ISBN \1-\2")
    if txt2!=txt:
        msg=u'شابک+'+msg
    return txt,msg

def findmarker(text, startwith=u'@@', append=None):
    # find a string which is not part of text
    if not append:
        append = u'@'
    mymarker = startwith
    while mymarker in text:
        mymarker += append
    return mymarker
        
def minor_edits (text):
    text=text.replace(u'\r',u'')    
    text=text.replace(u'\n \n \n',u'\n\n').replace(u'\n \n',u'\n\n').replace(u'\n \n',u'\n\n').replace(u'\n  \n',u'\n\n').replace(u"--------",u'----').replace(u"-----",u'----').replace(u"--------",u'----').replace(u"-----",u'----')
    text = re.sub(ur'[\r\n]{3,}', ur"\n\n",text)
    text=text.replace(u'[[ ',u'[[').replace(u' ]]',u']]').replace(u' }}',u'}}').replace(u'{{ ',u'{{').replace(u'< ',u'<').replace(u'</ ',u'</').replace(u' />',u'/>').replace(u'<!--\n',u'<!--').replace(u'\n-->',u'-->').replace(u'<!---\n',u'<!---').replace(u'\n--->',u'--->')
    text=text.replace(u'[[ ',u'[[').replace(u' ]]',u']]').replace(u' }}',u'}}').replace(u'{{ ',u'{{').replace(u'==  ',u'== ').replace(u'==  ',u'== ').replace(u'  ==',u' ==').replace(u'  ==',u' ==')
    text=fa_replaceExcept(text,u' >',u'>', ['math', 'pre', 'template', 'timeline', 'ref', 'source', 'startspace'])
    text=text.replace(u'\n<ref',u'<ref').replace(u'</ref>\n<ref',u'</ref><ref')
    text = re.sub(re.compile(ur'^(\=+)\s*(.*?)\s*(\=+)$', re.MULTILINE), ur"\1 \2 \3",text)
    text=text.replace(u'\n\n*',u'\n*').replace(u'\n\n#',u'\n#')
    #a: الگوافزایی
    if text.find(u'{{پانویس')==-1:
        if text.find(u'= منابع =') !=-1:
          text = re.sub(ur'(= منابع =+\n)', ur'\1{{پانویس}}\n', text, re.S)
    text=finall_cleaning(text)
    minor_text=text.strip()
    return minor_text
    
def arabic_to_farsi(text):
    exceptions = ['gallery', 'hyperlink', 'interwiki', 'math', 'pre', 'template', 'timeline', 'ref', 'source', 'startspace', 'inputbox','file','URL']
    text2=text
    while True:
        text = fa_replaceExcept(text, ur'[كﮑﮐﮏﮎﻜﻛﻚﻙ]', ur'ک', exceptions)
        text = fa_replaceExcept(text, ur'[ىىىﻴﻳﻲﻱﻰىىﻯي]', ur'ی', exceptions)
        text = fa_replaceExcept(text, ur'[ہەھ]', ur'ه', exceptions)
        text = fa_replaceExcept(text,ur'[ۀﮤ]',ur'هٔ', exceptions)
        if text==text2:
           break
        text2=text
    return text

    
def Dictation(txt,msg_short,msg=msg):
    old_txt=txt
    #s: شبه‌ساده‌ها  ####### مشارٌ‌اليه، مضاف‌ٌاليه، منقولٌ‌عنه، مختلفٌ‌فيه، متفق‌ٌعليه، بعبارةٍاُخرى، اباًعن‌جدٍ، اىّ‌نحوٍكان.
    #txt = re.sub(bLB+u'من ?(باب|جمله)'+bLA, ur'من‌\1', txt)
    txt = re.sub(ur' مع ?(هذا|ذلک|الفار[غق]|الوصف|ال[اأ]سف)', ur' مع‌\1', txt)
    txt = re.sub(ur' علی ?(هذا|حده|رغم|الاصول|الحساب|الخصوص|البدل|الدوام|السویه|الطلوع|الله|القاعده)', ur' علی‌\1', txt)
    txt = re.sub(bLB+u' ذو ال', u' ذوال', txt)
    txt = re.sub(ur' ذی ?(ال|نفع|امر|جود|حساب|حق|حیات|ربط|روح|شعور|صلاح|صلاحیّ?ت|عقل|علاقه|فقار|فن|قیمت|نفوذ)'+bLA, ur' ذی‌\1', txt)
    txt = re.sub(bLB+u' حقّ? (?=البوق|العبور|الت[اأ]لیف|التدریس|الزحمه|اللّ?ه|النّ?اس|تعالی)', u' حق‌', txt)
    txt = re.sub(ur' عن ?[قغ]ریب', ur' عن‌قریب', txt)
    #txt = re.sub(ur' قتل ?عام', ur' قتل‌عام', txt)
    txt = re.sub(ur' علی[‌ ][اأ]یّ?[‌ ]?حال', ur' علی‌أی‌حال', txt)
    txt = re.sub(ur' من[‌ ]?حیث[‌ ]?المجموع', ur' من‌حیث‌المجموع', txt)
    txt = re.sub(ur'ب(?:|ه[‌ ])ر[اأ]ی[‌ ]العین', ur'برأی‌العین', txt)
    txt = re.sub(ur'ما ?ب(?:|ه[‌ ])ازا', u'مابازا', txt)
    txt = re.sub(ur'متقابل[‌ ](?:ب|به[‌ ])ر[اأ]س', ur'متقابل‌به‌رأس', txt)
    #txt = re.sub(ur'منحصر ?(?:ب|به[‌ ])فرد', ur'منحصربه‌فرد', txt)
    txt = re.sub(bLB+ur'فی[‌ ]?ما ?بین', ur'فی‌مابین', txt)
    txt = re.sub(ur' [اآ]ی[ةت][‌ ]?اللّ?ه', ur' آیت‌الله', txt)#عنایت‌الله
    txt = re.sub(ur'حج[ةته][‌ ]?ال[اإ]سلام', ur'حجت‌الاسلام', txt)
    txt = re.sub(ur'ثق[ةته][‌ ]?ال[اإ]سلام', ur'ثقةالاسلام', txt)
    txt = re.sub(ur'امیر ?الم[وؤ]منین', ur'امیرالمؤمنین', txt)
    txt = re.sub(ur'(متوازی|مختلف)[‌ ]?ال[اأ]ضلاع', ur'\1‌الأضلاع', txt)
    txt = re.sub(ur'متساوی[‌ ]?السّ?اقین', ur'متساوی‌الساقین', txt)
    txt = re.sub(ur'قا[یئ]م[‌ ]الزّاوی[ةه]', ur'قائم‌الزاویه', txt)
    txt = re.sub(ur'دا[یئ]ر[ةته][‌ ]?(البروج|المعارف|العلوم)', ur'دائرة\1', txt)
    txt = re.sub(ur'دا[یئ]م[‌ ](الخمر|الصوم|الذّ?[کك]ر)', ur'دائم‌\1', txt)
    txt = re.sub(ur'ر[اأإ]س[‌ ](الجدی|السّ?رطان|المال)', ur'رأس‌\1', txt)
    txt = re.sub(ur'(مجنی|مجنی)[‌ ][عا]لیه', ur'\1‌علیه', txt)
    txt = re.sub(ur'(مضاف|مسند|مرجوع|مشار|منتقل)ٌ?[‌ ]?[عا]لیه', ur'\1ٌ‌الیه', txt)
    txt = re.sub(ur'منته[ای][‌ ]?[عا]لیه', ur'منتهی‌الیه', txt)
    txt = txt.replace(u'بین الملل', u'بین‌الملل').replace(u'نرم افزار', u'نرم‌افزار').replace(u'حزب الل', u'حزب‌الل')
    txt = txt.replace(u'جدید الاحداث', u'جدیدالاحداث').replace(u'کثیر الانتشار', u'کثیرالانتشار').replace(u'سریع السیر', u'سریع‌السیر')
    txt = txt.replace(u'لازم الاجرا', u'لازم‌الاجرا').replace(u'فوق الذکر', u'فوق‌الذکر').replace(u'مرضی الطرف', u'مرضی‌الطرف')
    txt = txt.replace(u'خاتم الانبیا', u'خاتم‌الانبیا').replace(u'متفق القول', u'متفق‌القول').replace(u'قریب الوقوع', u'قریب‌الوقوع')
    txt = txt.replace(u'سوق الجیشی', u'سوق‌الجیشی').replace(u'محیر العق', u'محیرالعق').replace(u'عظیم الجث', u'عظیم‌الجث')
    txt = txt.replace(u'لطایف الحیل', u'لطایف‌الحیل').replace(u'موقوف المعانی', u'موقوف‌المعانی').replace(u'سلیم النفس', u'سلیم‌النفس')
    txt = txt.replace(u'موثق الصدور', u'موثق‌الصدور').replace(u'شمس العمار', u'شمس‌العمار').replace(u'حسب الامر', u'حسب‌الامر')
    txt = txt.replace(u'مسلوب الاراده', u'مسلوب‌الاراده').replace(u'مستجاب الدعو', u'مستجاب‌الدعو')
    txt = re.sub(bLB+u'(دار|مشترک|ممنوع|قدیم|قلیل|ناقص|ضعیف|قوی|تحت|ر[یئ]یس|ربّ?|امّ?|حقّ?|ماء|ماوراء|باب) (?=ال)', ur'\1‌', txt)
   #txt = re.sub(u'‌(?=الهام|الصاق|الزام|القا|الکتریک|الکتریسیته)', u'', txt)

    #e: اً
    txt = re.sub(bLB+tnvindar+bLA, ur'\1ً', txt)
    txt = re.sub(ur'اصلاً? ?و ?ابداً?', ur'اصلا و ابدا', txt)
    txt = re.sub(ur'اهلاً? ?و ?سهلاً?', ur'اهلاً وسهلاً', txt)
    txt = re.sub(ur'ً'+ur'['+ur'ًٌٍَُِّْْ'+ur']', ur'ً', txt)#remove double erab

    #e: آ
    #txt = re.sub(bLB+u'(ا|أ)('+noAlef+u')'+bLA, ur"آ\2", txt)#it has some bugs!
    txt = txt.replace(u' راکتور', u' رآکتور').replace(u'فرآیند', u'فرایند').replace(u'فرآورده', u'فراورده')# e: ا <-> آ
    txt = re.sub(bLB+ur'ایده?[‌ ][اآ]ل', ur'ایده‌آل', txt)
    #s: افعال
    txt = txt.replace(u' دو میدانی ', u' دومیدانی ')
    txt = re.sub(bLB+u'(نمی) ?([نب]ی؟|)('+bnMzare+u'|'+bnMazi+u')(ان|)(م|ی|د|یم|ید|ا?ند)'+bLA, ur'\1‌\2\3\4\5', txt) # می bug همیاری
    #txt = re.sub(bLB+u'(باز|فر[او]|وا|[بد]ر) ?([هن]?می‌|)([منب]ی?|)('+bnMzare+u'|'+bnMazi+u')(م|ی|د|یم|ید|ا?ند)'+bLA, ur'\1\2\3\4\5', txt) # پیشوند فعل ### BUG
    txt = re.sub(bLB+u'(باز|فر[او]|وا) ?([منب]ی?|)('+bnMazi+u')ن'+bLA, ur'\1\2\3ن', txt)#وی در جنگیدن با من
    txt = re.sub(bLB+u'('+bnMazi+u')ه (ام |ای |ایم |اید |اند )'+bLA, ur'\1ه‌\2', txt) # فم بین «ه» و شناسه طبق شیوه‌نامه است باید جدا باشد
    txt = re.sub(u'([منب])یا(رزید|فتاد|فتد|فراشت|فروخت|فزود|فسرد|فشاند|ف[کگ]ند|نجامید|ند[او]خت|ندیشید|ن[بگ]اشت|نگیخت)(م|ی|یم|ید|ند|[^'+faChrs+u'])', ur'\1ی\2', txt) # نیافتاد -> نیفتاد
    txt = re.sub(u'([منب])یا(رز|فر[او]ز|فزای|فسر|فشان|ف[کگ]ن|نبار|نجام|ندا[یز]|ندوز|ندیش|نگار|نگیز)(م|ی|د|یم|ید|ا?ند|[^'+faChrs+u'])', ur'\1ی\2\3', txt) # بیاندیش -> بیندیش

    #s: ضمایر ملکی
    txt = re.sub(u'(?:ه|هٔ)[‌ ](مان|تان|شان)'+bLA, ur'ه‌\1', txt)#BUG:Solved
    txt = re.sub(u'(?<=ه)[‌ ](ام |ات |اش )'+bLA, ur'‌\1', txt)

    #s: و
    txt = re.sub(u'رفت[‌ ]?و ?[اآ]مد', u'رفت‌وآمد', txt)
    txt = re.sub(u'گفت[‌ ]?و ?گو', u'گفتگو', txt)
    txt = re.sub(u'جست[‌ ]?و ?جو', u'جستجو', txt)
    txt = re.sub(u'پخت[‌ ]?و ?پز', u'پخت‌وپز', txt)
    txt = re.sub(u'شست[‌ ]?و ?شو', u'شست‌وشو', txt)
    txt = re.sub(u'خفت[‌ ]?و ?خیز', u'خفت‌وخیز', txt)
    txt = re.sub(bLB+u'کند ?و ?کا?و'+bLA, u'کندوکاو', txt)
    txt = re.sub(bLB+u'کم[‌ ]و ?کاست', u'کم‌وکاست', txt)

    #s: بسیط
    txt = re.sub(u'(فن|دل)ّ?[‌ ]?[آا]وری', ur'\1اوری', txt)    
    txt = re.sub(bLB+u' دل[‌ ](سوزی|تنگی|بری) '+bLA, ur' دل\1 ', txt)#Bug دل بریدن
    txt = re.sub(bLB+u'یک[‌ ]دلی'+bLA, u'یکدلی', txt)
    txt = re.sub(u'گاه[‌ ]و ?بی[‌ ]?گاه', u'گاه‌و‌بیگاه', txt)

    #e: دیگر غلط‌های املایی
    txt = re.sub(u' (سپاس|شکر|بر)[‌ ]?گ[ذز]ار ', ur' \1‌گزار ', txt)#بنا بر گزارش
    txt = re.sub(u'(پایه|بنیان)[‌ ]?گزار', ur'\1‌گذار', txt)#متغییر الگو بنیانگذار
    txt = re.sub(bLB+u'بی[‌ ]?م[حه]ابا', u'بی‌محابا', txt)
    txt = re.sub(bLB+u' بر ?خو?است', u' برخاست', txt)
    txt = re.sub(u'خوانواد(?=ه|گی)', u'خانواد', txt)
    txt = re.sub(u'[آا]نفو?لو? ?[آا]نزا', u'آنفلوآنزا', txt)
    txt = re.sub(bLB+u'غری[ضظ]ه'+bLA, u'غریزه', txt)
    txt = txt.replace(u'خواستگاه', u'خاستگاه')
    txt = txt.replace(u'اطاق', u'اتاق').replace(u'باطری', u'باتری').replace(u'باطلاق', u'باتلاق').replace(u' ملیون', u' میلیون')
    txt = txt.replace(u'ضمینه', u'زمینه').replace(u'انظباط', u'انضباط').replace(u'حاظر', u'حاضر')
    #txt = txt.replace(u'نفوظ', u'نفوذ') ###
    txt = txt.replace(u'مذبور', u'مزبور').replace(u'قائله', u'غائله').replace(u' وحله', u' وهله').replace(u' مرهمت', u' مرحمت')    
    txt = txt.replace(u' انهنا', u' انحنا').replace(u'پزشگی', u'پزشکی').replace(u'تضاهرات', u'تظاهرات')
    txt = txt.replace(u'تلوزیون', u'تلویزیون').replace(u'پرفسور', u'پروفسور').replace(u' خوشنود', u' خشنود')
    txt = txt.replace(u' الویت', u' اولویت').replace(u'ملیارد', u'میلیارد')
    txt = re.sub(u'ه‌(گی|گانی?)'+bLA, ur'\1', txt)
    #txt = re.sub(bLB+u'وب[‌ ]?(سایت|گاه)', u'وبگاه', txt) ###in many cases it could be template vaiable!
    txt = re.sub(u'ویکی ?(?=سازی|فا |[مپ]دیا)', u'ویکی‌', txt)
    txt = re.sub(u'ویکی‌پدیا ?(?='+langs+u')', u'ویکی‌پدیای ', txt)
    txt = re.sub(u'علاقه?[‌ ]?مند', u'علاقه‌مند', txt)
    #txt = re.sub(u' باقی مانده ', u' باقی‌مانده ', txt) #کتاب باقی مانده است.
    txt = re.sub(u'مت[عاأ][سص]ّ?فانه', u'متأسفانه', txt)

    txt = re.sub(bLB+u' من[‌ ]را'+bLA, u' مرا', txt)
    #txt = re.sub(u'عدم وجود'+bLA, u'نبودِ', txt)
    #txt = txt.replace(u'عدم حضور', u'غیاب')
    txt = re.sub(u'اقدامات لازمه?'+bLA, u'اقدام‌های لازم', txt)

    #e: ماه‌ها
    #txt = re.sub(bLB+u'مارچ'+bLA, u'مارس', txt)#BUG می‌تواند اسم شخص هم باشد
    txt = re.sub(bLB+u'(?:ژوییه)'+bLA, u'ژوئیه', txt)
    #txt = re.sub(bLB+u'[اآ]گوست'+bLA, u'اوت', txt)#جین آگوست دومینیک
    txt = re.sub(bLB+u'دی?سا?مبر'+bLA, u'دسامبر', txt)
    txt = re.sub(u'(ربیع|جمادی)[‌ ]?(?:الثانی|ال[اأإ]خر)', ur'\1‌الثانی', txt)
    txt = re.sub(u'(ربیع|جمادی)[‌ ]?ال[اأإ]ول', ur'\1‌الاول', txt)
    #txt = re.sub(u'ذ[وی][‌ ]?(?:ال|)(حج|قعد)[ةه]', ur'ذی‌ال\1ه', txt) ###
    
    #e: جمع‌الجمع
    txt = re.sub(u'(مدارک)[‌ ]?های?'+bLA, u'مدارک', txt)      
       
    #e: حشو
    txt = re.sub(bLB+u'بر ?علیه', u'علیه', txt) # بر علیه
    txt = re.sub(u'اعلم[‌ ]?تر', u'اعلم', txt) # تر

    #e: طبق قاعدهٔ فارسی
    txt = re.sub(ur'(آزمایش|پژوهش|پیشنهاد|نمایش|دستور|فرمایش|گزارش|گرایش|باغ|کوهستان)اتی ', ur'\1‌هایی ', txt) # اتی -> هایی
    txt = txt.replace(u'بازرسین', u'بازرسان').replace(u'داوطلبین', u'داوطلبان') #e: ین -> ان
    txt = re.sub(ur' (رهبر|خوب|بد|من)یّ?ت ', ur' \1ی ', txt) # یّت -> ی
    txt = re.sub(bLB+u'دو[یئ]یت', u'دوگانگی', txt) # یّت
    txt = txt.replace(u'زباناً', u'زبانی').replace(u'تلفناً', u'تلفنی').replace(u'ناچاراً', u'به‌ناچار').replace(u'گاهاً', u'گاهی') #e: اً
    #--------------------------Reza added------------------------

    if old_txt!=txt:
        if msg_short:
            msg=u'املا+'+msg    
        else:
            msg=u'اشتباه نگارشی + '+msg
    return txt.strip(),msg

def cleaning(text,msg_short,msg=msg):    
    old_text=text
    text=re.sub(ur'\n[\t\u00A0]+',u'\n',text)
    text=re.sub(ur'[\u0085\u00A0\u1680\u180E\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]',u' ',text)
    text=text.replace(u'\r',u'').replace(u'\n^ "',u'\n*"').replace(u'&zwnj;',u'‌').replace(u'\n \n \n',u'\n\n').replace(u'\n \n',u'\n\n').replace(u'\n \n',u'\n\n').replace(u'\n  \n',u'\n\n')
    text=text.replace(u'< ',u'<').replace(u' >',u'>').replace(u'<!--\n',u'<!--').replace(u'\n-->',u'-->').replace(u'<!---\n',u'<!---').replace(u'\n--->',u'--->')
    #تمیزکاری فاصلهٔ مجازی
    text = re.sub(u'(\u202A|\u202B|\u202C|\u202D|\u202E|\u200F)',u'\u200C', text)#حذف کارکترهای تغییرجهت
    text = re.sub(u'‌{2,}', u'‌', text) # پشت‌سرهم
    text = re.sub(u'‌(?![ئاآأإژزرذدوؤةبپتثجچحخسشصضطظعغفقکگلمنهیيً\[\]ٌٍَُِّْٰٓٔكﮑﮐﮏﮎﻜﻛﻚﻙىىىﻴﻳﻲﻱﻰىىﻯيکیہەھ]|[\u0900-\u097F]|ֹ)', '', text) # در پس
    text = re.sub(u'(?<![ئبپتثجچحخسشصضطظعغفقکگلمنهیيًٌٍَُِّْٰٓٔك\[\]ﮑﮐﮏﮎﻜﻛﻚﻙىىىﻴﻳﻲﻱﻰىىﻯيکیہەھ]|[\u0900-\u097F]|f|ֹ)‌', '', text) # در پیش
    text=arabic_to_farsi(text)
    
    text = re.sub(u"(?:"+zaed+u")", "", text)
    #اصلاح شماره‌بندی
    text=text.replace(u'\n•',u'\n*')
    text=text.replace(u'\n\n*',u'\n*').replace(u'\n\n#',u'\n#').replace(u'\n# \n',u'\n#').replace(u'\n#\n',u'\n#').replace(u'\n*\n',u'\n*').replace(u'\n* \n',u'\n*').replace(u'\n*==',u'\n==').replace(u'\n#==',u'\n==').replace(u'\n* ==',u'\n==').replace(u'\n# ==',u'\n==')
    text=text.replace(u'\n\n**',u'\n**').replace(u'\n\n##',u'\n##').replace(u'\n## \n',u'\n##').replace(u'\n##\n',u'\n##').replace(u'\n**\n',u'\n**').replace(u'\n** \n',u'\n**').replace(u'\n**==',u'\n==').replace(u'\n##==',u'\n==').replace(u'\n** ==',u'\n==').replace(u'\n## ==',u'\n==') 
    #text = re.sub(re.compile(ur'^[\d۰-۹]+\s*[-_ـ–]\s*(.*)(\n|<br \/>)(?=\n)', re.MULTILINE), ur"# \1",text)
    
    #تمیزکاری عنوان 
    #----cleaning for subsections -----
    text=re.sub(ur'(\< *\/ *br *\>|\< *br *\\ *\>|\< *br *\. *\>)',u'<br/>',text)
    text=text.replace(u'<br/>',u'{{سخ}}').replace(u'{{سر خط}}',u'{{سخ}}').replace(u'{{سرخط}}',u'{{سخ}}').replace(u'<br />',u'{{سخ}}')
    text=re.sub(ur"(\n\{\{سخ\}\}|\n\n)\'\'\'(.*?)\'\'\'[\s_](\{\{سخ\}\}\n|\n\n)",r"\n\n== \2 ==\n\n",text)
    text=re.sub(ur"(\n\{\{سخ\}\}|\n\n)\'\'\'(.*?)\'\'\'(\{\{سخ\}\}\n|\n\n)",r"\n\n== \2 ==\n\n",text)
    text=re.sub(ur"(\n\{\{سخ\}\}|\n\n)[\s_]\'\'\'(.*?)\'\'\'(\{\{سخ\}\}\n|\n\n)",r"\n\n== \2 ==\n\n",text)
    text=re.sub(ur"\n\n\'\'\'(.*?)\'\'\'(\s)\n\n",r"\n\n== \1 ==\n\n",text)
    text=re.sub(ur"\n\n\'\'\'(.*?)\'\'\'(\s)\n\n",r"\n\n== \1 ==\n\n",text)
    text=re.sub(ur"\n\n\'\'\'(.*?)\'\'\'(\s)\n([\n\#\*])",r"\n\n== \1 ==\n\3",text)
    text=re.sub(ur"^(=+([^=].*?)=+)[\t\s]{1,}\n",r"\1\n",text)

    text = re.sub(re.compile(ur'^(\=+)\s*(.*?)\s*(\=+)$', re.MULTILINE), ur"\1 \2 \3",text).replace(u"==  ",u'== ').replace(u"  ==",u' ==')    
    for i in range(0,40):
        text=text.replace(u"=  =",u'==').replace(u"=   =",u'==')
        text=text.replace(u"--------",u'----').replace(u"-----",u'----')
    text=text.replace(u'== "',u'== ').replace(u'" ==',u' ==') 
    text=text.replace(u"== '''",u'== ').replace(u"''' == ",u' ==')
    text=text.replace(u"=='''",u'==').replace(u"'''== ",u'==')
    
    for i in u".:,;&^#@•→←↔↑↓…~٫،؛ٔ*":
        text=text.replace(u"== "+i,u"== ").replace(i+u" ==",u" ==").replace(u"\n\n"+i+u"\n\n",u"\n\n").replace(u"=\n"+i+u"\n\n",u"=\n\n")
    #زیربخش‌ها فقط یکی باشند
    if text.find(u'==')==-1:    
        text = re.sub(re.compile(ur'^\=([^\=\r\n]+)\=$', re.MULTILINE), ur"== \1 ==",text)
        text=text.replace(u'==  ',u'== ').replace(u'  ==',u' ==')
    #----cleaning for links and wiki syntaxes-----
    text=text.replace(u'[[ ',u'[[').replace(u' ]]',u']]').replace(u' }}',u'}}').replace(u'{{ ',u'{{').replace(u'< ',u'<').replace(u' >',u'>').replace(u'</ ',u'</').replace(u' />',u'/>')
    text=text.replace(u'[[ ',u'[[').replace(u' ]]',u']]').replace(u' }}',u'}}').replace(u'{{ ',u'{{').replace(u'==  ',u'== ').replace(u'==  ',u'== ').replace(u'  ==',u' ==').replace(u'  ==',u' ==')
    text=text.replace(u'\n ]]\n',u']]\n').replace(u'\n]]\n',u']]\n')
    
    #----cleaning for images-----
    text=text.replace(u'\r',u'').replace(u'{{audio||Play}}',u'').replace(u'<gallery>\n\n</gallery>',u'').replace(u'<gallery>\n</gallery>',u'').replace(u'<gallery></gallery>',u'')
    text = re.sub(ur'\[\[ *(?:[Cc]ategory|رده):', u'[[رده:', text)
    text = re.sub(ur'\{\{ *(?:[Tt]emplate|الگو):', u'{{', text)
    text = re.sub(ur'\[\[ *(?:[Ii]mage|[Ff]ile|تصویر|تصوير):', u'[[پرونده:', text)
    text=text.replace(u'تصویر:',u'پرونده:').replace(u'تصوير:',u'پرونده:').replace(u'پرونده:تصویر:',u'پرونده:')
    text=text.replace(u'پرونده:پرونده:',u'پرونده:').replace(u'پرونده:تصوير:',u'پرونده:')
    text=text.replace(u'تصویر:|\n',u'')
    text=text.replace(u'پرونده:|\n',u'')
    text=text.replace(u'تصوير:|\n',u'')     
    #e: عنوان‌ها
    txet=text.replace(u'<small>',u'{{کوچک}}').replace(u'</small>',u'{{پایان کوچک}}')
    text=text.replace(u'== منابع ==\n\n== منابع ==',u'== منابع ==').replace(u'== منابع ==\n\n\n== منابع ==',u'== منابع ==').replace(u'== منابع ==\n== منابع ==',u'== منابع ==')
    
    text = re.sub(ur'\=\s*پانو[یي]س[‌ ]?(?:ها)?\s*\=', u'= پانویس =', text)
    text = re.sub(ur'\=\s*گالر[یي]\s*\=', u'= نگارخانه =', text)
    text = re.sub(ur'\=\s*نگارستان\s*\=', u'= نگارخانه =', text)
    text = re.sub(ur'\=\s*پاورقی\s*\=', u'= پانویس‌ها =', text)
    text = re.sub(ur'\=\s*پاورقی‌ها\s*\=', u'= پانویس‌ها =', text)    
    text = re.sub(ur'\=\s*لیست\s*\=', u'= فهرست =', text)    
    text = re.sub(ur'\=\s*جُ?ستار(?:ها[یي])? (?:وابسته|د[یي]گر|مرتبط|مشابه)\s*\=', u'= جستارهای وابسته =', text)
    text = re.sub(ur'\=\s*(?:همچنین ببینید|ببینید)\s*\=', u'= جستارهای وابسته =', text)
    text = re.sub(ur'\=\s*(?:منبع|منبع[‌ ]?ها|رفرنس|رفرنس[‌ ]?ها|ارجاع[‌ ]?ها|ارجاع|مرجع[‌ ]?ها|رفرنس|برگرفته از|مراجع|منابع و یادداشت[‌ ]?ها|منبع|مرجع|فهرست مراجع|لیست مراجع|فهرست ارجاع[‌ ]?ها|فهرست ارجاع)\s*\=', u'= منابع =', text)
    text = re.sub(ur'\=\s*(?:پ[یي]وند|ل[یي]ن[کك])[‌ ]?(?:ها[یي])? (?:به ب[یي]رون|ب[یي]رون[یي]|خارج[یي])\s*\=', u'= پیوند به بیرون =', text)
    text=text.replace(u'= همچنین ببینید =',u'= جستارهای وابسته =').replace(u'=همچنین ببینید=',u'= جستارهای وابسته =').replace(u'=مطالب مرتبط=',u'= جستارهای وابسته =').replace(u'= مطالب مرتبط =',u'= جستارهای وابسته =').replace(u'= مطلب مرتبط =',u'= جستارهای وابسته =').replace(u'=مطلب مرتبط=',u'= جستارهای وابسته =')
    # تمیزکاری زیربخش‌های پردندانه
    # اصلاح مواردی که همه زیر بخش‌ها ۳ تایی باشند
    text_test=re.sub(r'\n\=+ (منابع|جستارهای وابسته|پیوند به بیرون|پانویس|نگارخانه) \=+\n','',text)
    if text_test.find(u'\n== ')==-1:
        #۳ تایی
        if text_test.find(u'\n=== ')!=-1:
            text = re.sub(re.compile(ur'^\=\=\=([^\=\r\n]+)\=\=\=$', re.MULTILINE), ur"== \1 ==",text)
        # ۴ تایی
        elif text_test.find(u'\n==== ')!=-1:
            text = re.sub(re.compile(ur'^\=\=\=\=([^\=\r\n]+)\=\=\=\=$', re.MULTILINE), ur"== \1 ==",text)
        else:
            text=text.replace(u'===',u'==')
        text=text.replace(u'==  ',u'== ').replace(u'  ==',u' ==')

    text = re.sub(re.compile(ur"^(\=+)([^\=\r\n]+)(\=+)$", re.MULTILINE), ur"\1 \2 \3",text)
    text = re.sub(re.compile(ur"^(\=+) \<(?:small|big) *\>([^\=\r\n]+)\<\/(?:small|big) *\> (\=+)$", re.MULTILINE), ur"\1 \2 \3",text)
    text=text.replace(u'==  ',u'== ').replace(u'  ==',u' ==').replace(u'==  ',u'== ').replace(u'  ==',u' ==').replace(u'==  ',u'== ').replace(u'  ==',u' ==').replace(u'==  ',u'== ').replace(u'  ==',u' ==') 
    text_test=re.sub(ur'\n\=\= (منابع|جستارهای وابسته|پیوند به بیرون|پانویس|نگارخانه) \=\=\n',u'',text)

    if string.count(text_test,u'\n== ')==0 and string.count(text_test,u' ==\n')==0:
        if string.count(text_test,u'\n=== ')==0 and string.count(text_test,u' ===\n')==0:
            text=text.replace(u'====',u'==')
        else:
            text=text.replace(u'===',u'==')

    #e: <ref> & {{پانویس}}
    text = re.sub(ur'<(?:\s*|\s*/\s*)references?(?:\s*|\s*/\s*)>', u'{{پانویس}}', text).replace(u'<references />',u'{{پانویس}}').replace(u'<references/>',u'{{پانویس}}')
    text = re.sub(ur'{{(?:[Rr]eflist|[Rr]eferences?|پانویس[‌ ]?ها)(?=\||})', u'{{پانویس', text)
    text = re.sub(ur'{{(پایان|آغاز|) ?(چپ|راست|وسط)[‌ ]?چین}}', ur'{{\1 \2‌چین}}', text).replace(u'{{ چپ‌چین}}',u'{{چپ‌چین}}').replace(u'{{ راست‌چین}}',u'{{راست‌چین}}')
    text = re.sub(ur'{{راست‌چین}}\s*{{پانویس(.*?)}}\s*{{پایان راست‌چین}}', ur'{{پانویس\1}}', text, re.S)
    text = re.sub(ur'{{چپ‌چین}}\s*{{پانویس(.*?)}}\s*{{پایان چپ‌چین}}', ur'{{پانویس\1|چپ‌چین=بله}}', text, re.S)
    text = re.sub(ur'<small>\s*{{پانویس(.*?)}}\s*</small>', ur'{{پانویس\1|اندازه=کوچک}}', text, re.S)
    text = re.sub(ur'{{راست‌چین}}\s*{{پانویس(.*?)}}\s*{{پایان راست‌چین}}', ur'{{پانویس\1}}', text, re.S)
    text = re.sub(ur'{{چپ‌چین}}\s*{{پانویس(.*?)}}\s*{{پایان چپ‌چین}}', ur'{{پانویس\1|چپ‌چین=بله}}', text, re.S)
    text = re.sub(ur'<small>\s*{{پانویس(.*?)}}\s*</small>', ur'{{پانویس\1|اندازه=کوچک}}', text, re.S)
    refsa=re.findall(ur'(?ism)<ref[ >].*?</ref>',text, re.S)
    if refsa:
        if len(refsa) > 7:
            text = text.replace(u'{{پانویس}}',u'{{پانویس|۲}}')
            text = text.replace(u'{{پانویس|اندازه=کوچک}}',u'{{پانویس|۲|اندازه=کوچک}}')
            text = text.replace(u'{{پانویس|عرض=۳۰}}',u'{{پانویس|۲|عرض=۳۰}}')
            text = text.replace(u'{{پانویس|اندازه=ریز}}',u'{{پانویس|۲|اندازه=ریز}}')
            text = text.replace(u'{{پانویس|گروه=پانویس}}',u'{{پانویس|۲|گروه=پانویس}}')
            text = text.replace(u'{{پانویس|چپ‌چین=بله}}',u'{{پانویس|۲|چپ‌چین=بله}}')
    text=text.replace(u'==<',u'==\n<').replace(u'>==',u'>\n==')#واگردانی خطای کد

    # Files
    text = re.sub(ur'\[\[ *[Ii]mage *: *', u'[[پرونده:', text)
    text = re.sub(ur'\[\[ *[Ff]ile *: *', u'[[پرونده:', text)
    text = re.sub(ur'(\[\[پرونده:.*?\|) *thumb *(?=\|.*?]])', ur'\1بندانگشتی', text)
    text = re.sub(ur'(\[\[پرونده:.*?\|) *left *(?=\|.*?]])', ur'\1چپ', text)
    text = re.sub(ur'(\[\[پرونده:.*?\|) *right *(?=\|.*?]])', ur'\1راست', text)
    text = re.sub(ur'(\[\[پرونده:.*?\|) *center *(?=\|.*?]])', ur'\1وسط', text)
    text = re.sub(ur'(\[\[پرونده:.*?\|) *link *= *(?=.*?]])', ur'\1پیوند=', text)    
    #a: الگوافزایی
    if text.find(u'{{پانویس')==-1 and text.find(u'<references group')==-1:
        if text.find(u'= منابع =') !=-1:
          text = re.sub(ur'(= منابع =+\n)', ur'\1{{پانویس}}\n', text, re.S)
    #e: نام الگوها
    text = re.sub(u'{{(?:جا:|subst:|)(?:فم|نیم[‌ ]?فاصله|فاصلهٔ? مجازی)}}', u'‌', text)
    text = re.sub(u'{{(?:جا:|subst:|)--}}', u'–', text)
    text = re.sub(u'{{(?:جا:|subst:|)---}}', u'—', text)
    text = re.sub(u'{{(?:DEFAULTSORT|[Dd]efaultsort|ترتیب|ترتیب[‌ ]پیش[‌ ]?فرض) *[|:] *(?=.*?}})', u'{{ترتیب‌پیش‌فرض:', text)
    text=re.sub(ur'{{(ترتیب‌پیش‌فرض|DEFAULTSORT):[-\w,\s\(\)]+}}\n?', ur'', text)    
    text = re.sub(ur'{{(?:[Cc]ommons?|انبار|ویکی انبار) ?\|', u'{{ویکی‌انبار|', text)
    text = re.sub(ur'{{(?:[Ww]ikispecies|ویکی گونه) ?\|', u'{{ویکی‌گونه|', text)
    text = re.sub(ur'{{(?:[Cc]ommons?[\- ]?(?:[Cc]ats?|[Cc]ategory)|(?:ویکی[‌ ]?|)انبار[\- ]?رده) ?\|', u'{{ویکی‌انبار-رده|', text)
    text = re.sub(u'{{(?:منبع|ذکر منبع|درخواست یادکرد منا?بع|نیاز به منبع|بی[‌ ]منبع|منبع کم|[Uu]nreferenced)}}', u'{{بدون منبع}}', text)
    text = re.sub(u'{{(?:تمیز ?[کك]اری|[Cc]lean ?up)}}', u'{{تمیزکاری}}', text)
    text = re.sub(u'{{(?:منا?بع بیشتر|منبع بهتر|بهبود منا?بع|به)}}', u'{{بهبود منبع}}', text)
    text = re.sub(u'{{وی[کك]ی[‌ ]?(?:سازی)}}', u'{{ویکی‌سازی}}', text)
    text = re.sub(u'{{(?=(?:'+langs+ur')\|)', ur'{{به ', text)
    #جعبه اطلاعات
    # خط اضافی بعد از جعبه اطلاعات
    text_box=Get_box (text)
    if text_box:
        text_box=text_box.strip()
        if text_box.strip():
            text=text.replace(text_box+u'\n\n',text_box+u'\n')

    #تمیزکاری سرخط
    for i in range(0,2):    
        text=text.replace(u'{{سخ}} ',u'{{سخ}}').replace(u'{{سخ}} ',u'{{سخ}}').replace(u' {{سخ}}',u'{{سخ}}').replace(u' {{سخ}}',u'{{سخ}}').replace(u'{{سخ}}\n==',u'\n==').replace(u'==\n{{سخ}}',u'==\n').replace(u'=={{سخ}}',u'==').replace(u'{{سخ}}==',u'==')
        text=text.replace(u']]\n{{سخ}}',u']]{{سخ}}').replace(u'{{سخ}}\n[[',u'{{سخ}}[[').replace(u'{{سخ}}\n\n==',u'\n\n==').replace(u'{{سخ}}\n\n\n==',u'\n\n==').replace(u'{{سخ}}\n==',u'\n==').replace(u'==\n\n{{سخ}}',u'==\n\n').replace(u'==\n\n\n{{سخ}}',u'==\n\n')
    text=text.replace(u'{{سخ}}\n*',u'\n*').replace(u'{{سخ}}\n\n*',u'\n*').replace(u'{{سخ}}\n#',u'\n#').replace(u'{{سخ}}\n\n#',u'\n#').replace(u'{{سخ}}\n|',u'\n|').replace(u'{{سخ}}\n\n|',u'\n|')
    text=text.replace(u'%7B%7Bسخ}}',u'{{سخ}}')#Correcting the bug

    #تمیزکاری ارجاع‌ها
    text=text.replace(u'\n<ref',u'<ref').replace(u'</ref>\n<ref',u'</ref><ref').replace(u'</ref>{{سخ}}<ref',u'</ref><ref')
    #e: کامنت‌های اضافی
    comment_list=[u'<small></small>',u'<sup></sup>',u'<sub></sub>',u'<code></code>',u'<pre></pre>',u'<math></math>',u'<nowiki></nowiki>',u"'''متن پررنگ'''",u"''متن مورب''",u'<!--توضیح-->',u'<!--- رده‌بندی --->',u'<!--- میان‌ویکی را وارد کنید مثل [[en:Article]] --->',u'<!--- [[ویکی‌پدیا:پانویس‌ها]] را بخوانید. در وسط مقاله از <ref>منبع</ref> به عنوان منبع استفاده کنید -->']
    for item in comment_list:
        text=text.replace(item,u'').replace(item+u'\n',u'').replace(item.replace(u'><',u'>\n<'),u'').replace(item.replace(u'><',u'>\n\n<'),u'')  

    #اصلاح نشانی اینترنتی
    text=re.sub(ur'(\<ref.*?\>) *(\[|)\www\.',u'\1\2http://www.',text)
    text=re.sub(ur'\[\[ *(https?\:\/\/.*?) *\]\]',u'[\1]',text)
    text=re.sub(ur'\[\[ *(\/\/.*?) *\]\]',u'[\1]',text)
    text=re.sub(ur'(https?:\/?\/?){2,}',u'\1',text)
    text=re.sub(ur'^ +(\=+[^\=]+\=+)',u'\1',text, re.MULTILINE)
    text=re.sub(ur'\[\[\|',u'[[',text)
    text=re.sub(ur'\[\[([^\]]+)\{\{\!\}\}([^\]]+)\]\]',ur'[[\1|\2]]',text)
    text=re.sub(ur'\[{2}([^\|]+)\|\1\]{2}',ur'[[\1]]',text)

    #حذف رده انگلیسی    
    text = re.sub(ur'\[\[([Cc]ategory|رده):[\w\s\–\-\|]+?\]\]\r?\n?', u"",text).replace(u'[[رده:|]]',u'')     
   
    #ابهام‌ردایی
    for i in [u'ابهام زدایی',u'ابهامزدایی',u'ابهامزدائی',u'ابهام‌زدائی',u'ابهام زدائی']:
        text=text.replace(u'{{'+i+u'}}',u'{{ابهام‌زدایی}}').replace(u'{{'+i.replace(u'ی',u'ي')+u'}}',u'{{ابهام‌زدایی}}')
    
    #الگوهای خرد
    #if text.find(u'-خرد}}')!=-1:
    #    text=subs (text)
    #الگوها و خطوط
    text = re.sub(ur'(\n\{\{.*?\}\}\n)\n+(\{\{.*?\}\}\n)',r"\1\2",text)

    #تمیزکاری خطوط
    text=text.replace(u'\n\n{{-}}\n\n',u'\n{{-}}\n').replace(u' [[پرونده:]] ',u'').replace(u'<!---->\n',u'').replace(u'<!---->',u'')
    text = re.sub('[\r\n]{3,}', "\n\n",text)
    text=text.replace(u"\n''''''\n",u"\n")

    if old_text!=text:
        if msg_short:
            msg=u'تمیز+'+msg    
        else:
            msg=u'تمیزکاری + '+msg
    text=text.replace(u'==<',u'==\n<').replace(u'>==',u'>\n==')
    return text.strip(),msg

def subs (text):
    subslinks = re.findall(ur'\{\{.*?\-خرد\}\}',text, re.S)
    tem=u'\n'
    for i in subslinks: 
        text=text.replace(i,u'')
        tem+=i+u'\n'
    tem=u'\n\n'+tem.strip()+u'\n'
    text=add_cat_top (text,tem)
    return text

def Citation_links(text,msg):
    return ref_link_correction_core.main(text,msg)

def Citation (text,msg):
    done=False
    for a in [u'{{citation',u'{{Citation']:
        if  a in text:
            subslinks=text.split(a)
            b=0
            for item in subslinks:
                b+=1
                if b==1 or a+u' needed' in item :
                    continue
                item=item.split(u'}}')[0]
                item_old=item
                count=-1
                for i in u'۰۱۲۳۴۵۶۷۸۹':
                    count+=1
                    item=item.replace(i,str(count))
                if item!=item_old:
                    text=text.replace(item_old,item)
                    done=True
    if done:
        msg=u'ارجاع+'+msg
    return text,msg

def persian_sort(categorylist):
    finallradeh,s_radeh=[],[]
    alphabets=u' ۰۱۲۳۴۵۶۷۸۹آابپتثجچحخدذرزژسشصضعغفقکگلمنوهی‌'
    for radeh in categorylist:
            radeh=radeh.replace(u'[[رده:',u'').replace(u']]',u'')
            coderadeh=radeh
            for i in range(0,len(alphabets)):    
                alphabet=alphabets[i]
                if i<10:
                    j='0'+str(i)
                else:
                    j=str(i)
                coderadeh=coderadeh.replace(alphabet,j)
            s_radeh.append(coderadeh+u'0000000000000000000@@@@'+radeh)
    s_radeh=list(set(s_radeh))
    sortedradeh=sorted(s_radeh)
    for radeh in sortedradeh:
        radeh=u'[[رده:'+radeh.split(u'@@@@')[1]+u']]'
        finallradeh.append(radeh)
    return finallradeh
    
def CatSorting(text,page,msg_short,msg=msg):
        new_text=text
        RE=re.compile(u"(\[\[رده\:(?:.+?)\]\])")
        cats=RE.findall(text)
        if not cats:
            return text,msg
        for i in cats:
                new_text=new_text.replace(i,u"")
        cats=persian_sort(cats)
        for name in cats:
            if re.search(u"\[\[(.+?)\|[ \*]\]\]",name) or u"[[رده:"+page.title()==name.split(u"]]")[0].split(u"|")[0]:
                cats.remove(name)    
                cats.insert(0, name)
        if cats==RE.findall(text):   
            return text,msg
        for i in cats:
            new_text=new_text+u"\n"+i
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(300) #if cosmetic_changes takes more than 300 sec it will aborted
        try:
            ccToolkit = cosmetic_changes.CosmeticChangesToolkit(page.site, redirect=page.isRedirectPage(), namespace = page.namespace(), pageTitle=page.title())
            new_text = ccToolkit.change(new_text)
        except TimeoutException:
            pywikibot.output(u'-----Time out--')
            pass
        signal.alarm(0)
        if msg_short:
            msg=u'مرتب+'+msg    
        else:
            msg=u' + مرتب‌سازی رده‌ها + '+msg    
        return new_text,msg

def add_cat_top (text,addtemplate):
                text=text.replace(addtemplate+u'\n',u'')
                
                if text.find(u'\n<!-- رده‌ها -->\n')!=-1:
                    num=text.find(u'\n<!-- رده‌ها -->\n')
                    text=text[:num]+addtemplate+u'\n'+text[num:]
                    return text
                    
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
                                    text+='\n'+addtemplate                                
                            except:
                                text+='\n'+addtemplate
                        else:
                            num=text.find(m.group(0))
                            text=text[:num]+addtemplate+'\n'+text[num:]
                    else:
                        text+='\n'+addtemplate
                return text
   
def tem_cleaner(text,page):
    old_text=text
    text=text.replace(u'\r',u'')
    templates=templatequery(page.title(),'fa')
    khord,tartib=u'\n',u'\n'
    if not templates:
        return old_text
    for i in templates:
        if u'{{'+i.replace(u'الگو:',u'') in text:
            temp_braket=u'{{'+i.replace(u'الگو:',u'')+text.split(u'{{'+i.replace(u'الگو:',u''))[1].split(u'}}')[0]+u'}}'
            template_sub=templatequery(i,'fa')
            if template_sub:    
                if u'الگو:الگوی خرد' in template_sub:
                        khord+=temp_braket+u'\n'
                        text=text.replace(temp_braket,u'').replace(u'}}\n\n{{',u'}}\n{{')
                for b in [u'الگو:DEFAULTSORT', u'الگو:ترتیب رده', u'الگو:تنظیم رده', u'الگو:Defaultsort', u'الگو:ترتیب پیش‌فرض']:
                    if b==i and u'{{ترتیب‌پیش‌فرض' in text:
                           text=text.replace(temp_braket,u'').replace(u'}}\n\n{{',u'}}\n{{')
                
    if u'{{ترتیب‌پیش‌فرض' in text:
        tartib=u'{{ترتیب‌پیش‌فرض'+text.split(u'{{ترتیب‌پیش‌فرض')[1].split(u'}}')[0]+u'}}'
        text=text.replace(tartib,u'').replace(u'}}\n\n{{',u'}}\n{{')
    addtext=re.sub('[\r\n]{3,}',u'\n\n',u'\n'+khord+u'\n\n'+tartib+u'\n')
    if addtext.strip():
        text=add_cat_top (text, addtext)
        text = re.sub('[\r\n]{3,}', "\n\n",text)
        text=text.replace(u'}}\n\n{{',u'}}\n{{').replace(u'}}\n\n\n[[',u'}}\n\n[[')
        if khord.strip():
            text=text.replace(u'}}'+khord,u'}}\n'+khord)
        if tartib.strip():
            text=text.replace(u'}}\n'+tartib,u'}}\n\n'+tartib)
        return text
    else:
        return old_text

def UnicodeURL(text,msg=msg):
    old_text=text
    RE=re.compile(ur'\/\/.*?(?=[\s\n\|\}\]]|$)')
    fa_Urls=RE.findall(text)
    if fa_Urls:
        for URL in fa_Urls:
            try:
                URL=URL.split('<')[0]
                new_URL=urllib.unquote(URL.encode('utf8')).decode('utf8').replace(u' ',u'%20').replace(u'{',u'%7B').replace(u'|',u'%7C').replace(u'}',u'%7D').replace(u'[',u'%5B').replace(u']',u'%5D')
                new_URL=new_URL.replace(u'"',u'%22').replace(u"'",u'%27')
                new_URL = re.sub('[\r\n\t]', "",new_URL)
                text=text.replace(URL,new_URL)
            except:
                continue
        text=re.sub(ur'\[(https?\:)(?=\/\/(?:[\w\-]+)\.(wikipedia|wikimedia|wikidata|wiktionary|wikisource|wikinews|wikivoyage|wikiquote)\.org\/[^\s\]]*)', ur'[',text)
        if old_text!=text:
            msg=u'نشانی+'+msg 
    return text,msg

def boxfind(text_en):
    text_en=text_en.replace(u'{{ ',u'{{').replace(u'{{ ',u'{{').replace(u'{{template:',u'{{').replace(u'{{Template:',u'{{').replace(u'\r',u'')
    start=False    
    box=u'\n'
    diff=1
    linebaz,linebasteh=0,0
    for our_box in boxes:
        our_box=our_box.strip()
        up_our_box=our_box[0].upper()+our_box[1:]
        lower_our_box=our_box[0].lower()+our_box[1:]
        regex_result=re.findall(u'(\{\|([\n\s]+|)\{\{([\s]+|)'+our_box+u')',text_en, re.IGNORECASE)
        if regex_result:
            if regex_result[0][0].strip():
                pre_template=u'{|'
                post_tempate=u'|}'
                text_en=text_en.replace(u'{| ',u'{|').replace(u'{| ',u'{|').replace(u'{|\n',u'{|').replace(u'{|\n',u'{|')
                text_en=text_en.replace(u' |}',u'|}').replace(u' |}',u'|}').replace(u'\n|}',u'|}').replace(u'\n|}',u'|}')
        else:
            pre_template,post_tempate=u'',u''
        lines=text_en.split('\n')
        for line in lines:
            if line==u'':
                continue
            if line.find(pre_template+u'{{'+lower_our_box)!=-1 :# lower case    
                start=True
                linebaz,linebasteh=0,0
                box+=pre_template+u'{{'+lower_our_box+line.split(pre_template+u'{{'+lower_our_box)[1]+'\n'
                linebaz += string.count( line,pre_template+"{{" )
                linebasteh += string.count( line,"}}"+post_tempate )    
                diff=linebaz-linebasteh
                continue
            if line.find(pre_template+u'{{'+up_our_box)!=-1 :# upper case
                start=True
                linebaz,linebasteh=0,0
                box+=pre_template+u'{{'+up_our_box+line.split(pre_template+u'{{'+up_our_box)[1]+'\n'
                linebaz += string.count( line,pre_template+"{{" )
                linebasteh += string.count( line,"}}" +post_tempate)
                diff=linebaz-linebasteh
                continue
            if start==True and diff!=0:
                linebaz += string.count( line,pre_template+"{{" )
                linebasteh += string.count( line,"}}"+post_tempate )
                diff=linebaz-linebasteh
                box+=line+'\n'
            if diff==0 and start==True:
                break
        if box.strip():
            break
    return box.replace(u'}}|}',u'}}\n|}')

def Get_box (txt):
    my_box=boxfind(txt)
    if my_box.strip():
        return my_box
    txt=txt.replace(u'\r',u'')
    lines=txt.split('\n')
    matn=' '
    for line in lines:
        linebaz=string.count(line,'{{')
        linebaste=string.count(line,'}}')
        diff=linebaz-linebaste
        if diff==0:
            line=line.replace('{{','$AAAA$').replace('}}','!BBBB!')
        linebaz=0
        linebaste=0
        matn+=line+u'\n'
    my_box=''
    for our_box in boxes:
        our_box=our_box.strip()
        try:
            my_box= re.search(ur'(\{\{\s*['+our_box[0].lower()+our_box[0].upper()+ur']'+our_box[1:]+ur'[_\s](?:\{\{.*?\}\}|[^\}])*\}\})',matn, re.S).group(1)# if Template box has other name please chang this regex
            my_box=my_box.replace(u'$AAAA$',u'{{').replace(u'!BBBB!',u'}}')
            break
        except:
            continue
    if not my_box.strip():
        return False
    return my_box

def reverting (text,old_text):
    #واگردانی بابت رفع باگ کد زیباسازی پای‌ویکی‌پدیا
    text=text.replace(u'< /',u'</')
    # math
    Regexs=re.compile(ur'\<math\>.*?\<\/math\>') 
    maths = Regexs.findall(text)
    old_maths = Regexs.findall(old_text)
    count=0
    for m in maths:
        text=text.replace(maths[count],old_maths[count])
        count+=1
    # source
    Regexs=re.compile(ur'(?is)<'+ur'source .*?<'+ur'/source'+ur'>') 
    sources = Regexs.findall(text)
    old_sources = Regexs.findall(old_text)
    count=0
    for source in sources:
        text=text.replace(sources[count],old_sources[count])
        count+=1
    text=text.replace(u'\r',u'')
    text=text.replace(u'==<',u'==\n<').replace(u'>==',u'>\n==')
    return text

def finall_cleaning(txt):
    #---zwnj cleaning
    txt = re.sub(u'‌{2,}', u'‌', txt)
    txt = re.sub(u'‌(?![ئاآأإژزرذدوؤةبپتثجچحخسشصضطظعغفقکگلمنهیيً\[\]ٌٍَُِّْٰٓٔكﮑﮐﮏﮎﻜﻛﻚﻙىىىﻴﻳﻲﻱﻰىىﻯيکیہەھ]|[\u0900-\u097F]|ֹ)', '', txt) # در پس
    txt = re.sub(u'(?<![ئبپتثجچحخسشصضطظعغفقکگلمنهیيًٌٍَُِّْٰٓٔك\[\]ﮑﮐﮏﮎﻜﻛﻚﻙىىىﻴﻳﻲﻱﻰىىﻯيکیہەھ]|[\u0900-\u097F]|f|ֹ)‌', '', txt) # در پیش
    return txt

def fa_cosmetic_changes(text,page,msg=msg,msg_short=True):

    old_text=text    
    old_msg=msg
    if page.namespace()==0 or testpass:#-------These functions are designed for namespace=0.
        text=text.replace(u'[[\u200c',u'[[اااااااا').replace(u']]\u200c',u']]بببببببببب')
        text=text.replace(u'\u200c[[',u'ججججججججججج[[').replace(u'\u200c]]',u'چچچچچچچچچچ]]')
        text=text.replace(u'ː',u':') #replace nostandard : with standard one
        text,msg=cleaning(text,msg_short,msg)
        if text==minor_edits(old_text):#---------------Undoing minor changes
            text=old_text
            msg=old_msg      
        text_new=tem_cleaner(text,page)
        text_new,msg=autoEdISBN(text_new,msg)
        text_new,msg=CatSorting(text_new,page,msg_short,msg)
        text_new,msg=Dictation(text_new,msg_short,msg)
        text_new,msg=UnicodeURL(text_new,msg)
        text_new,msg=Citation(text_new,msg)
        text_new,msg=Citation_links(text_new,msg)
        if text_new!=text:
            text=minor_edits(text_new)   
        msg=msg.replace(u"+(",u" (").replace(u"+ (",u" (").replace(u"++",u"+").replace(u"+ +",u"+")

        if msg.strip()==u'('+cleaning_version +u')':    
            msg=u''
        else:
            msg=u'+'+msg
        text=text.replace(u'[[اااااااا',u'[[\u200c').replace(u']]بببببببببب',u']]\u200c')
        text=text.replace(u'ججججججججججج[[',u'\u200c[[').replace(u'چچچچچچچچچچ]]',u'\u200c]]')
        text=reverting(text,old_text)
        text=text.replace(u'چچچچچچچچچچ',u'').replace(u'ججججججججججج',u'').replace(u'بببببببببب',u'').replace(u'اااااااا',u'')
        return text,cleaning_version,msg
   
def run(preloadingGen,msg):
    msg_o=msg
    for fapage in preloadingGen:
        
        #try:
            pywikibot.output(u'------fa_cosmetic_changes starting on '+fapage.title()+u' .....------------')
            msg=msg_o
            try:
                text=fapage.get()
            except:
                pywikibot.output(u'Page '+fapage.title()+u' had problem!')
                continue
            old_text=text
            text,cleaning_version,msg=fa_cosmetic_changes(text,fapage,msg=msg,msg_short=True)
            if old_text!=text and text!=minor_edits(old_text):            
                pywikibot.output(u'-------------------------------------------')
                msg=u'ربات:زیباسازی'+msg.strip()+u' ('+cleaning_version +u')'
                msg=msg.replace(u"+(",u" (").replace(u"+ (",u" (").replace(u"++",u"+").replace(u"+ +",u"+").strip()
                fapage.put(text,msg)
                msg_short=u''                
                msg=u''
        #except:
        #    continue

def fa_replaceExcept(text, old, new, exceptions,marker='', site=None):
    if site is None:
        site = pywikibot.Site()
    exceptionRegexes = {
        'comment':      re.compile(r'(?s)<!--.*?-->'),
        'header':       re.compile(r'\r?\n=+.+=+ *\r?\n'),
        'pre':          re.compile(r'(?ism)<pre>.*?</pre>'),
        'source':       re.compile(r'(?is)<'+ur'source .*?<'+ur'/source'+ur'>'),
        'category':       re.compile(ur'\[\[رده\:.*?\]\]'),
        'ref':          re.compile(r'(?ism)<ref[ >].*?</ref>'),
        'URL':         re.compile(r'\[\.*?\]'),
        'startspace':   re.compile(r'(?m)^ (.*?)$'),
        'table':        re.compile(r'(?ims)^{\|.*?^\|}|<table>.*?</table>'),
        'hyperlink':    compileLinkR(),
        'gallery':      re.compile(r'(?is)<gallery.*?>.*?</gallery>'),
        'link':         re.compile(r'\[\[[^\]\|]*(\|[^\]]*)?\]\]'),
        'file':         re.compile(ur'(\[\[پرونده\:[^\]\|]*(\|[^\]]*)?\]\])'),
        'interwiki':    re.compile(r'(?i)\[\[:?(%s)\s?:[^\]]*\]\][\s]*'
                                   % '|'.join(site.validLanguageLinks() +
                                              site.family.obsolete.keys())),
        'property':     re.compile(r'(?i)\{\{\s*#property:\s*p\d+\s*\}\}'),
        'invoke':       re.compile(r'(?i)\{\{\s*#invoke:.*?}\}'),
    }
    if isinstance(old, basestring):
        old = re.compile(old)

    dontTouchRegexes = []
    except_templates = False
    for exc in exceptions:
        if isinstance(exc, basestring):
            if exc in exceptionRegexes:
                dontTouchRegexes.append(exceptionRegexes[exc])
            elif exc == 'template':
                except_templates = True
            else:
                dontTouchRegexes.append(re.compile(r'(?is)<%s>.*?</%s>'
                                                   % (exc, exc)))
            if exc == 'source':
                dontTouchRegexes.append(re.compile(
                    r'(?is)<syntaxhighlight .*?</syntaxhighlight>'))
        else:
            dontTouchRegexes.append(exc)
    if except_templates:
        marker1 = findmarker(text)
        marker2 = findmarker(text, u'##', u'#')
        Rvalue = re.compile('{{{.+?}}}')
        Rmarker1 = re.compile('%(mark)s(\d+)%(mark)s' % {'mark': marker1})
        Rmarker2 = re.compile('%(mark)s(\d+)%(mark)s' % {'mark': marker2})
        dontTouchRegexes.append(Rmarker1)
        origin = text
        values = {}
        count = 0
        for m in Rvalue.finditer(text):
            count += 1
            while u'}}}%d{{{' % count in origin:
                count += 1
            item = m.group()
            text = text.replace(item, '%s%d%s' % (marker2, count, marker2))
            values[count] = item
        inside = {}
        seen = set()
        count = 0
        while TEMP_REGEX.search(text) is not None:
            for m in TEMP_REGEX.finditer(text):
                item = m.group()
                if item in seen:
                    continue
                seen.add(item)
                count += 1
                while u'}}%d{{' % count in origin:
                    count += 1
                text = text.replace(item, '%s%d%s' % (marker1, count, marker1))
                for m2 in Rmarker1.finditer(item):
                    item = item.replace(m2.group(), inside[int(m2.group(1))])
                for m2 in Rmarker2.finditer(item):
                    item = item.replace(m2.group(), values[int(m2.group(1))])
                inside[count] = item
    index = 0
    markerpos = len(text)
    while True:
        match = old.search(text, index)
        if not match:
            break
        nextExceptionMatch = None
        for dontTouchR in dontTouchRegexes:
            excMatch = dontTouchR.search(text, index)
            if excMatch and (
                    nextExceptionMatch is None or
                    excMatch.start() < nextExceptionMatch.start()):
                nextExceptionMatch = excMatch

        if nextExceptionMatch is not None \
                and nextExceptionMatch.start() <= match.start():
            index = nextExceptionMatch.end()
        else:
            if callable(new):
                replacement = new(match)
            else:
                new = new.replace('\\n', '\n')
                replacement = new

                groupR = re.compile(r'\\(?P<number>\d+)|\\g<(?P<name>.+?)>')
                while True:
                    groupMatch = groupR.search(replacement)
                    if not groupMatch:
                        break
                    groupID = groupMatch.group('name') or \
                              int(groupMatch.group('number'))   
                    try:
                        replacement = replacement[:groupMatch.start()] + \
                                      match.group(groupID) + \
                                      replacement[groupMatch.end():]
                    except IndexError:
                        print '\nInvalid group reference:', groupID
                        print 'Groups found:\n', match.groups()
                        raise IndexError
            text = text[:match.start()] + replacement + text[match.end():]
            break
            index = match.start() + len(replacement)
            markerpos = match.start() + len(replacement)
        
    text = text[:markerpos] + marker + text[markerpos:]

    if except_templates: 
        for m2 in Rmarker1.finditer(text):
            text = text.replace(m2.group(), inside[int(m2.group(1))])
        for m2 in Rmarker2.finditer(text):
            text = text.replace(m2.group(), values[int(m2.group(1))])
    return text

def compileLinkR(withoutBracketed=False, onlyBracketed=False):
    """Return a regex that matches external links."""
    notAtEnd = '\]\s\.:;,<>"\|\)'
    notAtEndb = '\]\s\.:;,<>"\|'
    notInside = '\]\s<>"'
    regex = r'(?P<url>http[s]?://[^%(notInside)s]*?[^%(notAtEnd)s]' \
            r'(?=[%(notAtEnd)s]*\'\')|http[s]?://[^%(notInside)s]*' \
            r'[^%(notAtEnd)s])' % {'notInside': notInside, 'notAtEnd': notAtEnd}
    regexb = r'(?P<urlb>http[s]?://[^%(notInside)s]*?[^%(notAtEnd)s]' \
            r'(?=[%(notAtEnd)s]*\'\')|http[s]?://[^%(notInside)s]*' \
            r'[^%(notAtEnd)s])' % {'notInside': notInside, 'notAtEnd': notAtEndb}
    if withoutBracketed:
        regex = r'(?<!\[)' + regex
    elif onlyBracketed:
        regex = r'\[' + regexb
    else:
        regex=r'(?:(?<!\[)'+ regex+r'|\['+regexb+')'
    linkR = re.compile(regex)
    return linkR

def templatequery(enlink,firstsite):
    if _cache.get(tuple([enlink, firstsite, 'templatequery'])):
        return _cache[tuple([enlink, firstsite, 'templatequery'])]
    temps=[]
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.split(u'#')[0].strip()
    if enlink==u'':
        _cache[tuple([enlink, firstsite, 'templatequery'])] = False
        return False    
    enlink=enlink.replace(u' ',u'_')
    site = pywikibot.Site(firstsite)
    try:
        categoryname = pywikibot.data.api.Request(site=site, action="query", prop="templates",titles=enlink,redirects=1,tllimit=500)
        categoryname=categoryname.submit()
        for item in categoryname[u'query'][u'pages']:
            templateha=categoryname[u'query'][u'pages'][item][u'templates']
            break
        for temp in templateha:
            temps.append(temp[u'title'].replace(u'_',u' '))  
        _cache[tuple([enlink, firstsite, 'templatequery'])] = temps
        return temps
    except:
        _cache[tuple([enlink, firstsite, 'templatequery'])] = False
        return False

def main():
    summary_commandline,gen = None,None
    exceptions,PageTitles,namespaces = [],[],[]
    autoText,autoTitle = False,False
    genFactory = pagegenerators.GeneratorFactory()
    for arg in pywikibot.handleArgs():
            if arg == '-autotitle':
                autoTitle = True
            elif arg == '-autotext':
                autoText = True
            elif arg.startswith( '-page:' ):
                if len(arg) == 6:
                    PageTitles.append(pywikibot.input( u'Which page do you want to chage?' ))
                else:
                    PageTitles.append(arg[6:])
            elif arg.startswith( '-cat:' ):
                if len(arg) == 5:
                    PageTitles.append(pywikibot.input( u'Which Category do you want to chage?' ))
                else:
                    PageTitles.append('Category:'+arg[5:])
            elif arg.startswith('-except:'):
                exceptions.append(arg[8:])
            elif arg.startswith( '-namespace:' ):
                namespaces.append( int( arg[11:] ) )
            elif arg.startswith( '-ns:' ):
                namespaces.append( int( arg[4:] ) )
            else:
                generator = genFactory.handleArg(arg)
    #if generator:
    gen = genFactory.getCombinedGenerator(gen)
    if PageTitles:
        pages = [pywikibot.Page(faSite,PageTitle) for PageTitle in PageTitles]
        gen = iter( pages )
    if not gen:
        pywikibot.stopme()
    if namespaces != []:    
        gen = pagegenerators.NamespaceFilterPageGenerator( gen,namespaces )
    preloadingGen = pagegenerators.PreloadingGenerator( gen,pageNumber = 60 )#---number of pages that you want load at same time
    run(preloadingGen,msg)
 
if __name__ == "__main__":
    testpass=True
    msg=u' '    
    main()
