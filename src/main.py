import flet as ft
from flet_route import Routing, path, Params, Basket
from views import selection_view ,time_view, hadith_view
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

def main(page: ft.Page) -> None:
    page.title = 'وقت القيام'
    page.horizontal_alignment = 'center'
    page.bgcolor = ft.Colors.TRANSPARENT
    page.theme_mode = ft.ThemeMode.DARK
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src='/images/app_cover.png',
            fit=ft.ImageFit.COVER
        )
    )

    app_routes = [
        path(url='/', clear=True, view=selection_view),
        path(url='/time_view', clear=True, view=time_view),
        path(url='/hadith_view', clear=True, view=hadith_view),
    ]

    Routing(page=page, app_routes=app_routes)

    with open(f'{BASE_DIR}/storage/logs/log_history.json', 'r', encoding="utf-8") as jf:
        history = json.load(jf)  

    if history["last_log"] == "":
        page.go(page.route)
        
    else:
        page.go(history["last_log"])


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")