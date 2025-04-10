from os import chdir, path
from geocoder import ip
import requests
import json
from datetime import datetime, timedelta
from threading import Thread

# Change cwd to -> fwd
chdir(path.dirname(path.abspath(__file__)))

year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")
today = datetime.now().strftime("%d %b %Y")
tomorrow = datetime.now() + timedelta(days=1)


def get_prayer_times():
    ip_location = ip('me')
    lat, lng = ip_location.latlng
    # جلب أوقات الصلاة باستخدام الإحداثيات
    url = f"https://api.aladhan.com/v1/calendar?latitude={lat}&longitude={lng}&month={month}&year={year}&method=4"
    prayer_data = requests.get(url).json()
        
    with open(f"data/prayer_data({month}-{year}).json", "w", encoding="utf-8") as json_file:
        json.dump(prayer_data, json_file, ensure_ascii=False, indent=4)
    print(f"Saved as prayer_data({month}-{year}).json")   


def fetch_night_times(prayer_data, start_time="Isha", end_time="Fajr"):
     
    for day in prayer_data["data"]:
        if day['date']['readable'] == today:
            today_night_end_time = day['timings'][end_time].strip("(EET)")
            night_start_time = day['timings'][start_time].strip("(EET)")
        elif day['date']['readable'] == tomorrow:      
            tomorrow_night_end_time = day['timings'][end_time].strip("(EET)")
             
    try:
        return (night_start_time.strip(), tomorrow_night_end_time.strip())
    except:
        return (night_start_time.strip(), today_night_end_time.strip())
    
    
def qyam_equaiton(start_night, end_night):
    start_night_dt = datetime.strptime(start_night, "%H:%M")
    end_night_dt = datetime.strptime(end_night, "%H:%M") + timedelta(days=1)  # إضافة يوم للشروق

    duration = end_night_dt - start_night_dt
    sixth = duration / 6
    midnight = start_night_dt + duration / 2
    fourth_and_fifth_sixth = (start_night_dt + (sixth * 4)).time()
    six_sixth = (start_night_dt + (sixth * 5)).time()
    
    #print(f"All night: {duration}")
    #print(f"One sixth: {sixth}")
    #print(f"Midnight: {midnight.time()}")
    #print(f"4 and 5 sixth starts at: {fourth_and_fifth_sixth}, ends at:{six_sixth}")
    #print(f"the 6 sixth starts at: {six_sixth}")
    
    calculation =  {
        "allnight": str(duration),
        "midnight": str(midnight.time()),
        "fourth_and_fifth_sixth": str(fourth_and_fifth_sixth),
        "six_sixth": str(six_sixth)        
    }
    
    print(calculation)
    return calculation
    
    
def main():
    if path.exists(f"data/prayer_data({month}-{year}).json"):
        #print(f"Exists -> prayer_data({month}-{year}).json")
        with open(f"data/prayer_data({month}-{year}).json", "r", encoding="utf-8") as json_file:
            prayer_data = json.load(json_file)
            qyam_equaiton(*fetch_night_times(prayer_data))
        

    else:
        #print(f"Not Exists -> prayer_data({month}-{year}).json")
        get_prayer_times()
        with open(f"data/prayer_data({month}-{year}).json", "r", encoding="utf-8") as json_file:
            prayer_data = json.load(json_file)
            
            qyam_equaiton(today_sunset.strip(), tomorrow_fajr.strip())
        
    
main()    
     
        
        
        