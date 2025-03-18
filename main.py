import customtkinter
from pathlib import Path
import yt_dlp
import threading

DEFAULT_DOWNLOAD_PATH = str(Path.home() / "Downloads")


def download_audio(url, output_path="."):
    """Downloads audio from a YouTube URL as an MP3 file.

    Args:
        url: The YouTube URL.
        output_path: The directory to save the downloaded audio. Defaults to the current directory.
    """
    ydl_opts = {
        "format": "bestaudio/best",  # Select the best audio quality
        "extractaudio": True,  # Extract audio
        "audioformat": "mp3",  # Convert to MP3
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",  # Output filename template
        "noplaylist": True,  # prevent downloading playlists if given a playlist url.
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Audio downloaded successfully to {output_path}")

    except yt_dlp.DownloadError as e:
        print(f"Error downloading audio: {e}")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.download_path = DEFAULT_DOWNLOAD_PATH
        self.download_thread = threading.Thread(target=self.download_song)
        self.progress = customtkinter.CTkProgressBar(
            self, orientation="horizontal", mode="indeterminate"
        )
        self.label = customtkinter.CTkLabel(
            self, text="Test text", fg_color="transparent"
        )
        self.label.pack()
        self.button = customtkinter.CTkButton(
            self, text="my button", command=self.download_thread.start
        )
        self.button.pack(padx=20, pady=20)

    def button_callbck(self):
        print("button clicked")

    def start_progress(self):
        self.progress.pack(pady=20, padx=20)
        self.progress.start()

    def stop_progress(self):
        self.progress.stop()
        self.progress.destroy()

    def download_song(self):
        dialog = customtkinter.CTkInputDialog(
            text="Your youtube video URL:", title="Test"
        )
        url = dialog.get_input()
        dialog.destroy()
        if url == "" or url == None:
            return
        self.start_progress()
        ydl_opts = {
            "format": "bestaudio/best",  # Select the best audio quality
            "extractaudio": True,  # Extract audio
            "audioformat": "mp3",  # Convert to MP3
            "outtmpl": f"{self.download_path}/%(title)s.%(ext)s",  # Output filename template
            "noplaylist": True,  # prevent downloading playlists if given a playlist url.
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Audio downloaded successfully to {self.download_path}")
            self.stop_progress()
        except yt_dlp.DownloadError as e:
            print(f"Error downloading audio: {e}")


app = App()
app.mainloop()
