import flet as ft
from flet_route import Params, Basket
import json
from pathlib import Path
from threading import Thread

BASE_DIR = Path(__file__).resolve().parent

def hadith_view(page: ft.Page, params: Params, basket :Basket) -> ft.View:
    
    view:ft.View = ft.View(
        '/hadith_view',
        horizontal_alignment = 'center',
        vertical_alignment = 'center',
        bgcolor = ft.Colors.TRANSPARENT,
        decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src=f'{BASE_DIR.parent}/assets/images/app_cover.png',
                fit=ft.ImageFit.COVER
            )
        )
    )
    

    hadith_label:ft.Row = ft.Row( 
        rtl=True,
        wrap=False,
        scroll=True,
        spacing=20,
        width=275,
        # height=250,
        )


    def ahadiths():
        with open(f'{BASE_DIR.parent}/storage/data/ahadiths.json', 'r', encoding="utf-8") as jf:
            ahadiths = json.load(jf)

        lables = []
        for value in ahadiths:
            hadith = ahadiths[value].splitlines()
            sanad = ft.TextSpan(
                text=hadith[0], # + "\n", 
                style=ft.TextStyle(color=ft.Colors.WHITE54)
            )
            nass = ft.TextSpan(
                text=hadith[1] + "\n\n",
                style=ft.TextStyle(color=ft.Colors.WHITE70, weight=ft.FontWeight.BOLD),
            )
            takhreg = ft.TextSpan(
                text=hadith[2],
                style=ft.TextStyle(color=ft.Colors.WHITE24, size=10)
            )

            lables.append(
                ft.Text(
                    text_align='center',
                    width=275,
                    height=250,
                    rtl=True,
                    spans=[
                        sanad, nass, takhreg
                    ],
                )
            )

        return lables


    hadith_label.controls = [
        *ahadiths()
    ]

    view.controls = [
        hadith_label,
    ]


    return view



# TIST HADITH_VIEW
def main(page: ft.Page):
    page.title = "Test View"
    v = hadith_view(page, Params({}), Basket())
    page.views.append(v)
    page.go(v.route)
ft.app(target=main)