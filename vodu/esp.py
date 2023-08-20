import re
import os
import requests
from tqdm import tqdm 

sample_text = """
html code 
"""



video_url_pattern = r"https://\S+\.mp4"

series_name="The_Walking_Dead"

video_matches = re.findall(video_url_pattern, sample_text)

base_directory = r"C:\Users\wtgd5\Desktop\Video\Walking Dead"

os.makedirs(base_directory, exist_ok=True)
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
