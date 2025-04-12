from flet import (
    AppBar,
    Icon,
    IconButton,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Text,
    colors,
    icons,
)


my_appbar:AppBar = AppBar(
    leading=Icon(icons.PALETTE),
    leading_width=40,
    title=Text("قيام الأنبياء"),
    center_title=False,
    bgcolor=colors.SURFACE_VARIANT,
    actions=[
        IconButton(icons.WB_SUNNY_OUTLINED),
        IconButton(icons.FILTER_3),
        PopupMenuButton(
            items=[
                PopupMenuItem(text="Item 1"),
                PopupMenuItem(),  # divider
                # PopupMenuItem(
                #     text="Checked item", checked=False, # on_click=check_item_clicked
                # ),
            ]
        ),
    ],
)
