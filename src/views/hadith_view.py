import flet as ft
from flet_route import Params, Basket
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parent

HADITHS = [
    {
        "hadith": "أَحَبُّ الصَّلَاةِ إِلَى اللَّهِ صَلَاةُ دَاوُدَ عَلَيْهِ السَّلَامُ ، وَأَحَبُّ الصِّيَامِ إِلَى اللَّهِ صِيَامُ دَاوُدَ ، وَكَانَ يَنَامُ نِصْفَ اللَّيْلِ وَيَقُومُ ثُلُثَهُ وَيَنَامُ سُدُسَهُ ، وَيَصُومُ يَوْمًا وَيُفْطِرُ يَوْمًا .",
        "source": "صحيح البخاري"
    },
    {
        "hadith": "عَلَيْكُمْ بِقِيَامِ اللَّيْلِ ، فَإِنَّهُ دَأْبُ الصَّالِحِينَ قَبْلَكُمْ ، وَهُوَ قُرْبَةٌ إِلَى رَبِّكُمْ ، وَمَكْفَرَةٌ لِلسَّيِّئَاتِ ، وَمَنْهَاةٌ لِلإِثْمِ .",
        "source": "سنن الترمذي"
    },
    {
        "hadith": "يَنْزِلُ رَبُّنَا تَبَارَكَ وَتَعَالَى كُلَّ لَيْلَةٍ إِلَى السَّمَاءِ الدُّنْيَا حِينَ يَبْقَى ثُلُثُ اللَّيْلِ الآخِرُ يَقُولُ : مَنْ يَدْعُونِي فَأَسْتَجِيبَ لَهُ ، مَنْ يَسْأَلُنِي فَأُعْطِيَهُ ، مَنْ يَسْتَغْفِرُنِي فَأَغْفِرَ لَهُ .",
        "source": "صحيح مسلم"
    }
]

def hadith_view(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    
    selected_hadith = random.choice(HADITHS)

    view = ft.View(
        '/hadith_view',
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor=ft.colors.TRANSPARENT,
        padding=30,
        spacing=30,
        decoration=ft.BoxDecoration(
            image=ft.DecorationImage(
                src=f'{BASE_DIR.parent}/assets/images/app_cover.png',
                fit=ft.ImageFit.COVER
            )
        )
    )

    hadith_text = ft.Text(
        value=selected_hadith["hadith"],
        size=20,
        text_align=ft.TextAlign.CENTER,
        rtl=True,
        weight=ft.FontWeight.BOLD
    )

    source_text = ft.Text(
        value=f"- {selected_hadith['source']} -",
        size=16,
        text_align=ft.TextAlign.CENTER,
        italic=True
    )

    back_btn = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda _: page.go('/')
    )

    view.controls.extend([
        ft.Text("أحاديث في قيام الليل", size=24, weight=ft.FontWeight.BOLD),
        hadith_text,
        source_text,
    ])

    view.bottom_appbar = ft.BottomAppBar(
        bgcolor='#0a283f',
        shape=ft.NotchShape.CIRCULAR,
        height=60,
        content=ft.Row(
            alignment='center',
            controls=[back_btn]
        ),
    )

    return view
