import flet as ft
from flet_route import Params, Basket
from sys import path as syspath
from pathlib import Path
from threading import Thread
from queue import Queue
from time import sleep, strftime, localtime, mktime, time
from plyer import notification

BASE_DIR = Path(__file__).resolve().parent
syspath.append(str(BASE_DIR.parent))
from app import qyam_times
import json

def time_view(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    
    try:
        with open(f'{BASE_DIR.parent}/storage/logs/user_selections.json', 'r', encoding="utf-8") as jf:
            user_selections = json.load(jf)
            start_night = user_selections["last_selected_time"]["start_night"]
            end_night = user_selections["last_selected_time"]["end_night"]
    except:
        start_night = basket.start_night
        end_night = basket.end_night

    result_queue = Queue()
    realtime_now = lambda :strftime("%I:%M:%S %p", localtime())
    is_time_view = True

    view:ft.View = ft.View(
        '/time_view',
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor=ft.Colors.TRANSPARENT,
        padding=50,
        spacing=15,
        decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src=f'{BASE_DIR.parent}/assets/images/app_cover.png',
                fit=ft.ImageFit.COVER
            )
        )
    )

    loading_progress:ft.ProgressBar = ft.ProgressBar(
        width=300,
        color=ft.Colors.BLUE_ACCENT_400, 
        bgcolor="#eeeeee"
    )

    realtime_label:ft.Text = ft.Text(
        value='00:00:00 --',
        size=20,
    )

    back_btn:ft.IconButton = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        rotate=ft.Rotate(angle=3.14),
        disabled=True,
    )

    def get_times():
        times = qyam_times(start=start_night, end=end_night)
        result_queue.put(times)

    def show_realtime():
        while True:
            if not is_time_view:
                page.clean()
                page.update()
                break
            else:
                if realtime_label in view.controls:
                    try:
                        realtime_label.value = realtime_now()
                        try:
                            realtime_label.update()
                        except:
                            ...
                        sleep(1)
                    except AssertionError as err:
                        print(f"{err} >> Maybe The View Is Cloused")
                    except Exception as err:
                        print(f"{err}")

    def alarm(time_str, label):
        def on_click(e):
            page.snack_bar = ft.SnackBar(ft.Text(f"تم ضبط المنبه لـ {label}"), open=True)
            page.update()

            def run_alarm():
                # Convert time string to seconds since epoch
                alarm_time = mktime(localtime())
                h, m = map(int, time_str.split(':'))
                now = localtime()
                alarm_time_struct = (now.tm_year, now.tm_mon, now.tm_mday, h, m, 0, now.tm_wday, now.tm_yday, now.tm_isdst)
                alarm_time_seconds = mktime(alarm_time_struct)

                # If alarm time is in the past, set it for the next day
                if alarm_time_seconds < time():
                    alarm_time_seconds += 24 * 60 * 60

                # Wait until the alarm time
                sleep(alarm_time_seconds - time())

                # Show notification
                notification.notify(
                    title="وقت القيام",
                    message=f"حان الآن وقت {label}",
                    app_name="Qiyam Time",
                    timeout=30,
                )
            
            thread = Thread(target=run_alarm)
            thread.start()

        return on_click

    def time_row(time, lable):
        return ft.Row(
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            spacing=15,
            controls=[
                ft.Column(
                    expand=True,
                    alignment='center',
                    controls=[ft.Text(value=time ,size=17)]
                ),
                ft.Column(
                    alignment='center',
                    controls=[ft.IconButton(icon=ft.Icons.ALARM_ADD, on_click=alarm(time, lable))]
                ),
                ft.Column(
                    rtl=True,
                    expand=True,
                    alignment='center',
                    controls=[ft.Text(value=lable ,size=17, rtl=True)]
                ),
            ]
        )
        
    def build():
        sleep(.2)
        while True:
            if not result_queue.empty():
                if is_time_view:
                    page.update()
                    view.controls.remove(loading_progress)
                    times = result_queue.get()
                    view.controls = [
                        ft.Text(value=times['city'], size=17, text_align='center'),
                        realtime_label,
                        time_row(time=times['start_night'], lable='بداية الليل'),
                        time_row(time=times['midnight'], lable='منتصف الليل'),
                        time_row(time=times['start_off_last_third'], lable='الثلث الآخر'),
                        time_row(time=times['start_off_last_sixth'], lable='السدس الآخر'),
                        time_row(time=times['end_night'], lable='نهاية الليل'),
                    ]
                    back_btn.disabled = False
                    page.update()
                    show_realtime_thread = Thread(target=show_realtime)
                    show_realtime_thread.start()
                    break
                else:
                    break
    
    def back_view(e: ft.ControlEvent):
        global is_time_view
        is_time_view = False
        back_btn.disabled = True
        def save_log():
            with open(f'{BASE_DIR.parent}/storage/logs/log_history.json', 'w', encoding="utf-8") as jf:
                json.dump({'last_log': '/'}, jf, ensure_ascii=False, indent=4)

        save_log()
        page.go('/')

    back_btn.on_click = back_view
    get_times_thread = Thread(target=get_times)
    get_times_thread.start()
    bulid_thread = Thread(target=build)
    bulid_thread.start()
    
    view.controls.append(
        loading_progress
    )
    view.bottom_appbar = ft.BottomAppBar(
        bgcolor='#0a283f',
        shape=ft.NotchShape.CIRCULAR,
        height=60,
        content=ft.Row(
            alignment='center',
            controls=[back_btn]
        ),
    )
    page.update()

    return view