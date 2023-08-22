import re
import os
import tkinter
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import time
from urllib3.exceptions import IncompleteRead
import tkinter as tk
from pathlib import Path
import tkinter
import webbrowser
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,filedialog,END,ttk,Variable,messagebox

from tkinter import Tk, scrolledtext, simpledialog, messagebox, ttk, filedialog
import customtkinter
import urllib.request
from urllib.parse import urlparse


def download_with_retry(url, save_path, max_retries=3, retry_delay=300):
    for retry in range(max_retries + 1):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception if the response status is not 200

            total_size = int(response.headers.get("content-length", 0))
            downloaded_size = 0
            with open(save_path, "wb") as file, tqdm(
                desc=os.path.basename(url),
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                start_time = time.time()
                for data in response.iter_content(chunk_size=1024):
                    bar.update(len(data))
                    downloaded_size += len(data)
                    file.write(data)
                    update_progress(downloaded_size, total_size)
            return True
        except (IncompleteRead, requests.exceptions.RequestException):
            if retry < max_retries:
                print(f"Retrying download for {url} after {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to download {url} after {max_retries} retries.")
                return False

def update_progress(downloaded_size, total_size):
    progress_value = int((downloaded_size / total_size) * 100)
    progress_bar["value"] = progress_value
    start_time = time.time()
    if progress_value > 0:
        elapsed_time = time.time() - start_time
        remaining_time = (elapsed_time / progress_value) * (100 - progress_value)
        time_remaining.config(text=f"Downloading... Estimated time remaining: {format_time(remaining_time)}")
    else:
        time_remaining.config(text="Downloading... Estimated time remaining: Calculating...")
    
    window.update_idletasks()

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"    



def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the response status is not 200
        html_content = response.text
        return html_content
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    
    
    # هاي الدالة تابعة الى الترجمة فقط 
def download_html_from_url(url,path):
    try:
        response = urllib.request.urlopen(url)
        html_content = response.read().decode("utf-8")
        
        # Generate a valid file name from the URL
        parsed_url = urlparse(url)
        file_name = parsed_url.netloc + parsed_url.path
        file_name = file_name.replace("/", "_").replace(".", "_")
        
        # Save the HTML content to a file
        save_path = os.path.join(path, f"{file_name}.html")
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        
        return html_content
    except Exception as e:
        print("Failed to download HTML content.")
        print(e)
        return None
    
    
def start_download_subtitle():
    url=text_widget.get("1.0",tk.END)
    if not url:
        messagebox.showinfo("Info", "Please enter a URL.")
        return
    
    download_path = filedialog.askdirectory(title="Choose Download Path")
    sample_text=download_html_from_url(path=download_path,url=url)
    sample_text=str(sample_text)
    subtitle_url_pattern = r"https://movie\.vodu\.me/subtitles/(.*?)_S(\d+)E(\d+)_(\d+)\.webvtt\" data-srt=\"(.*?)\.srt"
    
    subtitle_matches = re.findall(subtitle_url_pattern, sample_text)
    
    if not download_path:
        messagebox.showinfo("Info", "Download path not selected.")
        return
    
    os.makedirs(download_path, exist_ok=True)

    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, sample_text)
    text_widget.update_idletasks()
    for series_name, season_number, episode_number, _, subtitle_link in subtitle_matches:
        subtitle_filename = f"{series_name}_S{season_number}E{episode_number}.srt"
        subtitle_save_path = os.path.join(download_path, subtitle_filename)
        
        progress_bar["value"] = 0
        progress_label.config(text=f"Downloading {subtitle_filename}")
        
        if not subtitle_link.endswith(".srt"):
            subtitle_link += ".srt"
        
        if download_with_retry(subtitle_link, subtitle_save_path):
            print("done")
        else:
            print("error")
    
    progress_bar["value"] = 100
    progress_label.config(text="Download Completed")
    # result_text.insert(tk.END, "Subtitle download completed.\n")

def start_download_video():
    url = text_widget.get("1.0", tk.END).strip()
    if not url:
        messagebox.showinfo("Info", "Please enter a URL.")
        return
    
    # Extract the simple text from the URL
    sample_text = get_html_content(url)
    
    if not sample_text:
        messagebox.showinfo("Info", "Failed to extract simple text from the URL.")
        return
    
    
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, sample_text)
    text_widget.update_idletasks()
    
    video_url_pattern = r"https://\S+-360\.mp4"
    video_matches = re.findall(video_url_pattern, sample_text)
    download_path = filedialog.askdirectory(title="Choose Download Path")
    
    if not download_path:
        messagebox.showinfo("Info", "Download path not selected.")
        return
    
    os.makedirs(download_path, exist_ok=True)
    
    for video_link in video_matches:
        video_filename = os.path.basename(video_link)
        video_save_path = os.path.join(download_path, video_filename)
        
        progress_bar["value"] = 0
        progress_label.config(text=f"Downloading {video_filename}")
        
        if download_with_retry(video_link, video_save_path):
            print("done")
        else:
            print("error")
            # result_text.insert(tk.END, f"Failed to download video '{video_filename}' from {video_link}\n")
    
    progress_bar["value"] = 100
    progress_label.config(text="Download Completed")
    # result_text.insert(tk.END, "Video download completed.\n")

def show_developer_info():
    message = "Developer Information:\n\n" \
              "Name: sajjad salam\n" \
              "Email: sajjad.salam.teama@gmail.com\n" \
              "Website: https://engsajjad.000webhostapp.com \n" \
              "GitHub: https://github.com/sajjad-salam\n" \
              "LinkedIn: https://www.linkedin.com/in/sajjad-salam-963043244/ "
    
    messagebox.showinfo("Developer Information", message)


window = Tk()
window.title("vodu Downloader")
window.geometry("450x600")
window.configure(bg = "#282828")
window.iconbitmap(("vodu/gui/assets/icom.ico"))

canvas = Canvas(
    window,
    bg = "#282828",
    height = 600,
    width = 450,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)



# About Button
button_image_3 = PhotoImage(
    file="vodu/gui/assets/button_3.png")
button_3 = Button(
    command=show_developer_info,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    activebackground= "#202020",
    cursor="heart",
    relief="flat"
)
button_3.place(
    x=20.0,
    y=21.0,
    width=30.0,
    height=30.0
)


image_image_6 = PhotoImage(
    file="vodu/gui/assets/logo.png")
image_6 = canvas.create_image(
    225.0,
    37.0,
    image=image_image_6
)



# Settings Button



    
# Output Selection section
image_image_5 = PhotoImage(
    file="vodu/gui/assets/image_5.png")
image_5 = canvas.create_image(
    224.5,
    137.5,
    image=image_image_5
)


text_widget = scrolledtext.ScrolledText(canvas, width=50, height=0.1, bg="#2D2D2D")
canvas.create_window(224.5, 137.5, window=text_widget)


canvas.create_text(
    20.0,
    98.0,
    anchor="nw",
    text=" المسلسل او الفيلم رابط",
    justify="right",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)



# "Include Anonymous Intro" Toggle Button
canvas.create_text(
    75.0,
    178.0,
    anchor="nw",
    text="يجب التأكد جيدا من رابط المسلسل او الفيلم",
    fill="#FFFFFF",
    font=("Roboto Regular", 14 * -1)
)



# Download Subtitle Button
Download_subtitle_button_image = PhotoImage(
    file="vodu/gui/assets/button_subtitle.png")

Download_subtitle_button = Button(
    command=start_download_subtitle,
    image=Download_subtitle_button_image,
    borderwidth=0,
    highlightthickness=0,
    activebackground="#202020",
    relief="flat"
)
Download_subtitle_button.place(
    x=18.0,
    y=400.0,
    width=414.0,
    height=47.0
)

# Simulate existing content height (adjust this value based on your content)
existing_content_height = 300

# Download Video Button
Download_video_button_image = PhotoImage(
    file="vodu/gui/assets/button_video.png")

Download_video_button = Button(
    command=start_download_video,
    image=Download_video_button_image,
    borderwidth=0,
    highlightthickness=0,
    activebackground="#202020",
    relief="flat"
)

# Calculate y coordinate for the second button
second_button_y = max(Download_subtitle_button.winfo_y() + Download_subtitle_button.winfo_height() + 20, existing_content_height + 20)

Download_video_button.place(
    x=18.0,
    y=second_button_y,
    width=414.0,
    height=47.0
)


progress_bar = ttk.Progressbar(window, orient="horizontal", mode="determinate")
progress_bar.pack(padx=10, pady=300, side="bottom")

# Create and position the progress label
progress_label = tkinter.Label(window, text="", font=("Helvetica", 10))
progress_label.pack(side="bottom")

# Create and position the time remaining label
time_remaining = tkinter.Label(window, text="", font=("Helvetica", 10))
time_remaining.pack(side="bottom")


window.resizable(False, False)
window.mainloop()

# End of GUI Code



