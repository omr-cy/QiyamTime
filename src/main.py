import flet as ft
from flet_route import Routing, path
from views import home
from views import timeline


def main(page: ft.Page) -> None:
    page.title = 'وقت القيام'
    page.horizontal_alignment = 'center'
    page.bgcolor = ft.Colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src='/images/app_cover.png',
            fit=ft.ImageFit.COVER
        )
    )

    app_routes = [
        path(url='/', clear=True, view=home),
        path(url='/timeline', clear=True, view=timeline)
    ]

    Routing(page=page, app_routes=app_routes)

    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")