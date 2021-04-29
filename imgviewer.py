"""
An image viewer written in Python using Tkinter and Pillow.
By Warren Hoeft - April 28 2021
"""

import os

from functools import partial

from tkinter import Menu, Tk, Button, Label, Toplevel, messagebox
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from PIL import ImageTk, Image

DIR_LEFT = 0
DIR_RIGHT = 1

FLIP_HORIZONTAL = 0
FLIP_VERTICAL = 1

ALERT_INFO = 0
ALERT_WARNING = 1
ALERT_ERROR = 2

HEADER = "Tk Image Viewer - "

NYI = "Not yet Implemented!"
CREDITS = "Image Viewer written in Python using Tkinter.\n\
Program written by Warren Hoeft, April 28th 2021."
HELP = "To open a new image, use File -> Open Image.\n\n\
To open a folder, use File -> Open Folder.\n\
Note when opening a folder that the first image in the folder will be displayed.\n\n\
You can cycle through any images in the currently active folder\n\
(either opened or where the currently open image is stored) by using the Next Image and Previous Image buttons.\n\n\
Use the Edit menu to perform basic image transformations.\n\n\
To save a transformed image (or save a copy of the current image elsewhere), use File -> Save Image.\n\n\
For more information, please check the README.md file distributed with this program."

class ImageViewer:
    """
        Displays images in a Tkinter window.
        Supports controls for opening and cycling between images.
    """
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Image Viewer")
        self.root.iconphoto(False, ImageTk.PhotoImage(file = "./images/icon.png"))

        menubar = Menu(self.root)
        self.root.configure(menu = menubar)

        file_menu = Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label = "Open Image", command=self.open_image)
        file_menu.add_command(label = "Open Folder", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label = "Save Image", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label = "Quit Viewer", command=self.root.quit)

        edit_menu = Menu(menubar)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(label = "Rotate Image 90 Deg Clockwise",
            command=partial(self.rotate_image, DIR_RIGHT))
        edit_menu.add_command(label = "Rotate Image 90 Deg Counterclockwise",
            command=partial(self.rotate_image, DIR_LEFT))
        edit_menu.add_separator()
        edit_menu.add_command(label = "Flip Image Vertically",
            command=partial(self.flip_image, FLIP_VERTICAL))
        edit_menu.add_command(label = "Flip Image Horizontally",
            command=partial(self.flip_image, FLIP_HORIZONTAL))

        info_menu = Menu(menubar)
        menubar.add_cascade(label = "Info", menu=info_menu)

        info_menu.add_command(label = "Image Details",
            command=self.show_img_info)
        info_menu.add_command(label = "About",
            command=self.show_about_info)
        info_menu.add_command(label = "Help",
            command=self.show_help_info)

        # TODO: Initialize an 'empty image' as placeholder while waiting for the user to view theirs
        self.curr_dir = "./images"
        self.curr_dir_images = []
        
        self.collect_image_refs()

        self.curr_img_index = 0
        self.curr_img = ImageTk.PhotoImage(file = self.curr_dir_images[self.curr_img_index])
        title = HEADER + self.curr_dir_images[self.curr_img_index]
        self.root.title(title)

        self.img_label = Label(self.root, image = self.curr_img)
        self.img_label.pack()

        button_left = Button(self.root, text = "Previous Image",
            command=partial(self.cycle_image, DIR_LEFT))
        button_left.pack()

        button_right = Button(self.root, text = "Next Image",
            command=partial(self.cycle_image, DIR_RIGHT))
        button_right.pack()


    def start_viewer(self) -> None:
        """
            Run the image viewer.
        """
        self.root.mainloop()

    def cycle_image(self, direction: int) -> None:
        """
            Listener for next and previous image buttons.
            Grabs the new image and updates the viewer.
        """
        if direction == DIR_LEFT:
            self.curr_img_index -= 1
            if self.curr_img_index < 0:
                self.curr_img_index = len(self.curr_dir_images) - 1
        elif direction == DIR_RIGHT:
            self.curr_img_index += 1
            if self.curr_img_index >= len(self.curr_dir_images):
                self.curr_img_index = 0
        else:
            self.raise_alert("Error: Invalid image cycle direction!")

        self.curr_img = ImageTk.PhotoImage(file = self.curr_dir_images[self.curr_img_index])
        self.img_label.configure(image = self.curr_img)
        title = HEADER + self.curr_dir_images[self.curr_img_index]
        self.root.title(title)

    def rotate_image(self, direction: int) -> None:
        """
            Rotate the currently loaded image Clockwise (Right) or Counterclockwise (left).
        """
        rotated_img = ImageTk.getimage(self.curr_img)
        if direction == DIR_LEFT:
            rotated_img = rotated_img.rotate(90, expand = True)
        elif direction == DIR_RIGHT:
            rotated_img = rotated_img.rotate(-90, expand = True)
        else:
            self.raise_alert("ERROR: Cannot perform rotation operation.")
        self.curr_img = ImageTk.PhotoImage(rotated_img)
        self.img_label.configure(image = self.curr_img)

    def flip_image(self, direction: int) -> None:
        """
            Mirror the currently loaded image over the vertical or horizontal axis.
        """
        flipped_img = ImageTk.getimage(self.curr_img)
        if direction == FLIP_HORIZONTAL:
            flipped_img = flipped_img.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == FLIP_VERTICAL:
            flipped_img = flipped_img.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            self.raise_alert("ERROR: Cannot perform rotation operation.")
        self.curr_img = ImageTk.PhotoImage(flipped_img)
        self.img_label.configure(image = self.curr_img)

    def open_image(self) -> None:
        """
            Listener for open image button.
            Load up an image file to view (Note: also updates active folder).
        """

        img_filepath = askopenfilename(title="Select Image to Open")

        self.curr_dir = os.path.dirname(img_filepath)
        self.curr_img = ImageTk.PhotoImage(file = img_filepath)
        self.img_label.configure(image = self.curr_img)
        title = HEADER + img_filepath
        self.root.title(title)

        self.collect_image_refs()

    def open_folder(self) -> None:
        """
            Listener for open folder button.
            Open a new folder for bulk viewing (and displays first image found).
        """
        new_dir = askdirectory(title="Select Folder to View")
        self.curr_dir = new_dir

        self.collect_image_refs()

        self.curr_img_index = 0
        self.curr_img = ImageTk.PhotoImage(file = self.curr_dir_images[self.curr_img_index])
        self.img_label.configure(image = self.curr_img)
        title = HEADER + self.curr_dir_images[self.curr_img_index]
        self.root.title(title)

    def save_image(self) -> None:
        """
            Prompt the user to save the currently viewed image.
        """
        new_img_path = asksaveasfilename(title = "Where would you like to save this image?",
            filetypes = [("PNG Image", '*.png'), ("JPEG Image", '*.jpg'), ("Bitmap Image", '*.bmp'),\
                ("GIF Image", '*.gif'), ("Icon Image", '*.ico')],
            initialdir = self.curr_dir)

        if new_img_path.endswith(".jpg"):
            img_to_save = ImageTk.getimage(self.curr_img).convert('RGB')
            img_to_save.save(new_img_path)
        else:
            img_to_save = ImageTk.getimage(self.curr_img)
            img_to_save.save(new_img_path)

    def collect_image_refs(self) -> None:
        """
            When a new directory is loaded, refresh the list of all local images (for navigation).
        """
        self.curr_dir_images = []

        for file in os.listdir(self.curr_dir):
            if self.file_supported(file):
                self.curr_dir_images.append(self.curr_dir + "/" + file)

    def file_supported(self, file_path: str) -> bool:
        """
            Confirm if a given file path is an image supported by this viewer.
        """
        valid_exts = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".ico"]
        for ext in valid_exts:
            if file_path.endswith(ext):
                return True
        return False

    def show_img_info(self) -> None:
        """
            Listener for image info button.
            Displays basic information about the currently visible image in a pop up.
            TODO: Implement this!
        """
        win = Toplevel()

        win.title("Image Details")

        img = ImageTk.getimage(self.curr_img)

        label_text = ""
        label_text += "Image Mode: " + img.mode + "\n"
        label_text += "Image Dimensions: " + str(img.size) + "\n"

        label = Label(win, text=label_text)
        label.pack(fill='x', padx=64, pady=8)

        button_done = Button(win, text="Done", command=win.destroy)
        button_done.pack(fill='x')

    def show_about_info(self) -> None:
        """
            Listener for about button.
            Displays program credits in new window.
        """
        win = Toplevel()

        win.title("About Tk Image Viewer")

        label = Label(win, text=CREDITS)
        label.pack(fill='x', padx=64, pady=8)

        button_done = Button(win, text="Done", command=win.destroy)
        button_done.pack(fill='x')

    def show_help_info(self) -> None:
        """
            Listener for help button.
            Displays basics usage instructions.
        """
        win = Toplevel()

        win.title("Help Window")

        label = Label(win, text=HELP)
        label.pack(fill='x', padx=64, pady=8)

        button_done = Button(win, text="Done", command=win.destroy)
        button_done.pack(fill='x')

    def raise_alert(self, msg: str, alert_type = ALERT_INFO) -> None:
        """
            Open alert pop up in the event there is an issue
        """
        if alert_type == ALERT_INFO:
            messagebox.showinfo(title = "Info", message = msg)
        elif alert_type == ALERT_WARNING:
            messagebox.showwarning(title = "Warning", message = msg)
        elif alert_type == ALERT_ERROR:
            messagebox.showerror(title = "Error", message = msg)
        else:
            raise ValueError("Invalid alert type!")

def main():
    """
    Program entry point.
    Initialize a new instance of the image viewer class.
    """
    my_viewer = ImageViewer()
    my_viewer.start_viewer()

if __name__ == "__main__":
    main()
