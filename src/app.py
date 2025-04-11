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
    
    
def qyam_calc(start_night, end_night):
    start_night_dt = datetime.strptime(start_night, "%H:%M")
    end_night_dt = datetime.strptime(end_night, "%H:%M") + timedelta(days=1)  # إضافة يوم للشروق

    duration = end_night_dt - start_night_dt
    sixth = duration / 6
    midnight = start_night_dt + duration / 2
    last_third = (start_night_dt + (sixth * 4)).time()
    # importent not "السدسي الرابع والخامس يبدأنان من منتصف الليل وينتهيان في اول السدس الأخير " 
    six_sixth = (start_night_dt + (sixth * 5)).time()
    
    calculation =  {
        "allnight": str(duration),
        "start_night": start_night,    
        "midnight": str(midnight.time()),
        "start_off_last_third": str(last_third),  
        "start_off_last_sixth": str(six_sixth),
        "end_night": end_night 
    }
    
    print(calculation)
    return calculation
    
    
def qyam_equaiton(start, end, auto_calc=True):
    
    try: # علشان لو المستخدم غير اللوكيشن يتم اعادة بناء ملف اوقات الصلاوات على اللوكيشن الجديد
        thread = Thread(target=get_prayer_times)
        thread.start() #  وضعتها في ثريد علشان متأثرش على باقي التطبيق 
    except:
        pass
    
    if auto_calc: # لو سيتم حساب الوقت تلقائي
    
        start_time = start.capitalize()
        end_time = end.capitalize()
        
        if path.exists(f"data/prayer_data({month}-{year}).json"):
            with open(f"data/prayer_data({month}-{year}).json", "r", encoding="utf-8") as json_file:
                prayer_data = json.load(json_file)
                
                return qyam_calc(
                    *fetch_night_times(
                        prayer_data,
                        start_time=start_time,
                        end_time=end_time
                    )
                )
                
        else:
            get_prayer_times()
            with open(f"data/prayer_data({month}-{year}).json", "r", encoding="utf-8") as json_file:
                prayer_data = json.load(json_file)
                
                return qyam_calc(
                    *fetch_night_times(
                        prayer_data,
                        start_time=start_time,
                        end_time=end_time
                    )
                )
        
    else: # لو سيتم حساب الوقت يدوي
        
        return qyam_calc(start, end)
    
    
qyam_equaiton("isha", "fajr")
#qyam_equaiton("sunset", "sunrise")
#qyam_equaiton("isha", "sunrise")
#qyam_equaiton("06:18", "4:0", auto_calc=False)

     
        
        
        