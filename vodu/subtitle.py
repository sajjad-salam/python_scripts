import re
import os
import requests

# Sample text containing subtitle links
sample_text = """
html code
"""

# Regular expression pattern to match subtitle URLs
subtitle_url_pattern = r"https://movie\.vodu\.me/subtitles/.*?_S(\d+)E(\d+)_(\d+)\.srt"
series_name="The_Walking_Dead"

# Find all subtitle matches in the sample text
subtitle_matches = re.findall(subtitle_url_pattern, sample_text)

# Specify the base directory for saving subtitles
base_directory = r"C:\Users\wtgd5\Desktop\Video\Walking-Dead"

# Create the base directory if it doesn't exist
os.makedirs(base_directory, exist_ok=True)

# Download and save subtitles to the specified path
for season_number, episode_number, subtitle_number in subtitle_matches:
    subtitle_filename = f"{series_name}_S{season_number}E{episode_number}.srt"
    subtitle_save_path = os.path.join(base_directory, subtitle_filename)
    
    subtitle_link = f"https://movie.vodu.me/subtitles/{series_name}_S{season_number}E{episode_number}_{subtitle_number}.srt"
    
    response = requests.get(subtitle_link)
    if response.status_code == 200:
        with open(subtitle_save_path, "wb") as file:
            file.write(response.content)
        print(f"Subtitle for S{season_number}E{episode_number} downloaded to {subtitle_save_path}")
    else:
        print(f"Failed to download subtitle for S{season_number}E{episode_number} from {subtitle_link}")
