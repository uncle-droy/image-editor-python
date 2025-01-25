import customtkinter as ctk
from customtkinter import filedialog
from CTkColorPicker import *
import os, shutil, PIL, pilgram2, pilgram

from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
from PIL import ImageDraw, Image, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageTk

# Initialize
os.system("cls||clear")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(os.path.join('assets', 'theme.json'))
root = ctk.CTk()
root.geometry("1200x600")
root.title("DRoy's Image Editor")

root.iconbitmap('assets/icon.ico')

# Create the path to store the undo images
def undo_path_create():
    # print(path)
    if not os.path.isdir(undo_path):
        os.makedirs(undo_path)
    else:
        shutil.rmtree(undo_path)
        os.makedirs(undo_path)


# global message
message: str = "Welcome, Open an image to start editing"

# Varibales
bright = 1
height: int = 550
width: int = 700

# angle: int = 90
undo_number: int = 0
file_extension: str = '.png'
save_quality = 100
# undo_number: int = 0
undo_path = os.path.join(os.getcwd(), 'undo')

filters = ['Sepia',
           '1977',
           'Aden',
           'Lofi',
           'Brannan',
           'Brooklyn',
           'Maven',
           'Earlybird',
           'Vignette',
           'Gingham',
           'Cartoon',
           'Grayscale',
           'Toaster',
           'Hefe',
           'Ludwig',
           'Perpetua',
           'Poprocket',
           'Valencia',
           'Kelvin',
           'Dogpatch',
           'Crema',
           'Clarendon',
           'Charmes',
           'Amaro',
           'Ashby']

#Widgets
editor_frame = ctk.CTkFrame(root, width=460, height=height - 80)
editor_frame.place(relx=0.8, rely=0.45, anchor=ctk.CENTER)
editor_frame.grid_propagate(0)
editor_frame.columnconfigure((0, 1, 2), weight=2)

img_info_frame = ctk.CTkFrame(root, width=460, height=170)
img_info_frame.place(relx=0.8, rely=0.7, anchor=ctk.CENTER)
img_info_frame.grid_propagate(0)
img_info_frame.columnconfigure(0, weight=1)
img_info_frame.rowconfigure(0, weight=1)


#Image properties

img_path_lbl = ctk.CTkLabel(img_info_frame, text='')
img_path_lbl.grid(row=0, column=0)

img_ht_lbl = ctk.CTkLabel(img_info_frame, text='')
img_ht_lbl.grid(row=1, column=0)

img_wd_lbl = ctk.CTkLabel(img_info_frame, text='')
img_wd_lbl.grid(row=2, column=0)

img_format_lbl = ctk.CTkLabel(img_info_frame, text='')
img_format_lbl.grid(row=3, column=0)

img_mode_lbl = ctk.CTkLabel(img_format_lbl, text='')
img_mode_lbl.grid(row=4, column=0)

img_size_lbl = ctk.CTkLabel(img_format_lbl, text='')
img_size_lbl.grid(row=5, column=0)

# Editor buttons
open_btn = ctk.CTkButton(editor_frame, text='Open', command=lambda: open_img())
open_btn.grid(row=0, column=0)

save_btn = ctk.CTkButton(editor_frame, text='Save', command=lambda: save_img(img))
save_btn.grid(row=0, column=1)

undo_btn = ctk.CTkButton(editor_frame, text='Undo', command=lambda: undo())
undo_btn.grid(row=0, column=2)

rotate_cbtn = ctk.CTkButton(editor_frame, text='Rotate Clockwise', command=lambda: rotate_clockwise())
rotate_cbtn.grid(row=2, column=1)

rotate_acbtn = ctk.CTkButton(editor_frame, text='Rotate Anti-Clockwise', command=lambda: rotate_anti_clockwise())
rotate_acbtn.grid(row=2, column=2)

blur_btn = ctk.CTkButton(editor_frame, text='Blur', width=80, command=lambda: blur())
blur_btn.grid(row=5, column=2, sticky='NW')

txt_blur = ctk.CTkEntry(editor_frame, placeholder_text="Value", width=60)
txt_blur.grid(row=5, column=2, sticky='NE')

contrast_btn = ctk.CTkLabel(editor_frame, text='Contrast:')
contrast_btn.grid(row=3, column=1)

contrast_up_btn = ctk.CTkButton(editor_frame, text='Increase', width=70, command=lambda: contrast_up())
contrast_up_btn.grid(row=3, column=2, sticky='NW')

contrast_down_btn = ctk.CTkButton(editor_frame, text='Decrease', width=70, command=lambda: contrast_down())
contrast_down_btn.grid(row=3, column=2, sticky='NE')

crop_btn = ctk.CTkButton(editor_frame, text="Crop", command=lambda: modern_crop())
crop_btn.grid(row=1, column=2)

annotate_btn = ctk.CTkButton(editor_frame, text="Annotate", command=lambda: draw())
annotate_btn.grid(row=2, column=0)

brighten_btn = ctk.CTkLabel(editor_frame, text="Brightness:")
brighten_btn.grid(row=1, column=0)

brighten_up = ctk.CTkButton(editor_frame, width=70, text="Increase", command=lambda: bright_up())
brighten_up.grid(row=1, column=1, sticky="W")

brighten_down = ctk.CTkButton(editor_frame, width=70, text="Decrease", command=lambda: bright_down())
brighten_down.grid(row=1, column=1, sticky="E")

# grayscale_to_rgb = ctk.CTkButton(editor_frame, text="Grayscale", command=lambda: grayscale())
# grayscale_to_rgb.grid(row=3, column=0)

background_remove = ctk.CTkButton(editor_frame, text="Remove bg", command=lambda: remove_background())
background_remove.grid(row=5, column=1)

# cartoonize_btn = ctk.CTkButton(editor_frame, text="Cartoonize", command=lambda: cartoon())
# cartoonize_btn.grid(row=4, column=0)

text_btn = ctk.CTkButton(editor_frame, text="Add Text", command=lambda: add_text_fn())
text_btn.grid(row=4, column=1)

sharpen_btn = ctk.CTkButton(editor_frame, text="Sharpen", command=lambda: sharp())
sharpen_btn.grid(row=4, column=2)

detail_btn = ctk.CTkButton(editor_frame, text="Detail", command=lambda: detail())
detail_btn.grid(row=5, column=0)

border_btn = ctk.CTkButton(editor_frame, text="Add Borders", command = lambda:borders())
border_btn.grid(row=4, column=0)

blend_btn = ctk.CTkButton(editor_frame, text='Blend', command = lambda:blend())
blend_btn.grid(row=11, column=2)

colorize_btn = ctk.CTkButton(editor_frame, text='Colorize', command = lambda:colorize_rgb())
colorize_btn.grid(row=12, column=0)

rev_colorize_btn = ctk.CTkButton(editor_frame, text='Reverse Colorize', command = lambda:rev_colorize_rgb())
rev_colorize_btn.grid(row=12, column=1)

# #Filters

filters_label = ctk.CTkLabel(editor_frame, text="Filters:")
filters_label.grid(row=6, column=0)

filters_list = ctk.CTkOptionMenu(editor_frame, values=filters)
filters_list.grid(row=6, column=1)

apply_filter_btn = ctk.CTkButton(editor_frame, text='Apply', command=lambda: apply_filter())
apply_filter_btn.grid(row=6, column=2)

hue_rotate_btn = ctk.CTkButton(editor_frame, text="Rotate Hue", width=75, command=lambda: hue_rotate())
hue_rotate_btn.grid(row=3, column=0, sticky="NW")

hue_rotate_value = ctk.CTkEntry(editor_frame, placeholder_text="Degrees", width=65)
hue_rotate_value.grid(row=3, column=0, sticky="NE")

magic_resize_button = ctk.CTkButton(editor_frame, text='Magic Resize', command=lambda: magic_rescale())
magic_resize_button.grid(row=11, column=0)

resize_btn = ctk.CTkButton(editor_frame, text='Resize',command=lambda:rescale_image())
resize_btn.grid(row=11, column=1)

message_lbl = ctk.CTkLabel(root, text=message)
message_lbl.place(relx=0.8, rely=0.92, anchor=ctk.CENTER)


# Draw the image canvas
def draw_canvas():
    global view_frame
    view_frame = ctk.CTkFrame(root, width=width, height=height)
    view_frame.place(relx=0.32, rely=0.5, anchor=ctk.CENTER)
    return view_frame


# Save the image
def save_img(image):
    global img
    pdf_author = "Daiwik Roy"
    save_quality=ctk.CTkInputDialog(text="Enter a save quality (0-100)%", title='Save quality')
    if save_quality>=0 and save_quality<=100:
        filepath = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                filetypes=[("JPG files", "*.jpg"), ("PNG files", "*.png"),
                                                        ("BITMAP files", "*.bmp"), ("TIFF files", "*.tiff"),
                                                        ("GIF files", "*.gif"), ("PDF files", "*.pdf")])
        if filepath:
            if str(image.format) == "JPEG" or img.format == "JPG":
                image = image.convert('RGB')
            image.save(filepath, quality=save_quality, creator="Baan Editor", author=pdf_author, producer="PIL")
            message = "Image saved successfully"
            update_message_label(message)


# Save the undo image
def save_undo_image():
    global undo_number, img
    undo_number += 1
    save_path = os.path.join(undo_path, "undo" + str(undo_number) + "." + str(file_extension).lower())
    print(undo_number, str(file_extension.lower()) + "." + str(save_path))
    # if str(img.format) == "JPEG" or img.format == "JPG":
    #         img = img.convert('RGB')
    if img.mode in ('RGBA', 'LA'):
        save_path = os.path.join(undo_path, "undo" + str(undo_number) + ".png")
    img.save(save_path, quality=100, lossless=True)
    print(undo_number)


# File dialog box open
def open_img():
    # import matplotlib.pyplot as plt

    filepath = filedialog.askopenfilename(title='Open Image')
    # Load canvas and image
    view_frame = draw_canvas()

    if filepath:
        global img
        img = Image.open(filepath)
        global file_extension
        file_extension = img.format
        img_format = file_extension
        # img_size = img.size()
        
        img_path_lbl.configure(text = 'Filename of file being edited: ' + os.path.basename(filepath) + '\nParent Folder: ' +  os.path.basename(os.path.dirname(filepath)))
        img_ht_lbl.configure(text = 'Height (px): ' + str(img.height))
        img_wd_lbl.configure(text = 'Width (px): ' + str(img.width))
        if os.path.getsize(filepath)/1024 > 10:
            img_size_lbl.configure(text = 'Size (MB): ' + str(round(os.path.getsize(filepath)/(1024*1024), 3)))
        else:
            img_size_lbl.configure(text = 'Size (KB): ' + str(round(os.path.getsize(filepath)/1024, 3)))
        img_format_lbl.configure(text= 'Format: ' + file_extension)
        img_mode_lbl.configure(text='Mode: ' + img.mode)

        # Display
        # img = img.resize((r_x, r_y))
        # my_image = ctk.CTkImage(light_image=img, dark_image=img, size=(r_x, r_y))
        r_x, r_y = resize(img)
        global image_label, message
        image_label = ctk.CTkLabel(view_frame, text="")
        image_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        message = "Image opened successfully"
        save_changes(img, message)


def display_image(image, x, y):
    disp_img = ctk.CTkImage(light_image=image, dark_image=image, size=(x, y))
    global image_label
    image_label.configure(image=disp_img)
    image_label.image = disp_img


def undo():
    global undo_number, message
    global img
    if undo_number > 1:
        undo_number -= 1
        undo_image_path = os.path.join(undo_path, "undo" + str(undo_number) + "." + str(file_extension).lower())
        img = Image.open(undo_image_path)
        x_r, y_r = img.size
        factor = min(width / x_r, height / y_r)
        if x_r >= width and x_r >= height:
            r_x = int(x_r * factor)
            r_y = int(y_r * factor)
        else:
            r_x, r_y = img.size

        display_image(img, r_x, r_y)
        undo_file_path_cur = os.path.join(undo_path, "undo" + str(undo_number) + "." + str(file_extension).lower())
        if os.path.getsize(undo_file_path_cur)/1024 > 10:
            img_size_lbl.configure(text = 'Previous Size (MB): ' + str(round(os.path.getsize(undo_file_path_cur)/(1024*1024), 3)))
        else:
            img_size_lbl.configure(text = 'Previou Size (KB): ' + str(round(os.path.getsize(undo_file_path_cur)/1024, 3)))

        message = "Undo done!"


    elif undo_number == 1:
        message = "Last undo done.\nNothing more to undo!"

    update_message_label(message)


#Update the message label
def update_message_label(message):
    message_lbl.configure(text=message)
    message_lbl.text = message


# Scale image
def resize(img):
    x, y = img.size
    factor = min(width / x, height / y)
    if x >= width and x >= height:
        new_x = int(x * factor)
        new_y = int(y * factor)
    else:
        new_x, new_y = img.size
    
    return new_x, new_y



def save_changes(image, message):
    x, y = resize(image)
    display_image(image, x, y)
    save_undo_image()
    update_message_label(message)


# Image operations

#Brightness
def bright_up():
    global img, bright, undo_number
    filt = ImageEnhance.Brightness(img)

    img = filt.enhance(1.1)

    x, y = resize(img)
    display_image(img, x, y)
    save_undo_image()


def bright_down():
    global img, bright, undo_number
    bright = 1
    filt = ImageEnhance.Brightness(img)

    img = filt.enhance(0.9)

    x, y = resize(img)
    display_image(img, x, y)
    save_undo_image()


#Crop the image
def modern_crop():
    import scripts.crop as crop
    global img, undo_number
    image_path = os.path.join(undo_path,"undo" + str(undo_number) + "." + str(file_extension).lower())
    undo_number += 1
    save_path = os.path.join(undo_path, "undo" + str(undo_number) + "." + str(file_extension).lower())
    crop.crop_image(image_path, undo_number, save_path)

    img = Image.open(save_path)
    x, y = resize(img)
    display_image(img, x, y)
    message = "Image has been cropped"
    update_message_label(message)


#Blur the image
def blur():
    global img

    if txt_blur.get() == "":
        r = 5
    else:
        r = int(txt_blur.get())
    img = img.filter(ImageFilter.GaussianBlur(radius=r))
    x_r, y_r = img.size
    x_r, y_r = img.size
    factor = min(width / x_r, height / y_r)
    if x_r >= width and x_r >= height:
        r_x = int(x_r * factor)
        r_y = int(y_r * factor)
    else:
        r_x, r_y = img.size

    display_image(img, r_x, r_y)
    #Undo save
    save_undo_image()
    message = f"Blur applied with intensity: {r}"
    update_message_label(message)


#Vignette
def vignette():
    global img
    width, height = img.size
    vignette_effect = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(vignette_effect)

    center_x, center_y = width // 2, height // 2
    max_radius = int(max(center_x, center_y) * 0.9)

    for i in range(max_radius):
        alpha = int(255 * (i / max_radius) ** 2)
        draw.ellipse([(center_x - i, center_y - i), (center_x + i, center_y + i)], fill=alpha)

    vignette_effect = vignette_effect.filter(ImageFilter.GaussianBlur(60))
    vignette_effect = vignette_effect.resize(img.size)

    img = Image.composite(img, Image.new('RGB', img.size, (0, 0, 0)), vignette_effect)

    x, y = resize(img)
    display_image(img, x, y)
    save_undo_image()
    message = "Vignette applied!"
    update_message_label(message)


#Sharpen
def sharp():
    global img
    img = img.filter(SHARPEN)
    x, y = resize(img)
    display_image(img, x, y)
    save_undo_image()
    message = "Image sharpened!"
    update_message_label(message)


#Detail
def detail():
    global img
    if img.format == "JPEG" or img.format == "JPG":
        img = img.convert('RGB')
    img = img.filter(DETAIL)

    message = "Details enhanced!"
    save_changes(img, message)


#Grayscale
def grayscale():
    global img
    if img.format == "JPEG" or img.format == "JPG":
        img = img.convert('RGB')
    img = ImageOps.grayscale(img)

    message = "Grayscale applied!"
    save_changes(img, message)


# Rotate the image
def rotate_clockwise():
    global img
    img = img.rotate(-90, expand=True)

    message = "Rotated Clockwise"
    save_changes(img, message)


def rotate_anti_clockwise():
    global img
    img = img.rotate(90, expand=True)
    message = "Rotated Anti-Clockwise"
    save_changes(img, message)


#Remove background
def remove_background():
    from rembg import remove
    global img

    img = remove(img)
    message = "Background removed successfully"
    save_changes(img, message)


#Annotate:
def draw():
    import scripts.draw as an
    global img, undo_number
    image_path = os.path.join(undo_path, "undo" + str(undo_number) + "." + str(file_extension).lower())
    undo_number += 1
    save_path = os.path.join(undo_path,"undo" + str(undo_number) + "." + str(file_extension).lower())
    an.draw(image_path, undo_number, save_path)

    img = Image.open(save_path)
    message = "Annotations applied"
    save_changes(img, message)


#Cartoonize the image
def cartoon():
    import scripts.cartoon as cn
    global img, undo_number

    image_path = os.path.join(undo_path,"undo" + str(undo_number) + "." + str(file_extension).lower())
    save_path = os.path.join(undo_path,"undo" + str(undo_number + 1) + "." + str(file_extension).lower())

    message = "Please wait!\nProgram will freeze for some time..."
    update_message_label(message)

    cn.cartoonify_image(image_path, undo_number, save_path)
    undo_number += 1
    img = Image.open(save_path)
    message = "Cartoonized successfully"
    save_changes(img, message)


def add_text_fn():
    import scripts.add_text as at
    global img, undo_number
    print(undo_number)

    image_path = os.path.join(undo_path,"undo" + str(undo_number) + "." + str(file_extension).lower())
    print(image_path)
    save_path = os.path.join(undo_path,"undo" + str(undo_number + 1) + "." + str(file_extension).lower())

    new_undo_number = at.text_add(image_path, undo_number, save_path)
    if new_undo_number != undo_number:
        img = Image.open(save_path)
        x, y = resize(img)

        display_image(img, x, y)
        undo_number = new_undo_number
        message = "Text added successfully"
        update_message_label(message)
    else:
        message = "Text not added"
        update_message_label(message)


# 1977
def _1977():
    global img, undo_number
    img = pilgram2._1977(img)
    message = "Applied old 1977 tone"
    save_changes(img, message)

# Set contrast
def contrast_up():
    global img, undo_number
    img = pilgram2.css.contrast(img, 1.1)
    message = "Contrast increased"
    save_changes(img, message)


def contrast_down():
    global img, undo_number
    img = pilgram2.css.contrast(img, 0.9)
    message = "Contrast decreased"
    save_changes(img, message)

# Rotate hue
def hue_rotate():
    global img, undo_number
    if hue_rotate_value.get() == '':
        degrees = 90
    else:
        degrees = int(hue_rotate_value.get())
    img = pilgram2.css.hue_rotate(img, degrees)
    message = f"Hue rotated {degrees}"
    save_changes(img, message)


# Apply the selected filter
def apply_filter():
    import pilgram2.css
    import pilgram2.css.blending
    import pilgram
    global img, undo_number
    filter_selected = filters_list.get().lower()
    if filter_selected == "1977":
        _1977()
    elif filter_selected == "vignette":
        vignette()
    elif filter_selected == "cartoon":
        cartoon()
    else:

        try:
            func = 'pilgram2.' + filter_selected + '(img)'
            img = eval(func)
        except:
            func = 'pilgram2.css.' + filter_selected + '(img)'
            img = eval(func)
        message = f"{filters_list.get()} applied"
        save_changes(img, message)
    print(filter_selected)


# Resize
def magic_rescale():
    global img, undo_number
    from wand.image import Image as wImage
    import numpy as np
    import io
    with wImage.from_array(np.array(img)) as ximg:
        wand_img = ximg.clone()

    h_dialog = ctk.CTkInputDialog(text="Height:", title="Resize")
    resize_height = int(h_dialog.get_input())
    w_dialog = ctk.CTkInputDialog(text="Width:", title="Resize")
    resize_width = int(w_dialog.get_input())
    wand_img.liquid_rescale(resize_width, resize_height)
    img = PIL.Image.open(io.BytesIO(wand_img.make_blob("png")))
    message = f"Image resized to {width}x{height}"
    save_changes(img, message)

def rescale_image():
    global img, undo_number
    h_dialog = ctk.CTkInputDialog(text="Height:", title="Resize")
    resize_height = int(h_dialog.get_input())
    w_dialog = ctk.CTkInputDialog(text="Width:", title="Resize")
    resize_width = int(w_dialog.get_input())
    img = img.resize((resize_width, resize_height), resample=Image.LANCZOS)
    message = f"Image resized to {resize_width}x{resize_height}"
    img_ht_lbl.configure(text='Updated image height: ' + str(resize_height) + 'px')
    img_wd_lbl.configure(text='Updated image width: ' + str(resize_width) + 'px')
    undo_file_path_cur = os.path.join(undo_path, "undo" + str(undo_number) + "." + str(file_extension).lower())
    if os.path.getsize(undo_file_path_cur)/1024 > 10:
        img_size_lbl.configure(text = 'Size (MB): ' + str(round(os.path.getsize(undo_file_path_cur)/(1024*1024), 3)))
    else:
        img_size_lbl.configure(text = 'Size (KB): ' + str(round(os.path.getsize(undo_file_path_cur)/1024, 3)))
    save_changes(img, message)

# Add borders
def borders():
    global img, undo_number
    size_dialog = ctk.CTkInputDialog(text='Enter border width between 1-100', title = 'Apply borders')
    border_size = int(size_dialog.get_input())
    color = ask_color()

    img = ImageOps.expand(img, border=border_size, fill=color)
    message = f"Border added with size {border_size}"
    save_changes(img, message)

def blend():
    global img, undo_number
    import cv2, numpy
    filepath = filedialog.askopenfilename(title='Open Image')
    img2 = cv2.imread(filepath)
    img1 = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    img2 = cv2.resize(img2, img.size)
    weights_input = ctk.CTkInputDialog(text='Enter weights for first, second images, and the scalar constant', title = 'Weights')
    weights = [float(i) for i in weights_input.get_input().split(',')]
    alpha, beta, gamma = weights[0], weights[1], weights[2]
    dst = cv2.addWeighted(img1, alpha, img2, beta, gamma)
    img = Image.fromarray(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
    message = "Blending applied"
    save_changes(img, message)


# Choose color
def ask_color():

    pick_color = AskColor()  # open the color picker
    color = pick_color.get()  # get the color string
    return color

def colorize_rgb():
    global img, undo_number
    color = ask_color()
    img = img.convert('L')
    img = ImageOps.colorize(img, black='#000000', white=color)
    message = "Image colorized"
    save_changes(img, message)

def rev_colorize_rgb():
    global img, undo_number
    color = ask_color()
    img = img.convert('L')
    img = ImageOps.colorize(img, black=color, white='#000000')
    message = "Image colorized"
    save_changes(img, message)
    
    


# Main Run
if __name__ == "__main__":
    undo_path_create()
    root.mainloop()
