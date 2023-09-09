from voice import Voice
import model
import flet as ft
import os

voice = Voice()

def getSettings(type: str):
    if not os.path.isfile("ui_config.ini"):
            with open("ui_config.ini", "w") as file:
                file.write("Theme = dark\n")
            print("Was created ui_config.ini")
    
    with open("ui_config.ini", 'r') as file:
        theme = file.readline()[8:-1].lower()

        if type == "theme": return theme

def main(page: ft.Page):
    page.title = "Voice assistant"
    page.window_width = 420
    page.window_height = 500
    page.theme_mode = getSettings("theme")

    progress_voice_assistant = ft.ProgressRing(scale=1.75, color = ft.colors.BLUE, visible = False)

    def speech():
        progress_voice_assistant.visible = True
        progress_voice_assistant.update()
        
        voice.speechToText()

        listTileQuestion.title = ft.Text(voice.resultSTT)
        listTileQuestion.update()

        progress_voice_assistant.color = ft.colors.GREEN
        progress_voice_assistant.update()

        model_result = model.ask(voice.resultSTT)

        progress_voice_assistant.color = ft.colors.PURPLE
        progress_voice_assistant.update()

        voice.textToSpeech(model_result)

        listTileAnswer.title = ft.Text(model_result)
        listTileAnswer.update()

        progress_voice_assistant.color = ft.colors.BLUE
        progress_voice_assistant.visible = False
        progress_voice_assistant.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        try:
            selected_files.value = (
            "\n".join(map(lambda f: f.name, e.files)) if e.files else "")
            selected_files.update()
        except:
            pass

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text(size = 20)

    page.overlay.append(pick_files_dialog)

    listTileQuestion = ft.ListTile(
                            leading=ft.Icon(ft.icons.QUESTION_ANSWER),
                            title=ft.Text("Ваш вопрос будет тут"),
                            selected=True,
                        )
                        
    listTileAnswer = ft.ListTile(
                            title=ft.Text("Ваш ответ будет тут"))

    card = ft.Container(
                width = 375,
                border_radius = 40,
                bgcolor = ft.colors.BLACK45,
                content = ft.Column(
                    [   
                        listTileQuestion,
                        listTileAnswer
                        # ft.ListTile(
                        #     leading=ft.Icon(ft.icons.QUESTION_ANSWER),
                        #     title=ft.Text("One-line selected list tile"),
                        #     selected=True,
                        # ),
                        # ft.ListTile(
                        #     title=ft.Text("One-line with leading control"),
                        # )
                    ],
                    spacing = 0,
                ),
                padding = ft.padding.symmetric(vertical = 10),
            )

    tab_assistant = ft.Container(
        ft.Stack([
            ft.Column(
                [
                ft.Container(
                    ft.Stack([
                        ft.Column([card]),
                        ft.Column([progress_voice_assistant], top = 310, left = 160),
                        ft.Column([
                            ft.IconButton(icon = ft.icons.KEYBOARD_VOICE, icon_size = 40, bgcolor = ft.colors.BLUE,
                            on_click = lambda x: speech()),
                        ],
                        top = 300,
                        left = 150)
                    ]),
                    border_radius = 40,
                    padding = 5,
                    width = 390,
                    height = 380,
                    bgcolor = ft.colors.BLACK26)
                ],
                top = 15)
        ]), 
        bgcolor = ft.colors.TRANSPARENT)

    tab_upload = ft.Container(
        ft.Stack([
            ft.Column(
                [
                ft.Container(
                    ft.Stack([
                        ft.Row([
                            ft.OutlinedButton(text="Выбрать файлы",
                                on_click = lambda x: pick_files_dialog.pick_files(allow_multiple=True)),
                            
                            ft.IconButton(icon = ft.icons.FILE_UPLOAD, )
                        ],
                        top = 15,
                        left = 100),

                        ft.Column([
                            selected_files],
                        top = 60,
                        left = 20)
                    ]),
                    border_radius = 40,
                    padding = 5,
                    width = 390,
                    height = 380,
                    bgcolor = ft.colors.BLACK26)
                ],
                top = 15)
        ]), 
        bgcolor = ft.colors.TRANSPARENT)

    tab_settings = ft.Container(
        ft.Stack([
            ft.Column(
                [
                ft.Container(
                    ft.Stack([
                        ft.Column([
                            ft.Switch(label = "Темная тема", value = True if getSettings("theme") == "dark" else False)
                        ],
                        top = 20,
                        left = 20)
                    ]),
                    border_radius = 40,
                    padding = 5,
                    width = 390,
                    height = 380,
                    bgcolor = ft.colors.BLACK26)
                ],
                top = 15)
        ]), 
        bgcolor = ft.colors.TRANSPARENT)

    tabs = ft.Tabs(
            selected_index = 0,
            animation_duration = 300,
            tabs=[
                ft.Tab(
                    text = "Асистент",
                    icon = ft.icons.KEYBOARD_VOICE,
                    content = tab_assistant),
                ft.Tab(
                    text = "Загрузить",
                    icon = ft.icons.UPLOAD_FILE_OUTLINED,
                    content = tab_upload,
                ),
                ft.Tab(
                    text = "Настройки",
                    icon = ft.icons.SETTINGS,
                    content = tab_settings),
            ],
            expand=1,
        )

    page.add(tabs)
    page.update()

ft.app(target=main)