import flet as ft
from widgets import my_appbar

def main(page: ft.Page) -> None:
    page.title = "قيام الأنبياء"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    
    
    # Setup Controls | تهيئة عناصر التطبيق
    page.appbar = my_appbar()
    









    page.update()
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
