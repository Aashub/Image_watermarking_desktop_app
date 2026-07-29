"""Home Screen"""

# Single Image / Add Files: Upload a single image to watermark quickly.
# Batch Processing: Watermark many images at the same time.
# Templates / Presets: Load saved watermark styles and positions.
# cloud sync to upload the watermarked image and watermark style and position to the cloud storage


from tkinter import Tk, PhotoImage, Label, Canvas, Button

HEADING_TEXT_COLOR = "black"
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 700

class UserInterface(Tk):

    def __init__(self):
        super().__init__()



        # this will set the game window center to the screen.
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        center_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")
        self.resizable(False, False)
        self.title("Image Watermarking Desktop App")

        self.add_home_screen_image()


    def add_home_screen_image(self):

        # add home screen image
        img = PhotoImage(file="img/watermark_app_home_menu_bg_img.png")
        image_label = Label(self, image=img)
        image_label.pack()

        self.home_screen_heading_text()
        self.mainloop()


    def home_screen_heading_text(self):

        # home screen text canvas
        text_canvas = Canvas(width=490, height=80, bg = "#0D9BC7", highlightthickness = 0)
        text_canvas.place(x=300, y=200)

        # heading text
        heading_text = text_canvas.create_text(250, 25, text=f"Make watermark quickly", font=("Arial", 30, "bold"),
                                               anchor="center", fill= "white")

        # subheading text
        sub_heading_text = text_canvas.create_text(250, 63, text=f"add watermark to single & several images in a breeze.",
                                                   font=("Arial", 13, "bold"), fill= "white" )

        self.home_screen_button()

    def home_screen_button(self):

        # single image button
        single_image_button = Button(self, text="Start Make Watermark", font=("Arial", 12, "bold"), fg="white",
                                     command=lambda: print("Clicked!"), bd=0, bg="#F05A5A", height= 2)
        single_image_button.place(x=355, y=300)

        # batch image button
        batch_image_button = Button(self, text="Start Batch Watermark", font=("Arial", 12, "bold"), fg="white",
                                    command=lambda: print("Clicked!"), bd=0, bg="#F05A5A", height= 2)
        batch_image_button.place(x=560, y=300)

app_window = UserInterface()

