import os
import threading
import tkinter
from pathlib import Path

import customtkinter
import yt_dlp
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk

DEFAULT_DOWNLOAD_PATH = str(Path.home() / "Downloads")
def load_custom_theme(theme_path):
    """Loads a custom color theme from a JSON file for CustomTkinter."""
    try:
        if not os.path.exists(theme_path):
            raise FileNotFoundError(f"Theme file not found: {theme_path}")
        customtkinter.set_default_color_theme(theme_path) 
    # Missing exception for possible IO error when reading file.
    except FileNotFoundError as e:
        print(f"Error loading theme: {e}")
        customtkinter.set_default_color_theme("blue") 
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        customtkinter.set_default_color_theme("blue") 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.set_bg()
        self.download_path = DEFAULT_DOWNLOAD_PATH
        self.progress = customtkinter.CTkProgressBar(
            self, orientation="horizontal", mode="indeterminate"
        )
        self.yt_url = customtkinter.CTkEntry(
            self, placeholder_text="Your Youtube URL goes here", width=500
        )
        self.yt_url.pack()
        self.button = customtkinter.CTkButton(
            self, text="Download", command=self.start_download
        )
        self.button.pack(padx=20, pady=20)

    def set_bg(self):
        try:
            self.image = Image.open("strawberries-bg.jpg")
            self.image = self.image.resize((1920, 1080), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.background_label = tkinter.Label(self, image=self.tk_image, text="")
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            self.after(0, lambda: CTkMessagebox(title="Error", message="Background image not found!", icon="cancel"))
        except Exception as e:
            print(f"Error setting background: {e}")
            self.after(0, lambda: CTkMessagebox(title="Error", message=f"Failed to set background: {e}", icon="cancel"))

    def start_progress(self):
        self.progress.pack(padx=20, pady=40)
        self.progress.start()

    def stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()

    def start_download(self):
        threading.Thread(target=self.download_song).start()
        self.start_progress()

    def download_song(self):
        url = self.yt_url.get()
        self.yt_url._state = "disabled"
        if url == "" or None:
            self.yt_url._state = "normal"
            self.stop_progress()
            return CTkMessagebox(title="Error", message="No url set!!!", icon="cancel")
        ydl_opts = {
            "format": "bestaudio/best",
            "extractaudio": True,  # Extract audio
            "audioformat": "mp3",  # Convert to MP3
            "outtmpl": f"{self.download_path}/%(title)s.mp3",  # Output filename template
            "noplaylist": True,  # prevent downloading playlists if given a playlist url.
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.yt_url._state = "normal"
            self.stop_progress()
            return CTkMessagebox(title="File downloaded", message=f"Audio downloaded successfully to {self.download_path}",
                  icon="check", option_1="Ok")
        except yt_dlp.DownloadError as e:
            print(f"Error downloading audio: {e}")


customtkinter.set_appearance_mode("System")
load_custom_theme("themes/cherry.json")
app = App()
app.title("Ichigo")
# Missing function to handle loading icon
icon = tkinter.PhotoImage(file="icons8-strawberry.png")
app.wm_iconphoto(False, icon)
app.mainloop()
