import customtkinter as ctk

class interface(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.load_config()
        self.width = 1000
        self.height = 600
        self.font = ctk.CTkFont(family="Microsoft YaHei", size=16, weight="normal")
        self.display_center()
        self.title("Ascii Art")

    def load_config(self) -> None:
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        ctk.deactivate_automatic_dpi_awareness()
    
    def display_center(self) -> None:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_size = f"{self.width}x{self.height}+{int((screen_width - self.width) / 2)}+{int((screen_height - self.height) / 2)}"
        self.geometry(window_size)

    def layout(self) -> None:
        pass
    
    def layup(self) -> None:
        pass
        

if __name__ == "__main__":
    app = interface()
    app.layout()
    app.layup()
    app.mainloop()
