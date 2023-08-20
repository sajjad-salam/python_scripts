import re
import os
import requests
from tqdm import tqdm  # Import tqdm library

# Sample text containing video links
sample_text = """
html code 
"""

# Regular expression pattern to match video URLs
video_url_pattern = r"https://\S+\.mp4"
series_name="The_Walking_Dead"
# Find all video matches in the sample text
video_matches = re.findall(video_url_pattern, sample_text)

# Specify the base directory for saving videos
base_directory = r"C:\Users\wtgd5\Desktop\Video\Walking Dead"

# Create the base directory if it doesn't exist
os.makedirs(base_directory, exist_ok=True)

# Download and save videos to the specified path with progress bar
for video_link in tqdm(video_matches, desc="Downloading Videos"):
    video_filename = os.path.basename(video_link)
    video_save_path = os.path.join(base_directory, video_filename)
    
    response = requests.get(video_link, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    
    with open(video_save_path, "wb") as file, tqdm(
        desc=video_filename,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            bar.update(len(data))
            file.write(data)

print("Video download completed.")
