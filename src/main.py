import flet as ft
# from os import path

def main(page: ft.Page) -> None:
    page.title = 'قيام الأنبياء'
    # page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.bgcolor = ft.colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            # src='/images/start_image.PNG',
            # src='/images/#FF083B5C.png',
            src='/images/#FF052E4E.png',
            fit=ft.ImageFit.COVER
        )
    )


    # Setup Controls | تهيئة عناصر التطبيق

    willcome_label:ft.Text = ft.Text(
        value='مرحباً بك في تطبيق \nقيام الأنبياء',
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
                ft.IconButton(icon=ft.Icons.LOCATION_PIN, expand=2, icon_size=25),
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
                ft.IconButton(icon=ft.Icons.ACCESS_TIME, expand=2, icon_size=25),
            ],
        ),
    )

    page.appbar = ft.AppBar(
        title=ft.Text(value='قيام الأنبياء', size=10),
        rtl=True,
        center_title=False,
        leading=ft.Icon(ft.Icons.HOME),
        leading_width=40,
        bgcolor='#FF083B5C',
        title_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        toolbar_height=45
    )


    page.add(
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
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
