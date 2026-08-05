"""Home Screen"""

# Single Image / Add Files: Upload a single image to watermark quickly.
# Batch Processing: Watermark many images at the same time.
# Templates / Presets: Load saved watermark styles and positions.
# cloud sync to upload the watermarked image and watermark style and position to the cloud storage


from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox, Style

from PIL import Image, ImageTk

HEADING_TEXT_COLOR = "black"
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 700
FILE_TYPES = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
              ("All files", "*.*")]  # Define allowed image file types

text_align_options = ['Align-Center', 'Bottom-Right-Corner', 'Bottom-Left-Corner',
                         'Bottom-Center Edge', 'Top-Right-Corner', 'Top-Left-Corner',
                         'Top-Center Edge', 'Left-Center Edge', 'Right-Center Edge']


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

        self.watermark_mode = "alignment"
        self.current_alignment = "Align-Center"  # default alignment

        self.watermark_rel_x = 0.5  # used only in "free" mode
        self.watermark_rel_y = 0.5

        self.zoom_scale = 1.0

        self.add_home_screen_image()

    # ************************************************ HOME SCREEN *****************************************************

    def add_home_screen_image(self):
        """this method add background image in home screen"""

        # add home screen image
        img = PhotoImage(file="img/watermark_app_home_menu_bg_img.png")
        image_label = Label(self, image=img)
        image_label.pack()

        self.home_screen_heading_text()
        self.mainloop()

    def home_screen_heading_text(self):
        """this method add heading text in home screen"""

        # home screen text canvas
        text_canvas = Canvas(width=490, height=80, bg="#0D9BC7", highlightthickness=0)
        text_canvas.place(x=300, y=200)

        # heading text
        heading_text = text_canvas.create_text(250, 25, text=f"Make watermark quickly", font=("Arial", 30, "bold"),
                                               anchor="center", fill="white")

        # subheading text
        sub_heading_text = text_canvas.create_text(250, 63,
                                                   text=f"add watermark to single & several images in a breeze.",
                                                   font=("Arial", 13, "bold"), fill="white")
        self.home_screen_button()

    def home_screen_button(self):
        """this method add button in home screen"""

        # single image button
        single_image_button = Button(self, text="Start Make Watermark", font=("Arial", 12, "bold"), fg="white",
                                     command=self.display_watermarking_screen, bd=0, bg="#F05A5A", height=2)
        single_image_button.place(x=355, y=300)

        # batch image button
        batch_image_button = Button(self, text="Start Batch Watermark", font=("Arial", 12, "bold"), fg="white",
                                    command=lambda: print("Clicked!"), bd=0, bg="#F05A5A", height=2)
        batch_image_button.place(x=560, y=300)

    # ************************************************ HOME SCREEN *****************************************************

    # ****************************************** DISPLAY WATERMARK SCREEN **********************************************

    def display_watermarking_screen(self):
        """this method will load the screen where image is being watermarked."""

        [widget.destroy() for widget in self.winfo_children()]  # this for loop destroy the previous screen all widget

        # create canvas for image area
        self.image_canvas = Canvas(width=800, height=700, bg="#313131", highlightthickness=0)
        self.image_canvas.place(x=0, y=0)

        # create canvas for editing widget buttons
        self.image_edit_widget_canvas = Canvas(width=280, height=700, bg="#494949", highlightthickness=0)
        self.image_edit_widget_canvas.place(x=800, y=0)

        self.all_edit_button()

    # ****************************************** DISPLAY WATERMARK SCREEN **********************************************

    # ********************************************** ALL EDIT  BUTTON **************************************************

    def all_edit_button(self):
        """this method contains all the edit button to edit the watermark text"""

        def capture_text():
            """this function capture the entered text in entry field and pass that text to display_watermark_text method."""

            received_text = self.entry_field.get()
            self.display_watermark_text(received_text)

        # watermark text
        self.image_edit_widget_canvas.create_text(72, 30, text=f"Water Mark text",
                                                  font=("Arial", 10, "bold"), fill="white")

        entry_field_frame = Frame(self, width=235, height=30, bg="white")
        entry_field_frame.place(x=822, y=43)

        # entry field
        self.entry_field = Entry(entry_field_frame, font=("Arial", 11), width=30, relief="flat")
        self.entry_field.place(x=0, y=5)

        combobox_style = Style()
        combobox_style.configure("Padded.TCombobox", padding=(3, 4))  # (horizontal, vertical)

        # creating combobox button
        self.alignment_options = Combobox(self.image_edit_widget_canvas, values=text_align_options,
                                     font=("Arial", 8, "bold"),
                                     state="readonly", width=16, style="Padded.TCombobox")
        self.alignment_options.set('Select Alignment')
        self.alignment_options.place(x=22, y=80)

        self.alignment_options.bind("<<ComboboxSelected>>", self.on_alignment_selected)

        # watermark text submit btn
        submit_btn = Button(self.image_edit_widget_canvas, text="Submit", command=capture_text, width=14,
                            bg="gray")
        submit_btn.place(x=150, y=80)


        # creating add image button
        add_image_button = Button(self.image_edit_widget_canvas, text="Select Image", font=("Arial", 12, "bold"),
                                  fg="white",
                                  command=self.open_file_explorer, bd=0, bg="#007aff", width=18, height=2)
        add_image_button.place(x=48, y=600)

    # ********************************************** ALL EDIT  BUTTON **************************************************

    # ********************************** Display watermark & Align Watermark Position **********************************

    def display_watermark_text(self, received_text):
        """this method will display the watermark text on the canvas image area on the screen"""

        image_coord = self.image_canvas.bbox(self.image_on_canvas)
        image_left_side_coord, image_top_side_coord, image_right_side_coord, image_bottom_side_coord = image_coord

        image_width = image_right_side_coord - image_left_side_coord  # image width
        image_height = image_bottom_side_coord - image_top_side_coord  # image height

        text_x_cord = image_left_side_coord + (image_width // 2)
        text_y_cord = image_top_side_coord + (image_height // 2)

        # watermark text
        self.watermark_text = self.image_canvas.create_text(text_x_cord, text_y_cord, text=received_text,
                                                            font=("Arial", 14, "bold"),
                                                            anchor="center", fill="black")

        def move_text_on_drag(event):
            "this function will move text on the image anywhere the user wants."

            self.image_canvas.coords(self.watermark_text, event.x, event.y)


            image_coord = self.image_canvas.bbox(self.image_on_canvas)
            image_x1, image_y1, image_x2, image_y2 = image_coord

            image_width = image_x2 - image_x1
            image_height = image_y2 - image_y1

            # storing watermark relative position so i can be used in free mode.
            self.watermark_rel_x = (event.x - image_x1) / image_width
            self.watermark_rel_y = (event.y - image_y1) / image_height

            self.watermark_mode = "free"  # dragging overrides alignment

        self.image_canvas.tag_bind(self.watermark_text, "<B1-Motion>", move_text_on_drag)

    def reposition_watermark_after_resize(self):
        """this method will align the watermark after resize as per the user used mode between alignment and or free(drag mode) it has used."""

        if self.watermark_mode == "alignment":
            self.on_alignment_selected()  # recompute from stored alignment

        else:  # here when user used drag mode to position the text as per his desire will align the text according to the image size
            image_x1, image_y1, image_x2, image_y2 = self.image_canvas.bbox(self.image_on_canvas)
            image_width = image_x2 - image_x1
            image_height = image_y2 - image_y1

            new_x = image_x1 + (self.watermark_rel_x * image_width)
            new_y = image_y1 + (self.watermark_rel_y * image_height)
            self.image_canvas.coords(self.watermark_text, new_x, new_y)


    def on_alignment_selected(self, event = None):

        if event is not None:
            self.current_alignment = event.widget.get()

        self.watermark_mode = "alignment"    # selecting an option overrides free drag
        triggered_option = self.current_alignment

        # will get image all four side coordinates
        image_coord = self.image_canvas.bbox(self.image_on_canvas)
        image_left_side_coord, image_top_side_coord, image_right_side_coord, image_bottom_side_coord = image_coord

        image_width = image_right_side_coord - image_left_side_coord  # image width
        image_height = image_bottom_side_coord - image_top_side_coord  # image height

        # will get text all four side coordinates
        text_coord = self.image_canvas.bbox(self.watermark_text)
        text_x1, text_y1, text_x2, text_y2 = text_coord

        text_width = text_x2 - text_x1  # text width
        text_height = text_y2 - text_y1  # text height

        if "Align-Center" == triggered_option:

            text_x_cord = image_left_side_coord + (image_width // 2)
            text_y_cord = image_top_side_coord + (image_height // 2)
            self.image_canvas.coords(self.watermark_text, text_x_cord, text_y_cord)

        elif triggered_option == "Top-Left-Corner":

            text_x_cord = image_left_side_coord + (text_width / 2) + 5
            text_y_cord = image_top_side_coord + (text_height / 2) + 5
            self.image_canvas.coords(self.watermark_text, text_x_cord, text_y_cord)

        elif triggered_option == "Bottom-Left-Corner":

            text_x_cord = image_left_side_coord + (text_width / 2) + 5
            text_y_cord = image_bottom_side_coord - (text_height / 2) - 5
            self.image_canvas.coords(self.watermark_text, text_x_cord, text_y_cord)

        elif triggered_option == "Left-Center Edge":

            text_x_cord = image_left_side_coord + (text_width / 2) + 5
            text_y_cord = image_top_side_coord + (image_height // 2)
            self.image_canvas.coords(self.watermark_text, text_x_cord, text_y_cord)

        elif triggered_option == "Top-Right-Corner":

            text_x_cord = image_right_side_coord - (text_width / 2) - 5
            text_y_cord = image_top_side_coord + (text_height / 2) + 5
            self.image_canvas.coords(self.watermark_text, text_x_cord, text_y_cord)


        elif triggered_option == "Bottom-Right-Corner":

            text_x_cord = image_right_side_coord - (text_width / 2) - 5
            text_y_cord = image_bottom_side_coord - (text_height / 2) - 5
            self.image_canvas.coords(self.watermark_text, text_x_cord, text_y_cord)

        elif triggered_option == "Right-Center Edge":

            text_x_cord = image_right_side_coord - (text_width / 2) - 5
            text_y_cord = image_top_side_coord + (image_height // 2)
            self.image_canvas.coords(self.watermark_text, text_x_cord,
                                     text_y_cord)

        elif triggered_option == "Top-Center Edge":

            text_x_cord = image_left_side_coord  + (image_width // 2)
            text_y_cord = image_top_side_coord + (text_height / 2) + 5
            self.image_canvas.coords(self.watermark_text, text_x_cord,
                                     text_y_cord)

        elif triggered_option == "Bottom-Center Edge":

            text_x_cord = image_left_side_coord + (image_width // 2)
            text_y_cord = image_bottom_side_coord - (text_height / 2) - 5
            self.image_canvas.coords(self.watermark_text, text_x_cord,
                                     text_y_cord)  # getting watermark text coordinates

    # ********************************** Display watermark & Align Watermark Position **********************************


    # ******************************************* DISPLAY WATERMARK IMAGE **********************************************

    def open_file_explorer(self):
        """this method will open the file explorer to select the image on which user wants to add watermark."""

        # Open the file dialog and get the selected file path
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(FILE_TYPES))

        if file_path:
            self.display_image(file_path)

    def display_image(self, image_file):
        """this method will display image on the screen"""

        self.original_image = Image.open(image_file)
        self.original_width = self.original_image.width
        self.original_height = self.original_image.height

        # it will show image which needs to be watermarked screen image
        self.watermarking_image = ImageTk.PhotoImage(self.original_image)
        self.image_on_canvas = self.image_canvas.create_image(400, 350, image=self.watermarking_image, anchor='center')

        self.image_canvas.bind("<MouseWheel>", self.resize_image)

    def resize_image(self, event):
        """this method will zoom in or zoom out the image"""

        if event.num == 4 or event.delta > 0:
            self.zoom_scale *= 1.1

        elif event.num == 5 or event.delta < 0:
            self.zoom_scale /= 1.1

        # 1. Cap the maximum zoom at 5.0 (500%)
        if self.zoom_scale > 5.0:
            self.zoom_scale = 5.0

        # 2. Cap the minimum zoom at 0.1 (10%)
        if self.zoom_scale < 0.1:
            self.zoom_scale = 0.1

        new_size = (int(self.original_width * self.zoom_scale), int(self.original_height * self.zoom_scale))
        self.resized_image = self.original_image.resize(new_size, Image.Resampling.BILINEAR)

        self.watermarking_image = ImageTk.PhotoImage(self.resized_image)
        self.image_canvas.itemconfig(self.image_on_canvas, image=self.watermarking_image)

        self.reposition_watermark_after_resize()



    # ******************************************* DISPLAY WATERMARK IMAGE **********************************************


app_window = UserInterface()
