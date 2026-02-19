import os
import shutil

# مسارات الملفات المؤقتة في ويندوز
folders = [
    r'C:\Windows\Temp', 
    r'C:\Users\{}\AppData\Local\Temp'.format(os.getlogin())
]

print("🚀 Starting PC Cleanup...")

for folder in folders:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) # مسح الملف
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path) # مسح المجلد
            print(f"✅ Deleted: {filename}")
        except Exception as e:
            print(f"❌ Could not delete: {filename}")

print("✨ System Cleaned Successfully!")