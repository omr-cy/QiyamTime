import flet as ft
from flet_route import Params, Basket
from sys import path as syspath
from pathlib import Path
from threading import Thread
from queue import Queue
from time import sleep, strftime, localtime
BASE_DIR = Path(__file__).resolve().parent
syspath.append(str(BASE_DIR.parent))
from app import qyam_times
import json

def timeline(page: ft.Page, params: Params, basket: Basket) -> ft.View:

    result_queue = Queue()
    start_night = basket.start_night
    end_night = basket.end_night
    mode = basket.mode
    realtime_now = lambda :strftime("%I:%M:%S %p", localtime())


    view:ft.View = ft.View(
        '/timeline',
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor = ft.Colors.TRANSPARENT,
        padding=50,
        spacing=15,
        decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src=f'{BASE_DIR.parent}/assets/images/app_cover.png',
                fit=ft.ImageFit.COVER
            )
        )
    )

    ### SETUP CONTROLS ###
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
        # on_click=lambda _: page.go('/'),
        # width=15
    )

    ### SETUP THE EVENTS AND FUNCTIONS ###
    def get_times():
        times = qyam_times(start=start_night, end=end_night, mode=mode)
        result_queue.put(times)

    def show_realtime():
        # CHECK AND UPDATE TIME EVERY 1 SECOND 
        while True:
            try:
                realtime_label.value = realtime_now()
                realtime_label.update()
                sleep(1)
            except AssertionError as err:
                print(f"{err} >> Maybe The View Is Cloused")
                break

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
                    controls=[ft.IconButton(icon=ft.Icons.ACCESS_TIME,),]  
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
        sleep(1)
        if not result_queue.empty():
            page.clean()
            times = result_queue.get()
            view.controls = [
                ft.Text(value=times['city'], size=17),
                realtime_label,
                time_row(time=times['start_night'], lable='بداية الليل'),
                time_row(time=times['midnight'], lable='منتصف الليل'),
                time_row(time=times['start_off_last_third'], lable='الثلث الآخر'),
                time_row(time=times['start_off_last_sixth'], lable='السدس الآخر'),
                time_row(time=times['end_night'], lable='نهاية الليل'),
            ]
            page.update()
            # run real time in other thread
            show_realtime_thread = Thread(target=show_realtime)
            show_realtime_thread.start()
        else:
            build()
    
    def back_view(e):
        def save_log():
            with open(f'{BASE_DIR.parent}/storage/logs/log_history.json', 'w', encoding="utf-8") as jf:
                json.dump({'last_log': '/'}, jf, ensure_ascii=False, indent=4)
                
        save_log_thread = Thread(target=save_log)
        save_log_thread.start()
        page.go('/')


    ### CONNECT CONTROLS WITH EVENTS AND ACTIVEATE FUNCTIONS ###
    get_times_thread = Thread(target=get_times)
    get_times_thread.start()
    bulid_thread = Thread(target=build)
    bulid_thread.start()
    back_btn.on_click = back_view


    ### ADD CONTROLS TO VIEW ###
    view.controls = [
        ft.Column(
            alignment='center',
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                loading_progress
            ],
        )
    ]
    view.bottom_appbar = ft.BottomAppBar(
        bgcolor='#0a283f',
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            alignment='center',
            controls=[back_btn]
        ),
    )


    ### RETURN VIEW TO PAGE ###
    return view


# TIST TIMELINE PAGE
# def main(page: ft.Page):
#     page.title = "Test View"
#     v = timeline(page, Params({}), Basket())
#     page.views.append(v)
#     page.go(v.route)
# ft.app(target=main)