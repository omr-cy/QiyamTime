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

def timeline(page: ft.Page, params: Params, basket: Basket) -> ft.View:

    result_queue = Queue()
    start_night = basket.start_night
    end_night = basket.end_night
    mode = basket.mode
    realtime_now = lambda :strftime("%I:%M:%S %p", localtime())


    view:ft.View = ft.View(
        '/timeline',
        horizontal_alignment='center',
        bgcolor = ft.Colors.TRANSPARENT,
        decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src=f'{BASE_DIR.parent}/assets/images/app_cover.png',
                fit=ft.ImageFit.COVER
            )
        )
    )


    back_home_btn:ft.IconButton = ft.IconButton(
        icon=ft.Icons.HOME,
        on_click=lambda _: page.go('/')
    )
    
    loading_progress:ft.ProgressBar = ft.ProgressBar(
        width=300, 
        color=ft.Colors.BLUE_ACCENT_400, 
        bgcolor="#eeeeee"
    )

    realtime_label:ft.Text = ft.Text(
        value='00:00:00 --',
        size=10
    )


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

    def build():
        sleep(1)
        if not result_queue.empty():
            page.clean()
            times = result_queue.get()
            view.controls = [
                back_home_btn,
                ft.Text(times['city']),
                realtime_label,
                ft.Text(times['start_night']),
                ft.Text(times['midnight']),
                ft.Text(times['start_off_last_third']),
                ft.Text(times['start_off_last_sixth']),
                ft.Text(times['end_night']),
            ]
            page.update()
            show_realtime()
        else:
            build()


    view.controls = [
        back_home_btn,
        ft.Column(
            alignment='center',
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                loading_progress
            ],
        )
    ]

    get_times_thread = Thread(target=get_times)
    get_times_thread.start()
    bulid_thread = Thread(target=build)
    bulid_thread.start()
    # show_realtime_thread = Thread(target=show_realtime)
    # show_realtime_thread.start()

    return view


# TIST TIMELINE PAGE
# def main(page: ft.Page):
#     page.title = "Test View"
#     v = timeline(page, Params({}), Basket())
#     page.views.append(v)
#     page.go(v.route)
# ft.app(target=main)