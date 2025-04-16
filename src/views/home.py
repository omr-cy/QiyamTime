import flet as ft
from flet_route import Params, Basket
from os import chdir, path

# Change cwd to -> fwd
chdir(path.dirname(path.abspath(__file__)))

def home(page: ft.Page, params: Params, basket: Basket) -> ft.View:

    view:ft.View = ft.View(
        '/',
        horizontal_alignment='center',
        bgcolor = ft.Colors.TRANSPARENT,
        decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src='../assets/images/#FF052E4E.png',
                fit=ft.ImageFit.COVER
            )
        )
    )

    # SETUP CONTROLS | تهيئة عناصر التطبيق
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
                        ft.TextSpan("\tتحديد تلقائي للموقع", style=ft.TextStyle(size=20)),
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

    time_picker = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        # on_change=handle_change,
        # on_dismiss=handle_dismissal,
        # on_entry_mode_change=handle_entry_mode_change,
    )

    # model dialog
    paker_dlg: ft.AlertDialog = ft.AlertDialog(
        bgcolor='#1c2739',
        actions_alignment='center',
        action_button_padding=10,
        actions=[
            ft.ElevatedButton(
                text='إلغاء',
            ),
            ft.ElevatedButton(
                text='موافق',
            ),
        ]
    )   

    start_dd = ft.DropdownM2(
        expand=True,
        bgcolor='#FC182636',
        elevation=20,
        hint_text='-- 00:00',
    )

    end_dd = ft.Dropdown(
        expand=True,
        bgcolor='#FC182636',
        elevation=20,
        hint_text='-- 00:00'
    )
    

    # SETUP THE EVENTS
    def send_to_timeline(start_time, end_time):
        print(start_time, end_time)

    def clear_all():
        paker_dlg.content = None
        start_dd.options = None
        end_dd.options = None
        page.update()

    def open_paker_dlg(time_line_mode): # حل حلو اني اعمل فانكشن تهندل نتايج العنصر لو كان هيبقى منه نسخ كتير
        clear_all()
        global start_time
        global end_time

        if time_line_mode == 'outo': # AUTO TIMELINE
            paker_dlg.title = ft.Text('أختر توقيت الليل', text_align='center', rtl=True)

            start_dd.icon = ft.IconButton(icon=ft.Icons.ACCESS_TIME, expand=2, icon_size=25, disabled=True)
            start_dd.value = 'المغرب'
            start_dd.options = [
                ft.dropdownm2.Option("العشاء"),
                ft.dropdownm2.Option("المغرب")
            ]
            end_dd.icon = ft.IconButton(icon=ft.Icons.ACCESS_TIME, expand=2, icon_size=25, disabled=True)
            end_dd.value = 'الفجر'
            end_dd.options = [
                ft.dropdownm2.Option("الفجر"), 
                ft.dropdownm2.Option("الشروق")
            ]

        elif time_line_mode == 'manual': # MANUAL TIMELINE
            paker_dlg.title = ft.Text('أدخل توقيت الليل', text_align='center', rtl=True)

            start_dd.icon = ft.IconButton(icon=ft.Icons.ACCESS_TIME, expand=2, icon_size=25)
            end_dd.icon = ft.IconButton(icon=ft.Icons.ACCESS_TIME, expand=2, icon_size=25)

        paker_dlg.content = ft.Column(
            height=200,
            rtl=True,
            controls=[
                ft.Text('بداية الليل'),
                start_dd,
                ft.Text('نهاية الليل'),
                end_dd
            ],
        )
            
        view.controls.append(paker_dlg)
        paker_dlg.open = True
        page.update()


    # CONNECT CONTROLS WITH EVENTS
    auto_btn.on_click = lambda e: open_paker_dlg(time_line_mode='outo')
    maniual_btn.on_click = lambda e: open_paker_dlg(time_line_mode='manual')


    # ADD CONTROLS TO VIEW     
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
 
    # RETURN VIEW TO PAGE
    return view

# Tist
def main(page: ft.Page):
    page.title = "Test View"
    v = home(page, Params({}), Basket())
    page.views.append(v)
    page.go(v.route)
ft.app(target=main)