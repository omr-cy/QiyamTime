import flet as ft
from flet_route import Params, Basket
from sys import path as syspath
from pathlib import Path
from threading import Thread # , Event
from queue import Queue
from time import sleep, strftime, localtime
BASE_DIR = Path(__file__).resolve().parent
syspath.append(str(BASE_DIR.parent))
from app import qyam_times
import json

def time_view(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    
    try:
        # THE OPEN FILES WAY
        with open(f'{BASE_DIR.parent}/storage/logs/user_selections.json', 'r', encoding="utf-8") as jf:
            user_selections = json.load(jf)
            start_night = user_selections["last_selected_time"]["start_night"]
            end_night = user_selections["last_selected_time"]["end_night"]
    except:
        # THE BASKET WAY
        start_night = basket.start_night
        end_night = basket.end_night

    result_queue = Queue()
    realtime_now = lambda :strftime("%I:%M:%S %p", localtime())
    is_time_view = True

    view:ft.View = ft.View(
        '/time_view',
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
        rotate=ft.Rotate(angle=3.14),
        disabled=True,
        # on_click=lambda _: page.go('/'),
        # width=15
    )

    ### SETUP THE EVENTS AND FUNCTIONS ###
    def get_times():
        times = qyam_times(start=start_night, end=end_night)
        result_queue.put(times)

    def show_realtime():
        # CHECK AND UPDATE TIME EVERY 1 SECOND
        while True:
            if not is_time_view:
                page.clean() # IMPORTINT BEFOR ANY GO    
                page.update() # DO NOT TYR TO REMOVE THIS IT WILL DROP A ' BIG BUG '
                break
            else:
                if realtime_label in view.controls:
                    try:   
                        realtime_label.value = realtime_now()
                        try:
                            realtime_label.update() # WILL GIVE YOU A BUG IF IT WITHOUT TRY, _IDONT KNOW WAY_
                        except:
                            ...
                        sleep(1)
                    except AssertionError as err:
                        print(f"{err} >> Maybe The View Is Cloused")
                    except Exception as err:
                        print(f"{err}")
            

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
                    controls=[ft.IconButton(icon=ft.Icons.ALARM,),]  
                    # controls=[ft.IconButton(icon=ft.Icons.ALARM_ADD,),]  # TODO
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
            # page.clear() # DO NOT USE NEVER THIS WILL SHOW A BUG BETWEN PAGES
            if result_queue.empty() == False: # THIS IMPORTINT CUSE ITS GETINNG THE RESUILTS FROM APP
                if is_time_view == True:
                    page.update() # I THINK IT FIXED A BUG
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
                    # run real time in other thread # THIS MORE FASTER
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

    ### CONNECT CONTROLS WITH EVENTS AND ACTIVEATE FUNCTIONS ###
    back_btn.on_click = back_view
    get_times_thread = Thread(target=get_times)
    get_times_thread.start()
    bulid_thread = Thread(target=build)
    bulid_thread.start()
    
    ### ADD CONTROLS TO VIEW ###
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
    # view.update() # DO NOT USE THIS IT WILL GIVE YOU BUG "AssertionError"

    ### RETURN VIEW TO PAGE ###
    return view


# TIST TIME_VIEW PAGE
# def main(page: ft.Page):
#     page.title = "Test View"
#     v = time_view(page, Params({}), Basket())
#     page.views.append(v)
#     page.go(v.route)
# ft.app(target=main)