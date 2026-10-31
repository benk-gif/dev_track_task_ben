
import flet as ft
import flet_audio as fta
import asyncio
import random


def main(page: ft.Page):
    page.title = "Text Combiner"
    page.bgcolor = "#EAF3FF"
    page.padding = 0

    first_name = ft.TextField(label="First Name", width=300)
    last_name = ft.TextField(label="Last Name", width=300)

    greeting = ft.Text(
        size=20,
        color="#164A8A"
    )

    image_files = [
        "WU_TANG.jpg",
        "wu_tang.jpg",
        "wu.jpg",
        "tang.jpg"
    ]

    pictures = []

    for filename in image_files:
        pictures.append(
            ft.Container(
                content=ft.Image(
                    src=filename,
                    width=150,
                    height=120,
                    fit=ft.BoxFit.CONTAIN
                ),
                width=150,
                height=120,
                left=0,
                top=0,
                visible=False
            )
        )

    ben_picture = ft.Image(
        src="ben.jpeg",
        width=260,
        height=260,
        fit=ft.BoxFit.CONTAIN,
        visible=False
    )

    ben_label = ft.Text(
        "BEN KRAUS!!!!",
        size=38,
        weight=ft.FontWeight.BOLD,
        color="#164A8A",
        visible=False
    )

    audio = fta.Audio(
        src="cream.mp3",
        release_mode=fta.ReleaseMode.LOOP
    )

    ben_audio = fta.Audio(
        src="ben.mp3"
    )

    hacker_audio = fta.Audio(
        src="hacker.mp3",
        release_mode=fta.ReleaseMode.LOOP
    )

    page.services.extend([
        audio,
        ben_audio,
        hacker_audio
    ])

    animation_id = 0
    secret_active = False

    async def stop_all_audio():
        await audio.pause()
        await ben_audio.pause()
        await hacker_audio.pause()

    async def stop_egg():
        nonlocal animation_id

        animation_id += 1

        for picture in pictures:
            picture.visible = False

        ben_picture.visible = False
        ben_label.visible = False

        await stop_all_audio()

        page.update()

    
    async def animate(my_id):
        while my_id == animation_id and not secret_active:
            max_left = max(0, int(page.width or 900) - 160)
            max_top = max(0, int(page.height or 650) - 130)

            for picture in pictures:
                picture.left = random.randint(0, max_left)
                picture.top = random.randint(0, max_top)

            page.update()

            await asyncio.sleep(0.8)

    
    def show_main():
        nonlocal secret_active

        secret_active = False

        page.clean()
        page.bgcolor = "#EAF3FF"

        app_content = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Text Combiner",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="#164A8A"
                    ),

                    first_name,
                    last_name,

                    ft.Button(
                        "Combine",
                        on_click=say_hello,
                        bgcolor="#2563EB",
                        color="white"
                    ),

                    greeting,
                    ben_label,
                    ben_picture
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                scroll=ft.ScrollMode.AUTO
            )
        )

        page.add(
            ft.Stack(
                expand=True,
                controls=[
                    app_content,
                    *pictures
                ]
            )
        )

        page.update()


    async def show_secret():
        nonlocal secret_active, animation_id

        secret_active = True
        animation_id += 1

        await stop_all_audio()

        page.clean()
        page.bgcolor = "#050505"

        terminal_text = ft.Text(
            "",
            color="#00FF41",
            size=16,
            font_family="monospace"
        )

        status = ft.Text(
            "SYSTEM INITIALIZING...",
            color="#00FF41",
            size=14
        )

        async def startup():
            messages = [
                "INITIALIZING SECRET MODE...",
                "CONNECTING TO MAINFRAME...",
                "BYPASSING FIREWALL...",
                "ENCRYPTION CHECK: PASSED",
                "ACCESS GRANTED.",
                "WELCOME, BEN KRAUS."
            ]

            for message in messages:
                if not secret_active:
                    return

                terminal_text.value += message + "\n"

                page.update()

                await asyncio.sleep(0.65)

            if secret_active:
                status.value = "SYSTEM READY"
                page.update()

        async def exit_secret(e):
            nonlocal secret_active, animation_id

            secret_active = False
            animation_id += 1

            await stop_all_audio()

            show_main()

        async def self_destruct(e):
            nonlocal secret_active, animation_id

            secret_active = False
            animation_id += 1

            await stop_all_audio()

            page.clean()
            page.bgcolor = "#000000"

            page.add(
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "SYSTEM TERMINATED",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                color="#FF3030"
                            ),

                            ft.Text(
                                "ALL SYSTEMS SHUT DOWN.",
                                color="#00FF41",
                                size=16
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )

            page.update()

        secret_screen = ft.Container(
            expand=True,
            padding=25,
            bgcolor="#050505",
            content=ft.Column(
                controls=[
                    ft.Text(
                        "S E C R E T   M O D E",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="#00FF41"
                    ),

                    ft.Text(
                        "BEN KRAUS // CLASSIFIED TERMINAL",
                        color="#008F11",
                        size=13
                    ),

                    ft.Divider(color="#008F11"),

                    terminal_text,
                    status,

                    ft.Divider(color="#008F11"),

                    ft.Row(
                        controls=[
                            ft.Button(
                                "EXIT",
                                on_click=exit_secret,
                                bgcolor="#2563EB",
                                color="white"
                            ),

                            ft.Button(
                                "SELF DESTRUCT",
                                on_click=self_destruct,
                                bgcolor="#B91C1C",
                                color="white"
                            )
                        ],
                        wrap=True
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=15
            )
        )

        page.add(secret_screen)
        page.update()

        await hacker_audio.play()
        await startup()

    # Combine button
    async def say_hello(e):
        nonlocal animation_id

        first = (first_name.value or "").strip().upper()
        last = (last_name.value or "").strip().upper()

        await stop_egg()

        if first == "WU" and last == "TANG":
            animation_id += 1
            current_id = animation_id

            greeting.value = "WUUUU TANG!!!"

            for picture in pictures:
                picture.visible = True

            page.update()

            await audio.play()

            page.run_task(animate, current_id)

        elif first == "BEN" and last == "KRAUS":
            greeting.value = ""

            ben_label.visible = True
            ben_picture.visible = True

            page.update()

            await ben_audio.play()

        elif first == "SECRET" and last == "MODE":
            greeting.value = ""

            await show_secret()

        else:
            greeting.value = "Hello, " + first_name.value.strip() + " " + last_name.value.strip()

            page.update()

    show_main()


ft.run(
    main,
    view=ft.AppView.WEB_BROWSER,
    assets_dir="assets"
)
