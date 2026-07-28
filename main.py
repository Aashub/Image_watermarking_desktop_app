"""Home Screen"""

# Single Image / Add Files: Upload a single image to watermark quickly.
# Batch Processing: Watermark many images at the same time.
# Templates / Presets: Load saved watermark styles and positions.
# cloud sync to upload the watermarked image and watermark style and position to the cloud storage


from tkinter import Tk, PhotoImage, Label


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 700

app_window = Tk()

# this will set the game window center to the screen.
screen_width = app_window.winfo_screenwidth()
screen_height = app_window.winfo_screenheight()
center_x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
center_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

app_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y }")
app_window.resizable(False, False)
app_window.title("Image Watermarking Desktop App")

img = PhotoImage(file = "img/watermark_app_home_menu_bg_img.png")
image_label = Label(app_window, image = img)
image_label.pack()
app_window.mainloop()

