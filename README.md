# fawikibot
Collection of pywikibot-based tools for Persian Wikipedia

<div dir="rtl">
Fawikibot مجموعه‌ای از کدهای نوشته شده توسط کاربران ویکی‌پدیای فارسی است، که برای آمارگیری، گزارش‌گیری، اصلاح مقالات و صفحات و... کاربرد دارند. این کدها از کتابخانه پایتون پای‌ویکی‌بات pywikibot نسخه دوم (Core) استفاده می‌کنند. برای آشنایی با روش نصب و استفاده از این کدها و کتابخانه پای‌ویکی‌بات به ویکی‌پدیای فارسی صفحه «راهنما:شروع کار با ربات پایتون» مراجعه کنید.

**روش نصب و اجرا**

در صورتی که نام پوشه pywikibot کتابخانه core شما pycore باشد.
<div dir="ltr">
```
   git clone --recursive https://github.com/PersianWikipedia/pywikibot-core.git pycore
   cd pycore
   git submodule foreach git pull origin master
```
<div dir="rtl">

برای به‌روز رسانی کافی است دستور زیر را بنویسید.

<div dir="ltr">
```
   cd pycore
   git submodule foreach git pull origin master
```

<div dir="rtl">
برای اجرا مانند دستور زیر عمل کنید.

<div dir="ltr">
```
   cd pycore
   python pwb.py fawikibot/rade.py --newpages:100
```

<div dir="rtl">
**راهنمای کدها**

**dar.py**

ربات انتقال رده‌ها در ویکی‌پدیا:درخواست انتقال رده (وپ:دار)

**fa_cosmetic_changes_core.py**

ربات زیباسازی متن ویکی‌های فارسی

**laupdate.py**

تهیه فهرست مدیران ویکی‌پدیای فارسی در ویکی‌پدیا:فهرست مدیران

**otherwikis.py**

تهیه کوئری از تعداد مقالات جدید در ۲۴ ساعت گذشته

**rade.py**

ربات رده همسنگ که برای کتابخانه کور اصلاح شده است.

**ref_link_correction_core.py**

اصلاح پیوند فارسی موجود در ارجاع‌های لاتین و تبدیل آنها به پیوند لاتین.
