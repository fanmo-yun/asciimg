import customtkinter as ctk
from tkinter.messagebox import showerror, showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import asciimg, os, shutil
from PIL import Image, ImageTk

class interface(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.resizable(False, False)
        self.load_config()
        self.width = 1000
        self.height = 600
        self.canvas_w = self.width - 20
        self.canvas_h = self.height - 150
        self.button_w = 120
        self.button_h = 80
        self.font = ctk.CTkFont(family="Microsoft YaHei", size=16, weight="normal")
        self.display_center()
        self.title("Ascii Art")
        self.ita = asciimg.ImageToASCII()
        self.open_path = None
        self.canvas_img = None
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
        self.image_canvas = ctk.CTkCanvas(master=self, width=self.canvas_w, height=self.canvas_h, background="grey", highlightthickness=1, highlightbackground="grey")
        self.open_button = ctk.CTkButton(master=self, width=self.button_w, height=self.button_h, text="打开文件", font=self.font, command=self.open_img)
        self.convert_button = ctk.CTkButton(master=self, width=self.button_w, height=self.button_h, text="转换", font=self.font, command=self.process_img)
        self.save_button = ctk.CTkButton(master=self, width=self.button_w, height=self.button_h, text="保存文件", font=self.font, command=self.output_img)

    def layup(self) -> None:
        self.image_canvas.place(anchor="nw", x=10, y=10)
        self.open_button.place(x=self.width / 2 - 250, y=self.height - 110)
        self.convert_button.place(x=self.width / 2 - 60, y=self.height - 110)
        self.save_button.place(x=self.width / 2 + 130, y=self.height - 110)
    
    def open_img(self):
        self.open_path = askopenfilename(title="打开图片", filetypes=[("image", "*.jpg *.png *.jpeg *.JPG *.PNG *.JPEG")])
        if len(self.open_path) != 0 and self.open_path is not None:
            self.update_canvas(self.open_path)

    def process_img(self):
        if self.open_path is not None and len(self.open_path) != 0:
            self.temp_image, clips = self.ita.convert(self.open_path)
            self.update_canvas(self.temp_image)
            self.open_path = None
            self.clipboard_append(clips)
            self.update()

    def output_img(self):
        if self.temp_image is None:
            showerror(title="导出错误", message="图片导出出现问题, 请重试!")
            return

        save_path = asksaveasfilename(title="保存图片", filetypes=[("image", "*.png")])

        if len(os.path.splitext(save_path)[1]) == 0: return
        if os.path.splitext(save_path)[1] != ".png":
            showerror(title="后缀错误", message="文件后缀必须为<.png>")
            return

        if os.path.exists(self.temp_image):
            shutil.copy(self.temp_image, save_path)
            showinfo(title="复制完成", message="文件导出成功")
        else:
            showerror(title="复制错误", message="文件复制错误")
        
        self.image_canvas.delete(ctk.ALL)
        self.image_canvas = None
        self.temp_image = None
    
    def update_canvas(self, path: str):
        self.canvas_img = ImageTk.PhotoImage(self.suit_img(path))
        self.image_canvas.create_image(self.canvas_w/2, self.canvas_h/2, anchor=ctk.CENTER, image=self.canvas_img)
        self.image_canvas.update()

    def suit_img(self, path: str):
        img = Image.open(path)
        size1 = 1.0*self.canvas_w/img.size[0]
        size2 = 1.0*self.canvas_h/img.size[1]
        suitvar = min([size1, size2])
        w = int(img.size[0]*suitvar)
        h = int(img.size[1]*suitvar)
        return img.resize((w, h))

    def delete_temp_files(self):
        self.destroy()
        if not os.path.exists(self.ita.temp_save_path) or len(self.ita.temp_save_path) == 0:
            return
        
        for item in os.listdir(self.ita.temp_save_path):
            item_path = os.path.join(self.ita.temp_save_path, item)

            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
