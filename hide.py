import os
import subprocess

# 1. اسم المجلد الذي نريد إنشاؤه وقفله
folder_name = "MySecrets"
password = "123" # يمكنك تغييرها لأي كلمة سر

# وظيفة لإخفاء المجلد (قفله)
def lock():
    if os.path.exists(folder_name):
        # أمر ويندوز لجعل المجلد "ملف نظام مخفي" (قفل قوي)
        subprocess.run(['attrib', '+h', '+s', folder_name])
        print(f"🔒 Folder '{folder_name}' is now LOCKED.")
    else:
        print("❌ Folder doesn't exist!")

# وظيفة لإظهار المجلد (فتحه)
def unlock():
    user_input = input("Enter password to unlock: ")
    if user_input == password:
        subprocess.run(['attrib', '-h', '-s', folder_name])
        print(f"🔓 Folder '{folder_name}' is now UNLOCKED.")
    else:
        print("🚫 Wrong Password! Access Denied.")

# البداية: إذا كان المجلد غير موجود، نقوم بإنشائه
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"📁 Created new folder: {folder_name}")

# سؤال المستخدم: هل تريد القفل أم الفتح؟
action = input("Type 'L' to Lock or 'U' to Unlock: ").upper()

if action == "L":
    lock()
elif action == "U":
    unlock()