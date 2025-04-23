import flet as ft
from flet_route import Params, Basket
from pathlib import Path
import json
from threading import Thread
# from time import sleep

BASE_DIR = Path(__file__).resolve().parent

def selection_view(page: ft.Page, params: Params, basket: Basket) -> ft.View:

    view:ft.View = ft.View(
        '/',
        horizontal_alignment='center',
        bgcolor = ft.Colors.TRANSPARENT,
        decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src=f'{BASE_DIR.parent}/assets/images/app_cover.png',
                fit=ft.ImageFit.COVER
            )
        )
    )
    
    ### SETUP CONTROLS | تهيئة عناصر التطبيق ###
    willcome_label:ft.Text = ft.Text(
            value='مرحباً بك في تطبيق \nوقت القيام',
            text_align='center',
            rtl=True,
            size=25
        )
    auto_btn:ft.FilledTonalButton = ft.FilledTonalButton(
        # bgcolor = ft.Colors.with_opacity(color=ft.Colors.WHITE10, opacity=100),
        bgcolor=ft.Colors.WHITE10,
        height = 75,
        style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        elevation = 20,
        content = ft.Row(
            rtl = True,
            alignment='center',
            spacing=15,
            expand=True,
            controls=[
                ft.Text(
                    rtl=True,
                    expand=8,
                    spans=[
                        ft.TextSpan("\tتحديد تلقائي بالموقع", style=ft.TextStyle(size=20)),
                        ft.TextSpan("\n\tتحديد تلقائي لبداية الليل ونهايته حسب موقعك", style=ft.TextStyle(size=10, color=ft.Colors.WHITE54))
                    ],
                ),
                ft.IconButton(icon=ft.Icons.LOCATION_PIN, expand=2, icon_size=25, disabled=True),
            ],
        ),
    )
    maniual_btn:ft.FilledTonalButton = ft.FilledTonalButton(
        bgcolor=ft.Colors.WHITE10,
        elevation=20,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        height=75,
        content=ft.Row(
            rtl=True,
            alignment='center',
            spacing=15,
            expand=True,
            controls=[
                ft.Text(
                    rtl=True,
                    expand=8,
                    spans=[
                        ft.TextSpan('\tتحديد يدوي للأوقات', style=ft.TextStyle(size=20)),
                        ft.TextSpan('\n\tادخل وقت بداية الليل ونهايته حسب رغبتك', style=ft.TextStyle(size=10, color=ft.Colors.WHITE54))
                    ],
                ),
                ft.IconButton(icon=ft.Icons.ACCESS_TIME, expand=2, icon_size=25, disabled=True),
            ],
        ),
    )
    # Satrt DropDown
    start_dd = ft.Dropdown( 
        expand=True,
        width=190,
        elevation=20,
        bgcolor='#1c2739',
        border_radius=15,
        border_width=2,
        disabled=True,
        # border_color='#182745',
        # alignment=ft.CrossAxisAlignment.CENTER
    )
    # End DropDown
    end_dd = ft.Dropdown( 
        expand=True,
        width=190,
        elevation=20,
        bgcolor='#1c2739',
        border_radius=15,
        border_width=2,
        disabled=True,
        # border_color='#182745',
        # alignment=ft.CrossAxisAlignment.CENTER
    )
    time_picker:ft.TimePicker = ft.TimePicker(
        confirm_text="موافق",
        error_invalid_text="الوقت غير صحيح",
        help_text="اختر بدقة",
        cancel_text="إلغاء",
        expand=False,
        minute_label_text='الدقيقه',
        hour_label_text='الساعه',
    )
    confirm_btn:ft.TextButton = ft.TextButton(
        text='موافق',
        disabled=True,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                color=ft.Colors.INDIGO, # NOT WOARKING _IDONT KNOW WAY_
                size=15, 
                weight=ft.FontWeight.BOLD, 
                # bgcolor=ft.Colors.INDIGO_200, # _UGLY_
            ),
        ),
    )
    # Main Dialog
    paker_dlg: ft.AlertDialog = ft.AlertDialog(
        # bgcolor='#1a2f42', # OLD COLOR
        bgcolor='#EC1A2F42', # NEW COLOR
        actions_alignment='center',
        action_button_padding=30,
        content_padding=10,
        shape=ft.ContinuousRectangleBorder(radius=30),
        actions=[
            ft.TextButton(
                text='إلغاء',
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        color=ft.Colors.INDIGO, 
                        size=15, 
                        weight=ft.FontWeight.BOLD, 
                        # bgcolor=ft.Colors.INDIGO_200, # _UGLY_
                    ),
                ),
                on_click=lambda e: (
                    setattr(paker_dlg, "open", False),
                    page.update()
                )
            ),
            confirm_btn
        ]
    )   
    back_btn: ft.IconButton = ft.IconButton(
        icon=ft.Icons.ARROW_BACK_ROUNDED,
        disabled=True,
    )


    ### SETUP THE EVENTS ###
    def validate_confirm_btn(e: ft.ControlEvent):
        if start_dd.value == '00:00' or end_dd.value == '00:00':
            confirm_btn.disabled = True
        else:
            confirm_btn.disabled = False

        page.update()

    def save_log(): # SAVE LOG HISTORY
        with open(f'{BASE_DIR.parent}/storage/logs/user_selections.json', 'r', encoding="utf-8") as jf:
            user_selections = json.load(jf)

        with open(f'{BASE_DIR.parent}/storage/logs/user_selections.json', 'w', encoding="utf-8") as jf:
            user_selections["last_selected_time"] = {'start_night': start_dd.value, 'end_night': end_dd.value}
            json.dump(user_selections, jf, ensure_ascii=False, indent=4)

        with open(f'{BASE_DIR.parent}/storage/logs/log_history.json', 'w', encoding="utf-8") as jf:
            json.dump({'last_log': '/time_view'}, jf, ensure_ascii=False, indent=4)
        

    def check_logs():
        with open(f'{BASE_DIR.parent}/storage/logs/log_history.json', 'r', encoding="utf-8") as jf:
            log_history = json.load(jf)
            if log_history["last_log"] != '':
                return False # TO DEACTIVATE THE DISABLED
            else:
                return True # TO KEEP THE DISABLED

    def push_to_time_view(e: ft.ControlEvent):
        # CLOSEING THE RECENT CONTROLS TO HANDLE THE ERROES 
        paker_dlg.open = False
        time_picker.open = False

        # SAVEING LOG HISTORY
        save_log()
        # SEND THE VALUSE WITH ## BASKET WAY ##
        basket.start_night = start_dd.value
        basket.end_night = end_dd.value

        # GOING TO THE TIME VIEW PAGE
        page.go(f"/time_view")

    def save_time_from(dropdown: ft.Dropdown, tmode, tname):
        def _handler(e: ft.ControlEvent):
            with open(f'{BASE_DIR.parent}/storage/logs/user_selections.json', 'r', encoding="utf-8") as jf:
                log_time = json.load(jf)

            log_time[tmode][tname] = dropdown.value

            with open(f'{BASE_DIR.parent}/storage/logs/user_selections.json', 'w', encoding="utf-8") as jf:
                json.dump(log_time, jf, ensure_ascii=False, indent=4)

            validate_confirm_btn(e)

        return _handler
        
    def pick_time_for(dropdown: ft.Dropdown, tmode, tname):
        page.overlay.append(time_picker)
        def _show_picker(e):
            def on_time_selected(ev):
                if ev.control.value:
                    # نحول الوقت لتنسيق "ساعة:دقيقة"
                    selected_time = ev.control.value.strftime("%H:%M")
                    # نحط الوقت جوه الـ Dropdown
                    dropdown.hint_text = selected_time
                    dropdown.value = selected_time
                    validate_confirm_btn('e')
                    save_time_from(dropdown, tmode, tname)(ev)
                    # lambda save_time_from(dropdown, tmode, tname)()

            time_picker.on_change = on_time_selected
            time_picker.open = True
            page.update()

        return _show_picker

    def open_dlg_paker(tmode): # حل حلو اني اعمل فانكشن تهندل نتايج العنصر لو كان هيبقى منه نسخ كتير
        with open(f'{BASE_DIR.parent}/storage/logs/user_selections.json', 'r', encoding="utf-8") as jf:
            log_time = json.load(jf)

        if tmode == 'auto_time': # AUTO SELECTING TIME
            paker_dlg.title = ft.Text('أختر توقيت الليل', text_align='center', rtl=True) # TODO NEED TO PUT THIS TEXT "هئا الأختيار يحتاج الى انترنت في أول مرة وبعدها يحدث مرة كل شهر"

            # TO OPEN THE SELECT OPTION
            start_dd.disabled = False  if log_time[tmode]["start_night"] != "00:00" else True
            end_dd.disabled = False if log_time[tmode]["end_night"] != "00:00" else True

            # THE START DORPDOWN OPTIONS
            start_dd.value = log_time["auto_time"]["start_night"] # GETINNG THE VALUE FROM THE AUTO HISTORY LOGS
            start_dd.options = [
                ft.dropdown.Option("المغرب"),
                ft.dropdown.Option("العشاء"),
            ]
            # THE END DORPDOWN OPTIONS
            end_dd.value = log_time["auto_time"]["end_night"]  # GETINNG THE VALUE FROM THE MANUAL HISTORY LOGS
            end_dd.options = [
                ft.dropdown.Option("الفجر"), 
                ft.dropdown.Option("الشروق"),
            ]
            # start_dd.on_change = save_time_from(start_dd, tmode=tmode, tname='start_night')
            # end_dd.on_change = save_time_from(end_dd, tmode=tmode, tname='end_night')
            
        elif tmode == 'manual_time': # MANUALY SELECTING TIME
            paker_dlg.title = ft.Text('أدخل توقيت الليل', text_align='center', rtl=True)

            # TO CLOSE THE SELECT OPTION
            start_dd.disabled = True # if log_time[tmode]["start_night"] != "00:00" else False
            end_dd.disabled = True # if log_time[tmode]["end_night"] != "00:00" else False

            # THE START DORPDOWN OPTIONS
            start_dd.options = None
            start_dd.value = log_time["manual_time"]["start_night"] # GETINNG THE VALUE FROM THE AUTO HISTORY LOGS
            start_dd.hint_text = log_time["manual_time"]["start_night"]

            # THE END DORPDOWN OPTIONS
            end_dd.options = None
            end_dd.value = log_time["manual_time"]["end_night"] # GETINNG THE VALUE FROM THE AUTO HISTORY LOGS
            end_dd.hint_text = log_time["manual_time"]["end_night"]

        start_dd.on_change = save_time_from(start_dd, tmode=tmode, tname='start_night')
        end_dd.on_change = save_time_from(end_dd, tmode=tmode, tname='end_night')

        paker_dlg.content = ft.Column(
            # expand=True, # Need more learn to edit
            height=200,
            rtl=True,
            scroll=True,
            controls=[
                ft.Text('بداية الليل'),
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ACCESS_TIME,
                            on_click=pick_time_for(start_dd, tmode, 'start_night'),
                            disabled=True if tmode == 'auto_time' else False
                        ),
                        start_dd
                    ],
                ),
                ft.Text('نهاية الليل'),
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ACCESS_TIME,
                            on_click=pick_time_for(end_dd, tmode, 'end_night'),
                            disabled=True if tmode == 'auto_time' else False
                        ),
                        end_dd
                    ],
                ),
            ],
        )
        view.controls.append(paker_dlg)
        paker_dlg.open = True
        page.update() # NOT NEEDED CUSE THE VALIDATE WILL DO IT 
        validate_confirm_btn('e')


    ### CONNECT CONTROLS WITH EVENTS ###
    auto_btn.on_click = lambda _: open_dlg_paker(tmode='auto_time')
    maniual_btn.on_click = lambda _: open_dlg_paker(tmode='manual_time')
    confirm_btn.on_click = push_to_time_view
    back_btn.disabled = check_logs()
    back_btn.on_click = lambda e: page.go(f"/time_view")


    ### ADD CONTROLS TO VIEW ###
    view.controls.append(
        ft.Row(
            controls=[willcome_label],
            alignment='center',
            expand=3,
        ),
    )
    view.controls.append(
        ft.Column(
            controls=[auto_btn, maniual_btn],
            expand=7,
            spacing=10,
        )
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


# TIST SELECTION_VIEW PAGE
# def main(page: ft.Page):
#     page.title = "Test View"
#     v = selection_view(page, Params({}), Basket())
#     page.views.append(v)
#     page.go(v.route)
# ft.app(target=main)