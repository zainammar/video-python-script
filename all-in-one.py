import numpy as np
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import math

# === Config ===
output_file = "styled_text.mp4"
w, h = 1280, 720
video_duration = 1
fps = 24

# Background (50% opacity red)
bg_color = (255, 0, 0)  # red
bg_opacity = 128

# Text   Immigration Assistance Only for
text = "Only"
font_path = "DejaVuSans-Bold.ttf"
font_size = 150
text_color = (255, 255, 255)  # white (0, 0, 0)  (255, 255, 255)

# === Different Text Styles ===
def make_frame_wave(t):
    bg = Image.new("RGBA", (w, h), (bg_color[0], bg_color[1], bg_color[2], bg_opacity))
    draw = ImageDraw.Draw(bg)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    progress = t / video_duration
    base_x = int(-500 + progress * (w + 500))
    base_y = h // 2

    offset_x = base_x
    for i, ch in enumerate(text):
        wave = int(20 * math.sin(2 * math.pi * (progress * 2 + i / 5)))
        draw.text((offset_x, base_y + wave), ch, font=font, fill=text_color)
        offset_x += font.getsize(ch)[0]

    return np.array(bg.convert("RGB"))

def make_frame_bounce(t):
    bg = Image.new("RGBA", (w, h), (bg_color[0], bg_color[1], bg_color[2], bg_opacity))
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(font_path, font_size)
    progress = t / video_duration
    text_w, text_h = draw.textsize(text, font=font)
    x = (w - text_w) // 2
    y = h // 2 + int(30 * abs(math.sin(progress * math.pi * 4)))
    draw.text((x, y), text, font=font, fill=text_color)
    return np.array(bg.convert("RGB"))

def make_frame_shake(t):
    bg = Image.new("RGBA", (w, h), (bg_color[0], bg_color[1], bg_color[2], bg_opacity))
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(font_path, font_size)
    progress = t / video_duration
    text_w, text_h = draw.textsize(text, font=font)
    x = (w - text_w) // 2 + int(10 * math.sin(progress * 50))
    y = (h - text_h) // 2
    draw.text((x, y), text, font=font, fill=text_color)
    return np.array(bg.convert("RGB"))

def make_frame_zoom(t):
    bg = Image.new("RGBA", (w, h), (bg_color[0], bg_color[1], bg_color[2], bg_opacity))
    draw = ImageDraw.Draw(bg)
    scale = 1 + 0.5 * (t / video_duration)
    font = ImageFont.truetype(font_path, int(font_size * scale))
    text_w, text_h = draw.textsize(text, font=font)
    x = (w - text_w) // 2
    y = (h - text_h) // 2
    draw.text((x, y), text, font=font, fill=text_color)
    return np.array(bg.convert("RGB"))

def make_frame_diagonal(t):
    bg = Image.new("RGBA", (w, h), (bg_color[0], bg_color[1], bg_color[2], bg_opacity))
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(font_path, font_size)
    progress = t / video_duration
    text_w, text_h = draw.textsize(text, font=font)
    x = int(-text_w + progress * (w + text_w))
    y = int(h - progress * (h + text_h))
    draw.text((x, y), text, font=font, fill=text_color)
    return np.array(bg.convert("RGB"))

# === Choose Style ===
style = "bounce"   # change to "bounce", "shake", "zoom", "diagonal"

style_map = {
    "wave": make_frame_wave,
    "bounce": make_frame_bounce,
    "shake": make_frame_shake,
    "zoom": make_frame_zoom,
    "diagonal": make_frame_diagonal
}

make_frame = style_map[style]

# === Generate Video ===
clip = VideoClip(make_frame, duration=video_duration)
clip.write_videofile(output_file, fps=fps)

print(f"✅ Video created with style: {style}")
