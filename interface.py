import customtkinter as ctk
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename
import asciimg, os, shutil

class interface(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.resizable(False, False)
        self.load_config()
        self.width = 1000
        self.height = 600
        self.font = ctk.CTkFont(family="Microsoft YaHei", size=16, weight="normal")
        self.display_center()
        self.title("Ascii Art")
        self.ita = asciimg.ImageToASCII()
        self.open_path = None
        self.temp_image = None

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
        self.image_canvas = ctk.CTkCanvas(master=self, width=self.width - 20, height=self.height - 150, background="grey", highlightthickness=1, highlightbackground="grey")
        self.open_button = ctk.CTkButton(master=self, width=120, height=80, text="打开文件", font=self.font, command=self.open_img)
        self.convert_button = ctk.CTkButton(master=self, width=120, height=80, text="转换", font=self.font, command=self.process_img)
        self.save_button = ctk.CTkButton(master=self, width=120, height=80, text="保存文件", font=self.font, command=self.output_img)

    def layup(self) -> None:
        self.image_canvas.place(anchor="nw", x=10, y=10)
        self.open_button.place(x=self.width / 2 - 250, y=self.height - 110)
        self.convert_button.place(x=self.width / 2 - 60, y=self.height - 110)
        self.save_button.place(x=self.width / 2 + 130, y=self.height - 110)
    
    def open_img(self):
        self.open_path = askopenfilename(title="打开图片", filetypes=[("image", "*.jpg *.png *.jpeg *.JPG *.PNG *.JPEG")])

    def process_img(self):
        if self.open_path is not None:
            self.temp_image = self.ita.convert(self.open_path)
            self.open_path = None

    def output_img(self):
        save_path = asksaveasfilename(title="保存图片", filetypes=[("image", "*.png")])
        if os.path.splitext(save_path)[1] != ".png" or len(os.path.splitext(save_path)[1]) == 0:
            showerror(title="错误", message="文件后缀必须为<.png>")
            return
        
        if self.temp_image is not None:
            shutil.copy(self.temp_image, save_path)
            self.temp_image = None
