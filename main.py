# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.

import smtplib                # مكتبة لإرسال الايميلات
import datetime as dt         # مكتبة لمعرفة التاريخ والوقت
import random                 # لاختيار رسالة عشوائية
import pandas                 # لقراءة ملف CSV

MY_EMAIL = "your_email@gmail.com"      # ايميل المرسل
MY_PASSWORD = "your_password"          # كلمة المرور

# الحصول على تاريخ اليوم
today = dt.datetime.now()

# تحويل التاريخ الى tuple يحتوي (الشهر ، اليوم)
today_tuple = (today.month, today.day)

# قراءة ملف birthdays.csv
data = pandas.read_csv("birthdays.csv")

# إنشاء Dictionary يكون المفتاح فيه (month, day)
# والقيمة هي بيانات الشخص في الصف
birthdays_dict = {
    (data_row.month, data_row.day): data_row
    for (index, data_row) in data.iterrows()
}

# فحص اذا كان تاريخ اليوم موجود في القاموس
if today_tuple in birthdays_dict:

    # جلب بيانات الشخص الذي عيد ميلاده اليوم
    birthday_person = birthdays_dict[today_tuple]

    # اختيار رسالة عشوائية من 1 الى 3
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"

    # فتح ملف الرسالة
    with open(file_path) as letter_file:

        contents = letter_file.read()   # قراءة محتوى الرسالة

        # استبدال كلمة [NAME] باسم الشخص
        contents = contents.replace("[NAME]", birthday_person["name"])

    # الاتصال بسيرفر ارسال الايميل (Gmail)
    with smtplib.SMTP("smtp.gmail.com") as connection:

        connection.starttls()   # جعل الاتصال مشفر وآمن

        # تسجيل الدخول الى الايميل
        connection.login(MY_EMAIL, MY_PASSWORD)

        # ارسال الرسالة
        connection.sendmail(
            from_addr=MY_EMAIL,                     # المرسل
            to_addrs=birthday_person["email"],      # المستلم
            msg=f"Subject:Happy Birthday!\n\n{contents}"   # عنوان الرسالة + النص
        )
