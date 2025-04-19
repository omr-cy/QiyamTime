import flet as ft
from flet_route import Params, Basket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def home(page: ft.Page, params: Params, basket: Basket) -> ft.View:

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
        # border_color='#182745',
        hint_text='--:--',
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
        # border_color='#182745',
        hint_text='--:--',
        # alignment=ft.CrossAxisAlignment.CENTER
    )

    time_picker:ft.TimePicker = ft.TimePicker(
        confirm_text="موافق",
        error_invalid_text="الوقت غير صحيح",
        help_text="اختر بدقة",
        cancel_text="إلغاء",
        expand=False,
        # hour_label_text='--'
    )

    confirm_btn:fr.IconButton = ft.ElevatedButton(
        text='موافق',
        width=90,
        height=50,
        elevation=20,
        bgcolor='#142F66',
        disabled=True,
        style=ft.ButtonStyle(
            shape=ft.ContinuousRectangleBorder(radius=30),
            # side=ft.BorderSide(2) # color='#182745'
        )
        # on_click=lambda e: page.go(f"/timeline?start_night={start_dd.value}&end_night={end_dd.value}"), ## The URL way
    )

    # Main Dialog
    paker_dlg: ft.AlertDialog = ft.AlertDialog(
        bgcolor='#1c2739',
        actions_alignment='center',
        action_button_padding=5,
        content_padding=10,
        actions=[
            ft.ElevatedButton(
                text='إلغاء',
                width=90,
                height=50,
                elevation=20,
                bgcolor='#111B2D',
                style=ft.ButtonStyle(
                    shape=ft.ContinuousRectangleBorder(radius=30),    
                    # side=ft.BorderSide(2) # color='#182745'
                ),  
                on_click=lambda e: (
                    setattr(paker_dlg, "open", False),
                    page.update()
                )
            ),
            confirm_btn
        ]
    )   


    ### SETUP THE EVENTS ###
    def validate(e: ft.ControlEvent):
        if all([start_dd.value, end_dd.value]):
            confirm_btn.disabled = False
        else:
            confirm_btn.disabled = True
        page.update()

    def push_to_timeline(e: ft.ControlEvent): ## basket way ##
        view.controls.remove(paker_dlg) # To Escbae the dlg showing error in timeline page
        view.clean() 
        page.clean()
        page.update()

        basket.start_night = start_dd.value
        basket.end_night = end_dd.value

        page.go("/timeline")
        print(f"Sending -> {start_dd.value} , {end_dd.value}")
        
    def pick_time_for(dropdown: ft.Dropdown):
        page.overlay.append(time_picker)
        def _show_picker(e):
            def on_time_selected(ev):
                if ev.control.value:
                    # نحول الوقت لتنسيق "ساعة:دقيقة"
                    selected_time = ev.control.value.strftime("%H:%M")
                    # نحط الوقت جوه الـ Dropdown
                    dropdown.hint_text = selected_time
                    dropdown.value = selected_time
                    validate('e')
                    # print(dropdown.value)
                    
            time_picker.on_change = on_time_selected
            time_picker.open = True
            page.update()

        return _show_picker

    def clear_dd():
        # paker_dlg.content = None
        start_dd.value = None #if start_dd.value in [':'] else start_dd.value
        end_dd.value = None #if start_dd.value in [':'] else start_dd.value
        start_dd.hint_text = '--:--'
        end_dd.hint_text = '--:--'
        start_dd.options = None
        end_dd.options = None
        validate('e')

    def open_dlg_paker(timeline_mode): # حل حلو اني اعمل فانكشن تهندل نتايج العنصر لو كان هيبقى منه نسخ كتير
        clear_dd()

        if timeline_mode == 'auto': # AUTO TIMELINE
            paker_dlg.title = ft.Text('أختر توقيت الليل', text_align='center', rtl=True)
            start_dd.disabled = False
            end_dd.disabled = False

            start_dd.value = 'المغرب'
            start_dd.options = [
                ft.dropdown.Option("العشاء"),
                ft.dropdown.Option("المغرب")
            ]
            end_dd.value = 'الفجر'
            end_dd.options = [
                ft.dropdown.Option("الفجر"), 
                ft.dropdown.Option("الشروق")
            ]

        elif timeline_mode == 'manual': # MANUAL TIMELINE
            paker_dlg.title = ft.Text('أدخل توقيت الليل', text_align='center', rtl=True)
            start_dd.disabled = True
            end_dd.disabled = True

        paker_dlg.content = ft.Column(
            height=160,
            rtl=True,
            controls=[
                ft.Text('بداية الليل'),
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ACCESS_TIME,
                            on_click=pick_time_for(start_dd),
                            disabled=True if timeline_mode == 'auto' else False,
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
                            on_click=pick_time_for(end_dd),
                            disabled=True if timeline_mode == 'auto' else False
                        ),
                        end_dd
                    ],
                ),
            ],
        )
           
        basket.mode = timeline_mode

        view.controls.append(paker_dlg)
        paker_dlg.open = True
        validate('e')


    ### CONNECT CONTROLS WITH EVENTS ###
    auto_btn.on_click = lambda _: open_dlg_paker(timeline_mode='auto')
    maniual_btn.on_click = lambda _: open_dlg_paker(timeline_mode='manual')
    start_dd.on_change = validate
    end_dd.on_change = validate
    confirm_btn.on_click = push_to_timeline
    

    ### ADD CONTROLS TO VIEW ###
    view.controls = [
        ft.Row(
            controls=[willcome_label],
            alignment='center',
            expand=3,
        ),
        ft.Column(
            controls=[auto_btn, maniual_btn],
            expand=7,
            spacing=10,
        )
    ]   
 
    ### RETURN VIEW TO PAGE ###
    return view


# TIST HOME PAGE
# def main(page: ft.Page):
#     page.title = "Test View"
#     v = home(page, Params({}), Basket())
#     page.views.append(v)
#     page.go(v.route)
# ft.app(target=main)