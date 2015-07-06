# fawikibot
Collection of pywikibot-based tools for Persian Wikipedia

<div dir="rtl">
**روش نصب و اجرا**
</div>
```
   git clone --recursive https://github.com/PersianWikipedia/pywikibot-core.git pwb
   cd pwb
   git submodule foreach git pull origin master
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
</div>
