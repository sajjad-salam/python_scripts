import re
import os
import requests

sample_text = """
html code
"""

subtitle_url_pattern = r"https://movie\.vodu\.me/subtitles/.*?_S(\d+)E(\d+)_(\d+)\.srt"
series_name="The_Walking_Dead"

subtitle_matches = re.findall(subtitle_url_pattern, sample_text)

base_directory = r"C:\Users\wtgd5\Desktop\Video\Walking-Dead"

os.makedirs(base_directory, exist_ok=True)

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
