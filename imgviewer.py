"""
An image viewer written in Python using Tkinter and Pillow.
By Warren Hoeft - April 28 2021
"""

import os

from functools import partial

from tkinter import Menu, Tk, Button, Label, messagebox
from tkinter.filedialog import askdirectory, askopenfilename
from PIL import ImageTk

DIR_LEFT = 0
DIR_RIGHT = 1

FLIP_HORIZONTAL = 0
FLIP_VERTICAL = 1

ALERT_INFO = 0
ALERT_WARNING = 1
ALERT_ERROR = 2

NYI = "Not yet Implemented!"

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
            command=partial(self.rotate_image, FLIP_VERTICAL))
        edit_menu.add_command(label = "Flip Image Horizontally",
            command=partial(self.rotate_image, FLIP_HORIZONTAL))

        info_menu = Menu(menubar)
        menubar.add_cascade(label = "Info", menu=info_menu)

        info_menu.add_command(label = "Image Details")
        info_menu.add_command(label = "About")
        info_menu.add_command(label = "Help")

        # TODO: Initialize an 'empty image' as placeholder while waiting for the user to view theirs
        self.curr_dir = "./images/"
        self.curr_img = ImageTk.PhotoImage(file = "./images/7Days.jpg")
        self.curr_dir_images = []
        self.curr_img_index = 0
        self.img_label = Label(self.root, image = self.curr_img)
        self.img_label.pack()

        button_left = Button(self.root, text = "Previous Image",
            command=partial(self.cycle_image, DIR_LEFT))
        button_left.pack()

        button_right = Button(self.root, text = "Next Image",
            command=partial(self.cycle_image, DIR_RIGHT))
        button_right.pack()

        self.collect_image_refs()

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

    def rotate_image(self, direction: int) -> None:
        """
            Rotate the currently loaded image Clockwise (Right) or Counterclockwise (left).
        """
        self.raise_alert(NYI, alert_type=ALERT_WARNING)

    def flip_image(self, direction: int) -> None:
        """
            Mirror the currently loaded image over the vertical or horizontal axis.
        """
        self.raise_alert(NYI, alert_type=ALERT_WARNING)

    def open_image(self) -> None:
        """
            Listener for open image button.
            Load up an image file to view (Note: also updates active folder).
        """

        img_filepath = askopenfilename(title="Select Image to Open")

        self.curr_dir = os.path.dirname(img_filepath)
        self.curr_img = ImageTk.PhotoImage(file = img_filepath)
        self.img_label.configure(image = self.curr_img)

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

    def save_image(self) -> None:
        """
            Prompt the user to save the currently viewed image.
        """
        self.raise_alert(NYI, alert_type=ALERT_WARNING)

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
