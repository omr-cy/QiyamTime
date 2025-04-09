from os import chdir, path
import geocoder
import requests
import json
from datetime import datetime, timedelta

# Change cwd to -> fwd
chdir(path.dirname(path.abspath(__file__)))

year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")
today = datetime.now().strftime("%d %b %Y")
tomorrow = datetime.now() + timedelta(days=1)


def get_prayer_times():
    ip_location = geocoder.ip('me')
    lat, lng = ip_location.latlng
    # جلب أوقات الصلاة باستخدام الإحداثيات
    url = f"https://api.aladhan.com/v1/calendar?latitude={lat}&longitude={lng}&month={month}&year={year}&method=4"
    prayer_data = requests.get(url).json()
        
    with open(f"data/prayer_data({month}-{year}).json", "w", encoding="utf-8") as json_file:
        json.dump(prayer_data, json_file, ensure_ascii=False, indent=4)
    print(f"Saved as prayer_data({month}-{year}).json")   


def find_sunset_sunrise(today, tomorrow):
    with open(f"data/prayer_data({month}-{year}).json", "r", encoding="utf-8") as json_file:
       prayer_data = json.load(json_file)
     
    for day in prayer_data["data"]:
        if day['date']['readable'] == today:
            today_fajr = day['timings']['Fajr'].strip("(EET)")
            today_sunset = day['timings']['Sunset'].strip("(EET)")
        elif day['date']['readable'] == tomorrow:      
            tomorrow_fajr = day['timings']['Sunrise'].strip("(EET)")
             
    try:
        return (today_sunset, tomorrow_fajr)
    except:
        return (today_sunset, today_fajr)
    
    
def qyam_equaiton(today_sunset, tomorrow_fajr):
    sunset_dt = datetime.strptime(today_sunset, "%H:%M")
    fajr_dt = datetime.strptime(tomorrow_fajr, "%H:%M") + timedelta(days=1)  # إضافة يوم للشروق

    duration = fajr_dt - sunset_dt
    sixth = duration / 6
    midnight = sunset_dt + duration / 2
    fourth_and_fifth_sixth = (sunset_dt + (sixth * 4)).time()
    six_sixth = (sunset_dt + (sixth * 5)).time()
    
    print(f"All night: {duration}")
    print(f"One sixth: {sixth}")
    print(f"Midnight: {midnight.time()}")
    print(f"4 and 5 sixth starts at: {fourth_and_fifth_sixth}, ends at:{six_sixth}")
    print(f"the 6 sixth starts at: {six_sixth}")
    
    #fourth_and_fifth_sixth = (sunset_dt + sixth * 3, sunset_dt + sixth * 5)
    #return fourth_and_fifth_sixth
    


def main():
    if path.exists(f"data/prayer_data({month}-{year}).json"):
        print(f"Exists -> prayer_data({month}-{year}).json")
        today_sunset, tomorrow_fajr = find_sunset_sunrise(today, tomorrow)
        qyam_equaiton(today_sunset.strip(), tomorrow_fajr.strip())
        

    else:
        print(f"Not Exists -> prayer_data({month}-{year}).json")
        get_prayer_times()
        qyam_equaiton(today_sunset.strip(), tomorrow_fajr.strip())
        
    
main()    
     
        
        
        