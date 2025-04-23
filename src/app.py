import json
import requests
from geocoder import ip
from pathlib import Path
from threading import Thread
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent

now = datetime.now()
today = now.strftime("%d %b %Y")
tomorrow = now + timedelta(days=1)
current_date = now.strftime('%m-%Y').split('-')

def get_prayer_times():
    try:
        ip_location = ip('me')
        lat, lng = ip_location.latlng
        city = ip_location.city

        # جلب أوقات الصلاة باستخدام الإحداثيات
        url = f"https://api.aladhan.com/v1/calendar?latitude={lat}&longitude={lng}&month={current_date[0]}&year={current_date[1]}&method=4"
        prayer_data = requests.get(url).json()
        prayer_data['city'] = city  # add city name

        with open(f"{BASE_DIR}/storage/data/prayer_data({current_date[0]}-{current_date[1]}).json", "w", encoding="utf-8") as json_file:
            json.dump(prayer_data, json_file, ensure_ascii=False, indent=4)
        print(f"Saved as prayer_data({current_date[0]}-{current_date[1]}).json") 

    except Exception as err:
        print(err)

def fetch_night_times(prayer_data, start_time="Isha", end_time="Fajr"):
    city = prayer_data["city"]
    for day in prayer_data["data"]:
        if day['date']['readable'] == today:
            today_night_end_time = day['timings'][end_time].strip("(EET)")
            night_start_time = day['timings'][start_time].strip("(EET)")
        elif day['date']['readable'] == tomorrow:      
            tomorrow_night_end_time = day['timings'][end_time].strip("(EET)")
             
    try:
        return (night_start_time.strip(), tomorrow_night_end_time.strip(), city)
    except:
        return (night_start_time.strip(), today_night_end_time.strip(), city)
    
def conv_time_12h(time_str):
    for fmt in ('%H:%M', '%H:%M:%S'):
        try:
            time_obj = datetime.strptime(str(time_str), fmt)
            return time_obj.strftime("%I:%M %p")
        except ValueError:
            continue
    return f"Time Format Erro -> {time_str}"

def qyam_calc(start_night, end_night, city='--------'):
    start_night_dt = datetime.strptime(start_night, "%H:%M")
    end_night_dt = datetime.strptime(end_night, "%H:%M") + timedelta(days=1)  # إضافة يوم للشروق

    duration = end_night_dt - start_night_dt
    sixth = duration / 6
    midnight = (start_night_dt + duration / 2).time()
    last_third = (start_night_dt + (sixth * 4)).time()
    # importent note "السدسي الرابع والخامس يبدأنان من منتصف الليل وينتهيان في اول السدس الأخير " 
    six_sixth = (start_night_dt + (sixth * 5)).time()
    
    calculation =  {
        'city': city,
        "allnight": str(duration),
        "start_night": conv_time_12h(start_night),    
        "midnight": conv_time_12h(midnight),
        "start_off_last_third": conv_time_12h(last_third),  
        "start_off_last_sixth": conv_time_12h(six_sixth),
        "end_night": conv_time_12h(end_night)
    }
    return calculation
    
    
def qyam_times(start, end):
    auto_times = {
        'المغرب':'Sunset', 
        'العشاء' : 'Isha', 
        'الشروق':'Sunrise',  
        'الفجر': 'Fajr'
    }

    # thread = Thread(target=get_prayer_times) # TODO
    # thread.start() #  وضعتها في ثريد علشان متأثرش على باقي التطبيق 
   
    if start in auto_times and end in auto_times: # لو سيتم حساب الوقت تلقائي
        start_time = auto_times[start]
        end_time = auto_times[end]
        
        if Path(f"{BASE_DIR}/storage/data/prayer_data({current_date[0]}-{current_date[1]}).json").exists():
            # IF PRAYER DATA EXISTS WILL GET THE DATA FROM IT
            with open(f"{BASE_DIR}/storage/data/prayer_data({current_date[0]}-{current_date[1]}).json", "r", encoding="utf-8") as json_file:
                prayer_data = json.load(json_file)
                
                return qyam_calc(
                    *fetch_night_times(
                        prayer_data,
                        start_time=start_time,
                        end_time=end_time
                    )
                )
                
        else:
            # IF PRAYER DATA IS NOT EXISTS WILL RUN get_prayer_times TO GET THE DATA
            try:
                get_prayer_times()

                with open(f"{BASE_DIR}/storage/data/prayer_data({current_date[0]}-{current_date[1]}).json", "r", encoding="utf-8") as json_file:
                    prayer_data = json.load(json_file)
                    return qyam_calc(
                        *fetch_night_times(
                            prayer_data,
                            start_time=start_time,
                            end_time=end_time
                        )
                    )

            except Exception as err:
                print (err)
                return {
                    'city': "حدثت مشكلة\nلا يجود انترنت أو تحتاج لتحديث موقعك",
                    "allnight": "00:00:00",
                    "start_night": "00:00:00",  
                    "midnight": "00:00:00",  
                    "start_off_last_third": "00:00:00",  
                    "start_off_last_sixth": "00:00:00",  
                    "end_night": "00:00:00",  
                }

    else: # لو سيتم حساب الوقت يدوي
        
        return qyam_calc(start, end)


# TIST APP
# print(qyam_times("المغرب", "الشروق"))
# qyam_times("العشاء", "fajr")
# qyam_times("sunset", "sunrise")
# qyam_times("isha", "sunrise")
# qyam_times("06:18", "4:0")