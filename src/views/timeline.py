import flet as ft
from flet_route import Params, Basket
from os import chdir, path

# Change cwd to -> fwd
chdir(path.dirname(path.abspath(__file__)))

def timeline(page: ft.Page, params: Params, basket: Basket) -> ft.View:

    start_night = basket.start_night
    end_night = basket.end_night
    mode = basket.mode

    view:ft.View = ft.View(
        '/timeline',
        horizontal_alignment='center',
        bgcolor = ft.Colors.TRANSPARENT,
        decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src='../assets/images/#FF052E4E.png',
                fit=ft.ImageFit.COVER
            )
        )
    )


    back_home_btn:ft.IconButton = ft.IconButton(
        icon=ft.Icons.HOME,
        on_click=lambda _: page.go('/')
    )
    
    view.controls = [
        back_home_btn,
        ft.Text(f'{start_night}\n{end_night}\n{mode}')
    ]

    return view


# TIST TIMELINE PAGE
# def main(page: ft.Page):
#     page.title = "Test View"
#     v = timeline(page, Params({}), Basket())
#     page.views.append(v)
#     page.go(v.route)
# ft.app(target=main)