import flet as ft

class ProcessingCard(ft.Container):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.check_icon = ft.Icon(name=ft.icons.CHECK, color=ft.colors.GREY)
        self.label = ft.Text(value=self.text)
        self.progress_bar = ft.ProgressBar(width=400)
        self.progress_ring = ft.ProgressRing(visible=False, width=20, height=20)

        self.row = ft.Row(
            controls=[
                self.check_icon,
                self.label,
            ],
            alignment=ft.MainAxisAlignment.START
        )

        # Configurações do Container
        self.content = self.row
        self.padding = 10
        self.border_radius = 15
        self.bgcolor = ft.colors.WHITE
        self.margin = 10

    def update_check(self, is_complete):
        self.check_icon.color = ft.colors.GREEN if is_complete else ft.colors.GREY
        self.update()

    def toggle_loading(self, is_loading):
        if is_loading:
            if self.label.value.startswith("Video"):
                if self.progress_bar not in self.row.controls:
                    self.row.controls.append(self.progress_bar)
            else:
                if self.progress_ring not in self.row.controls:
                    self.row.controls.append(self.progress_ring)
                self.progress_ring.visible = is_loading
        else:
            if self.label.value.startswith("Video"):
                if self.progress_bar in self.row.controls:
                    self.row.controls.remove(self.progress_bar)
            else:
                self.progress_ring.visible = is_loading
        self.update()

    def update_progress(self, current, total):
        self.progress_bar.value = current / total
        self.update()
