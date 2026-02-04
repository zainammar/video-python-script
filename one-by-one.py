import numpy as np
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import cv2
# === Config ===
output_file = "text_reveal.mp4"
w, h = 1080, 1920
video_duration = 2  # increased duration
text_duration = 1  # duration for text reveal
fps = 24
video_bg_file = "/home/tnt/Videos/Project Media/Liv Sesseions/text-revel/final/background.mp4"  
text = "Contact:\n\n\n\nvirtualteck.com"
# Contact: virtualteck.com
# starting at $145
# Smart Digital Solutions
# Real Business Growth
font_path = "DejaVuSans-Bold.ttf"
font_size = 100
text_color = "white"
text_speed = 12  # characters per second

# === Create Text Frames (letter by letter) ===
def make_frame(t):
    # Get video frame
    frame = video_clip.get_frame(t)
    bg = Image.fromarray(frame)

    # Calculate how many characters to show at this time
    if t < text_duration:
        progress = t / text_duration
        chars_to_show = int(len(text) * progress)
        current_text = text[:chars_to_show]
    else:
        current_text = text  # show full text after text_duration

    # Draw text
    draw = ImageDraw.Draw(bg)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Get text size
    text_w, text_h = draw.textsize(current_text, font=font)
    pos = ((w - text_w) // 3, (h - text_h) // 3)

    # Draw text
    draw.text(pos, current_text, font=font, fill=text_color)

    return np.array(bg)

# Load video background
video_clip = VideoFileClip(video_bg_file).subclip(0, video_duration).resize((w, h))

# === Generate Video ===
clip = VideoClip(make_frame, duration=video_duration)
clip.write_videofile(output_file, fps=fps)