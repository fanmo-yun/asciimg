from typing import LiteralString
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFile import ImageFile
import numpy as np
import datetime, os

class ImageToASCII:
    def __init__(self) -> None:
        self.ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`\'. "
        self.font_path = os.path.join("font", "JETBRAINSMONO-REGULAR.TTF")
        self.temp_save_path = "temp/"
        self.font_size = 16

    def resize_image(self, image: ImageFile, output_width=150) -> Image:
        width_ratio = output_width / image.width
        height = int(image.height * width_ratio * 0.5)
        return image.resize((output_width, height))
    
    def rgb_to_ansi(self, r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    def image_to_color_ascii(self, image: ImageFile):
        rgb_image = image.convert('RGB')
        image_array = np.array(rgb_image)
        grayscale_image = image.convert('L')
        grayscale_array = np.array(grayscale_image)

        normalized = (grayscale_array - grayscale_array.min()) / (grayscale_array.max() - grayscale_array.min())

        chars = []
        clip_chars = []
        for y, row in enumerate(normalized):
            ascii_row = []
            clip_row = []
            for x, _ in enumerate(row):
                r, g, b = image_array[y, x]

                pixel_gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
                pixel_normalized = pixel_gray / 255

                char_index = int(pixel_normalized * (len(self.ascii_chars) - 1))
                char = self.ascii_chars[char_index]

                ascii_row.append((char, (r, g, b)))
                clip_row.append(f"{self.rgb_to_ansi(r, g, b)}{char}\033[0m")
            
            chars.append(ascii_row)
            clip_chars.append(''.join(clip_row))
        
        return chars, '\n'.join(clip_chars)
    
    def save_img(self, ascii_art: list, save_path: str) -> str:
        font = ImageFont.truetype(self.font_path, self.font_size)

        char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]
        max_width = max(len(line) for line in ascii_art)

        image_width = max_width * char_width
        image_height = len(ascii_art) * char_height

        img = Image.new("RGB", (image_width, image_height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        for y, row in enumerate(ascii_art):
            for x, (char, color) in enumerate(row):
                draw.text(
                    (x * char_width, y * char_height),
                    char,
                    font=font,
                    fill=color
                )

        filename = str(int(datetime.datetime.now().timestamp())) + ".png"
        path = os.path.join(save_path, filename)
        img.save(path)
        return path
    
    def convert(self, image_path: str):
        if not os.path.exists(self.temp_save_path):
            os.mkdir(self.temp_save_path)

        with Image.open(image_path) as img:
            resize = self.resize_image(img)
            ascii_art, clip_ascii = self.image_to_color_ascii(resize)
            return self.save_img(ascii_art, self.temp_save_path), clip_ascii
