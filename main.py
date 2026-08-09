
from tkinter import *
from tkinter import filedialog, font
from tkinter.ttk import Combobox, Style
from PIL import Image, ImageTk
from data import text_align_options, watermark_colors

HEADING_TEXT_COLOR = "black"
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 700
FILE_TYPES = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
              ("All files", "*.*")]  # Define allowed image file types


class UserInterface(Tk):

    def __init__(self):
        super().__init__()

        # this will set the game window center to the screen.

        self.font_style = "normal"
        self.received_text = None
        self.scaled_font_size = 8
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        center_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")
        self.resizable(False, False)
        self.title("Image Watermarking Desktop App")

        self.current_font_family = "Arial"
        self.current_font_size = 14

        self.watermark_mode = "alignment"
        self.current_alignment = "Align-Center"  # default alignment

        self.watermark_rel_x = 0.5  # used only in "free" mode
        self.watermark_rel_y = 0.5

        self.zoom_scale = 1.0

        self.font_designs = list(font.families())
        self.watermark_colors = watermark_colors

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

    # ********************************************** ALL EDIT  BUTTON **************************************************

    def all_edit_button(self):
        """this method contains all the edit button to edit the watermark text"""

        def capture_text():
            """this function capture the entered text in entry field and pass that text to display_watermark_text method."""

            self.received_text = self.entry_field.get()
            self.display_watermark_text(self.received_text)

            # watermark text
        self.image_edit_widget_canvas.create_text(72, 30, text=f"Water Mark text",
                                                  font=("Arial", 10, "bold"), fill="white")

        entry_field_frame = Frame(self, width=235, height=30, bg="white")
        entry_field_frame.place(x=822, y=43)

        # entry field
        self.entry_field = Entry(entry_field_frame, font=("Arial", 11), width=30, relief="flat")
        self.entry_field.place(x=0, y=5)

        # custom text alignment combobox padding
        combobox_style = Style()
        combobox_style.configure("Text_Alignment.TCombobox", padding=(3, 4))  # (horizontal, vertical)

        # creating combobox for alignment
        self.alignment_options = Combobox(self.image_edit_widget_canvas, values=text_align_options,
                                          font=("Arial", 8, "bold"),
                                          state="readonly", width=16, style="Text_Alignment.TCombobox")
        self.alignment_options.set('Select Alignment')
        self.alignment_options.place(x=22, y=80)

        self.alignment_options.bind("<<ComboboxSelected>>", self.on_alignment_selected)

        # watermark text submit btn
        submit_btn = Button(self.image_edit_widget_canvas, text="Submit", command=capture_text, width=14,
                            bg="gray")
        submit_btn.place(x=150, y=80)

        # 1. Create a shared Tkinter variable
        selected_option = StringVar(self.image_edit_widget_canvas, value="Option 1")

        # 2. Create the Radiobutton widgets
        radio1 = Radiobutton(self.image_edit_widget_canvas, text="Bold", variable=selected_option, value="Option 1",
                             bg="#494949", fg="white", font=("Arial", self.scaled_font_size), activebackground="#494949",
                             activeforeground="white", selectcolor="#494949",
                             command=lambda: self.update_font_style("bold"))

        radio2 = Radiobutton(self.image_edit_widget_canvas, text="Itallic", variable=selected_option, value="Option 2",
                             bg="#494949", fg="white", font=("Arial", self.scaled_font_size), activebackground="#494949",
                             activeforeground="white", selectcolor="#494949",
                             command=lambda: self.update_font_style("italic"))

        radio3 = Radiobutton(self.image_edit_widget_canvas, text="Underline", variable=selected_option,
                             value="Option 3",
                             bg="#494949", fg="white", font=("Arial", self.scaled_font_size), activebackground="#494949",
                             activeforeground="white", selectcolor="#494949",
                             command=lambda: self.update_font_style("underline"))

        radio4 = Radiobutton(self.image_edit_widget_canvas, text="reset", variable=selected_option, value="Option 4",
                             bg="#494949", fg="white", font=("Arial", self.scaled_font_size), activebackground="#494949",
                             activeforeground="white", selectcolor="#494949",
                             command=lambda: self.update_font_style("reset"))

        # 3. Display the radio button on the screen
        radio1.place(x=15, y=115)
        radio2.place(x=70, y=115)
        radio3.place(x=130, y=115)
        radio4.place(x=207, y=115)

        self.bind("<Control-b>", self.make_text_bold)
        self.bind("<Control-i>", self.make_text_italic)
        self.bind("<Control-u>", self.make_text_underline)


        # font style text
        self.image_edit_widget_canvas.create_text(58, 160, text=f"Font Design",
                                                  font=("Arial", 10, "bold"), fill="white")

        # search font entry field
        self.search_font_design_field = Entry(self.image_edit_widget_canvas, font=("Arial", 8), width=25, relief="flat")
        self.search_font_design_field.place(x=103, y=152)

        self.search_font_design_field.insert(0, "Search font style")  # adds text in search box

        self.search_font_design_field.bind("<KeyRelease>", self.search_font_design)  # calls search_font_style method

        # creating listbox for font selection
        self.select_font_design = Listbox(self.image_edit_widget_canvas, font=("Arial", 8, "bold"), width=39, height=2,
                                          highlightthickness=0)
        self.select_font_design.place(x=21, y=175)

        # Font Color text
        self.image_edit_widget_canvas.create_text(55, 230, text=f"Font Color",
                                                  font=("Arial", 10, "bold"), fill="white")

        # search font color field
        self.search_font_color_field = Entry(self.image_edit_widget_canvas, font=("Arial", 8), width=25, relief="flat")
        self.search_font_color_field.place(x=102, y=220)

        self.search_font_color_field.insert(0, "Search font color")  # adds text in search box

        self.search_font_color_field.bind("<KeyRelease>", self.search_font_color)  # calls search_font_color method

        # creating listbox for font selection
        self.select_font_color = Listbox(self.image_edit_widget_canvas, font=("Arial", 8, "bold"), width=39, height=2,
                                         highlightthickness=0)
        self.select_font_color.place(x=20, y=243)

        # Font Size text
        self.image_edit_widget_canvas.create_text(50, 300, text=f"Font Size",
                                                  font=("Arial", 10, "bold"), fill="white")

        # create font size Scale widget
        for_font_size = DoubleVar()
        self.font_size_scaler = Scale(self.image_edit_widget_canvas, variable=for_font_size, from_=1, to=100,
                                      orient="horizontal", length=236, width=10, bg="#494949", highlightthickness=0,
                                      foreground="white", activebackground="#494949",
                                      sliderrelief="flat", sliderlength=15, command=self.increase_font_size)
        self.font_size_scaler.place(x=18, y=310)

        # Rotation (°) text
        self.image_edit_widget_canvas.create_text(55, 370, text=f"Rotation (°)",
                                                  font=("Arial", 10, "bold"), fill="white")

        self.text_rotation_spinbox = Spinbox(self.image_edit_widget_canvas, from_=0, to=360, width=4, relief="sunken",
                                             repeatdelay=500, repeatinterval=100,
                                             font=("Arial", 11), bg="white", fg="#494949",
                                             command=self.rotate_watermark_text)

        self.text_rotation_spinbox.bind("<KeyRelease>", self.rotate_watermark_text)

        self.text_rotation_spinbox.place(x=100, y=360)

        # Preset Management text
        self.image_edit_widget_canvas.create_text(83, 405, text=f"Preset Management", font=("Arial", 10, "bold"), fill="white")

        # custom text alignment combobox padding
        preset_combobox_style = Style()
        preset_combobox_style.configure("Text_Alignment.TCombobox", padding=(2, 5))  # (horizontal, vertical)

        # creating combobox for presets
        self.saved_presets_options = Combobox(self.image_edit_widget_canvas, values=text_align_options,
                                      font=("Arial", 8, "bold"),
                                      state="readonly", width=17, style="Text_Alignment.TCombobox")
        self.saved_presets_options.set('Select Alignment')
        self.saved_presets_options.place(x=21, y=420)

        self.create_present_btn = Button(self.image_edit_widget_canvas, text="Create Preset", width=13, bg="gray", command=self.save_preset)
        self.create_present_btn.place(x=155, y=420)

        # creating add image button
        add_image_button = Button(self.image_edit_widget_canvas, text="Select Image", font=("Arial", 12, "bold"),
                                  fg="white",
                                  command=self.open_file_explorer, bd=0, bg="#007aff", width=18, height=2)
        add_image_button.place(x=45, y=600)

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
                                                            font=(self.current_font_family, self.current_font_size),
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

            self.new_x = image_x1 + (self.watermark_rel_x * image_width)
            self.new_y = image_y1 + (self.watermark_rel_y * image_height)
            self.image_canvas.coords(self.watermark_text, self.new_x, self.new_y)

    def on_alignment_selected(self, event=None):

        if event is not None:
            self.current_alignment = event.widget.get()

        self.watermark_mode = "alignment"  # selecting an option overrides free drag
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

            self.text_x_cord = image_left_side_coord + (image_width // 2)
            self.text_y_cord = image_top_side_coord + (image_height // 2)
            self.image_canvas.coords(self.watermark_text, self.text_x_cord, self.text_y_cord)

            return self.text_x_cord, self.text_y_cord

        elif triggered_option == "Top-Left-Corner":

            self.text_x_cord = image_left_side_coord + (text_width / 2) + 5
            self.text_y_cord = image_top_side_coord + (text_height / 2) + 5
            self.image_canvas.coords(self.watermark_text, self.text_x_cord, self.text_y_cord)

            return self.text_x_cord, self.text_y_cord

        elif triggered_option == "Bottom-Left-Corner":

            self.text_x_cord = image_left_side_coord + (text_width / 2) + 5
            self.text_y_cord = image_bottom_side_coord - (text_height / 2) - 5
            self.image_canvas.coords(self.watermark_text, self.text_x_cord, self.text_y_cord)

            return self.text_x_cord, self.text_y_cord

        elif triggered_option == "Left-Center Edge":

            self.text_x_cord = image_left_side_coord + (text_width / 2) + 5
            self.text_y_cord = image_top_side_coord + (image_height // 2)
            self.image_canvas.coords(self.watermark_text, self.text_x_cord, self.text_y_cord)

        elif triggered_option == "Top-Right-Corner":

            self.text_x_cord = image_right_side_coord - (text_width / 2) - 5
            self.text_y_cord = image_top_side_coord + (text_height / 2) + 5
            self.image_canvas.coords(self.watermark_text, self.text_x_cord, self.text_y_cord)


        elif triggered_option == "Bottom-Right-Corner":

            self.text_x_cord = image_right_side_coord - (text_width / 2) - 5
            self.text_y_cord = image_bottom_side_coord - (text_height / 2) - 5
            self.image_canvas.coords(self.watermark_text, self.text_x_cord, self.text_y_cord)

        elif triggered_option == "Right-Center Edge":

            self.text_x_cord = image_right_side_coord - (text_width / 2) - 5
            self.text_y_cord = image_top_side_coord + (image_height // 2)
            self.image_canvas.coords(self.watermark_text, self.text_x_cord,
                                     self.text_y_cord)

        elif triggered_option == "Top-Center Edge":

            self.text_x_cord = image_left_side_coord + (image_width // 2)
            self.text_y_cord = image_top_side_coord + (text_height / 2) + 5
            self.image_canvas.coords(self.watermark_text, self.text_x_cord,
                                     self.text_y_cord)

        elif triggered_option == "Bottom-Center Edge":

            self.text_x_cord = image_left_side_coord + (image_width // 2)
            self.text_y_cord = image_bottom_side_coord - (text_height / 2) - 5
            self.image_canvas.coords(self.watermark_text, self.text_x_cord,
                                     self.text_y_cord)  # getting watermark text coordinates

    # *********************************************** Update Font Style  ***********************************************

    def update_font_style(self, selected_font_style):

        if selected_font_style == "reset":
            self.current_font_style = "normal"
            self.font_style = "normal"

        else:
            self.current_font_style = selected_font_style

        font_properties = self.get_font_properties()
        self.current_font_family = font_properties["family"]
        self.current_font_size = font_properties["size"]

        self.image_canvas.itemconfig(self.watermark_text,
                                     font=(self.current_font_family, self.current_font_size, self.current_font_style))

        self.bind("<Control-b>", self.make_text_bold)
        self.bind("<Control-i>", self.make_text_italic)
        self.bind("<Control-u>", self.make_text_underline)


    def make_text_bold(self, event):
        """this method will add bold weight to the text and when user repress it it will change weight into normal"""

        font_properties = self.get_font_properties()

        font_design = font_properties["family"]
        font_size = font_properties["size"]

        # bold turns into normal
        if font_properties["weight"] == 'bold':
            self.font_style = "normal"

        # if normal turns into bold
        elif font_properties["weight"] == 'normal':
            self.font_style = "bold"

        for key, value in list(font_properties.items())[3:5]:

            if value != 0 :
                self.font_style +=   " " + value
                break

        self.image_canvas.itemconfig(self.watermark_text, font=(font_design, font_size, self.font_style))

    def make_text_italic(self, event):
        """this method will add italic to the text and when user repress it it will remove the italic slant"""

        font_properties = self.get_font_properties()

        font_design = font_properties["family"]
        font_size = font_properties["size"]
        self.font_style = font_properties["weight"]

        for key, value in list(font_properties.items())[3:]:

            if value == "roman" :
                self.font_style +=   " " + "italic"
                break

        self.image_canvas.itemconfig(self.watermark_text, font=(font_design, font_size, self.font_style))

    def make_text_underline(self, event):
        """this method will add underline to the text and when user repress it it will remove the underline"""


        font_properties = self.get_font_properties()

        font_design = font_properties["family"]
        font_size = font_properties["size"]
        font_weight = font_properties["weight"]
        font_slant = font_properties["slant"]

        self.font_style = font_weight + " " + font_slant

        # this for loop will add the underline key in the font style so that it will later gets applied.
        for key, value in list(font_properties.items())[3:5]:

            if value == 0:
                print(self.font_style)
                self.font_style += " " + key

        print(self.font_style)

        self.image_canvas.itemconfig(self.watermark_text, font=(font_design, font_size, self.font_style))


    # *********************************************** Select Font Style  ***********************************************

    def hide_widgets(self, *widgets):
        """this method will hide the widget which are appearing on top of search result when user search something in search box"""

        for widget in widgets:
            widget.place_forget()

    def make_widgets_reappear(self, *widgets_with_cords):
        """this method will make widgets reappear if listbox height are at certain level."""

        for widget, x, y in widgets_with_cords:
            widget.place(x=x, y=y)

    def get_font_properties(self):

        current_font = self.image_canvas.itemcget(self.watermark_text, "font")
        temp_font = font.Font(font=current_font)
        font_properties = temp_font.actual()

        return font_properties

    def search_font_design(self, event):
        """this method checks searched font with the font list and append the fonts which matches with the searched fonts"""

        searched_font = []

        font_design_entered = self.search_font_design_field.get()

        # this condition will prevent the font color fields to hide immediately and hides when the font style is size more than one and text be different than the condition
        if font_design_entered != "Search font style" and len(font_design_entered) >= 1:

            self.hide_widgets(self.search_font_color_field, self.select_font_color, self.font_size_scaler,
                              self.text_rotation_spinbox)

            if font_design_entered == "":
                pass

            else:
                searched_font = []

                # this for loop will check the searched font with all font and append the fonts which are matching
                for font_design in self.font_designs:

                    if font_design_entered.lower() in font_design.lower():
                        searched_font.append(font_design)

            self.display_matched_font_design(searched_font)

        # this condition will make sure when user text in search field is zero than it will show no font style and
        elif len(font_design_entered) == 0:

            searched_font = []
            self.display_matched_font_design(searched_font)
            self.select_font_design.config(height=2)

    def display_matched_font_design(self, matched_font_design):
        """this method will display all the matched fonts in the GUI so that user can later select whichever font he wants to use."""

        # deletes any current font in the listbox
        self.select_font_design.delete(0, END)

        if len(matched_font_design) == 0:
            self.select_font_design.config(height=2)

        elif len(matched_font_design) != 0:
            self.select_font_design.config(
                height=len(matched_font_design))  # creates listbox size as per the matched font result

        for font_design in matched_font_design:
            self.select_font_design.insert(END,
                                           font_design)  # here we are adding all the matched font style in the listbox.

        self.select_font_design.bind("<<ListboxSelect>>", self.apply_font_design)

        # separately, decide whether color fields should show or hide
        if len(matched_font_design) <= 2:

            self.make_widgets_reappear((self.search_font_color_field, 102, 220), (self.select_font_color, 20, 243),
                                       (self.font_size_scaler, 18, 310), (self.text_rotation_spinbox, 100, 360))

        else:

            self.hide_widgets(self.search_font_color_field, self.select_font_color, self.font_size_scaler,
                              self.text_rotation_spinbox)

    def apply_font_design(self, event):
        """this method is responsible for applying the font style to the watermark text"""

        # Returns a tuple containing the index of the selected font.
        selected_font_design = self.select_font_design.curselection()

        if not selected_font_design:
            return

        # Retrieve the font name using the selected index.
        self.current_font_design = self.select_font_design.get(selected_font_design[0])

        # once the user has retrieved the font it will delete the all fonts in the listbox.
        self.search_font_design_field.delete(0,END)

        # this will insert the selected font in the search box
        self.search_font_design_field.insert(0,self.current_font_design)

        # Collapse the listbox
        self.select_font_design.config(height=2)
        self.select_font_design.delete(0, END)

        font_properties = self.get_font_properties()
        font_size = font_properties["size"]
        font_weight = font_properties["weight"] + " " +  font_properties["slant"]

        print(font_weight)

        # applying new font style to the watermark text.
        self.image_canvas.itemconfig(self.watermark_text, font=(self.current_font_design, font_size, font_weight))

        self.current_font_family = self.current_font_design

        self.make_widgets_reappear((self.search_font_color_field, 102, 220), (self.select_font_color, 20, 243),
                                   (self.font_size_scaler, 18, 310), (self.text_rotation_spinbox, 100, 360))

    # *********************************************** Select Font Color ************************************************

    def search_font_color(self, event):
        """this method checks searched font color from the font color list and append the fonts which matches with the searched fonts"""

        font_color_entered = self.search_font_color_field.get()
        if font_color_entered != "Search font color" and len(
                font_color_entered) >= 1:  # this condition will prevent the font color fields to hide immediately and hides when the font style is size more than one and text be different than the condition

            self.hide_widgets(self.font_size_scaler, self.text_rotation_spinbox)

            searched_font_color = []

            if font_color_entered == "":
                pass

            else:
                searched_font_color = []

                for color in self.watermark_colors:  # this for loop will check the searched font color with all font color and append the font color which are matching

                    if font_color_entered.lower() in color.lower():
                        searched_font_color.append(color)

                    elif font_color_entered.lower() not in color.lower():  # this condition will prevent appearing of font size scale widget
                        searched_font = []
                        self.display_matched_font_colors(searched_font)
                        self.select_font_color.config(height=2)

            self.display_matched_font_colors(searched_font_color)

        elif len(
                font_color_entered) == 0:  # this condition will make sure when user text in search field is zero than it will show no font style and

            searched_font = []
            self.display_matched_font_colors(searched_font)
            self.select_font_color.config(height=2)

    def display_matched_font_colors(self, matched_font_color):
        """this method will display all the matched fonts colors in the GUI so that user can later select whichever font color he wants to use."""

        self.select_font_color.delete(0, END)  # deletes any current font color in the listbox

        if len(matched_font_color) > 2:
            self.select_font_color.config(
                height=len(matched_font_color))  # creates listbox size as per the matched font color result

        for font_color in matched_font_color:
            self.select_font_color.insert(END,
                                          font_color)  # here we are adding all the matched font color in the listbox.

        self.select_font_color.bind("<<ListboxSelect>>", self.apply_font_color)

        # separately, decide whether color fields should show or hide
        if len(matched_font_color) <= 4:

            self.make_widgets_reappear((self.font_size_scaler, 18, 310), (self.text_rotation_spinbox, 100, 360))

        else:
            self.hide_widgets(self.font_size_scaler, self.text_rotation_spinbox)

    def apply_font_color(self, event):
        """this method is responsible for applying the font color to the watermark text"""

        selected_font_color = self.select_font_color.curselection()  # Returns a tuple containing the index of the selected font.

        if not selected_font_color:
            return

        # Retrieve the font color name using the selected index.
        selected_color = self.select_font_color.get(selected_font_color[0])

        # once the user has retrieved the font color it will delete the all fonts color in the listbox.
        self.search_font_color_field.delete(0, END)

        # this will insert the selected font color in the search box
        self.search_font_color_field.insert(0, selected_color)

        # Collapse the listbox
        self.select_font_color.config(height=2)
        self.select_font_color.delete(0, END)

        # applying new font style to the watermark text.
        self.image_canvas.itemconfig(self.watermark_text, fill=selected_color)

        self.make_widgets_reappear((self.font_size_scaler, 18, 310), (self.text_rotation_spinbox, 100, 360))

    # ********************************************** Increase Font Size ************************************************

    def increase_font_size(self, font_size):
        """this method will increase the font size."""

        if not hasattr(self, "current_font_design"):
            self.current_font_design = "Arial"


        # applying new font style & font size to the watermark text.
        self.image_canvas.itemconfig(self.watermark_text, font=(self.current_font_design, font_size, self.font_style))

        self.scaled_font_size = font_size
        self.reposition_watermark_after_resize()

    # ********************************************** Rotate Watermark  *************************************************

    def rotate_watermark_text(self, event=None):
        """this method will update the font rotation direction into the new angle"""

        text_rotation = self.text_rotation_spinbox.get()

        # applying new font rotation to the watermark text.
        self.image_canvas.itemconfig(self.watermark_text, angle=text_rotation)

    # ********************************************** Save Watermark  *************************************************

    def save_preset(self):

        print(self.received_text)



        # print(font_properties)


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


app_window = UserInterface()
