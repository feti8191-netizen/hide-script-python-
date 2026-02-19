import requests

def get_ip_details():
    print("🌐 --- IP GEOLOCATION TRACKER --- 🌐")
    ip_address = input("Enter IP Address to track: ")
    
    try:
        # استخدام API مجاني لجلب بيانات الموقع
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        
        print(f"\n[+] Results for: {ip_address}")
        print(f"📍 City: {response.get('city')}")
        print(f"🌍 Country: {response.get('country_name')}")
        print(f"🏢 ISP: {response.get('org')}")
        print(f"🗺️ Lat/Long: {response.get('latitude')}, {response.get('longitude')}")
        print("\n✨ Done! Stay Safe.")
        
    except Exception as e:
        print("❌ Invalid IP or Connection Error!")

get_ip_details()