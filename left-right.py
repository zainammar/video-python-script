from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

# === Config ===
bg_video = "background.mp4" # Background video
logo_image = "logo.png" # Logo file
output_file = "final_video.mp4"
video_duration = 2 # Fixed duration in seconds
w, h = 1280, 720

# Text settings
text1 = "The href Attribute"
# text2 = "DATE Nov 7, 2024"
text_color = "white"
font_size = 80
font_path = "DejaVuSans-Bold.ttf" # Font file

# === Create Text Image with Pillow ===
def create_text_image(text, filename, font_size, color):
    dummy_img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Pillow 10+ : use textbbox instead of textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    padding = 20
    img_w = text_w + padding * 2
    img_h = text_h + padding * 2

    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), text, font=font, fill=color)
    img.save(filename)
    return img_w, img_h

# === Create Text Images ===
text1_w, text1_h = create_text_image(text1, "text1.png", font_size, text_color)
# text2_w, text2_h = create_text_image(text2, "text2.png", font_size, text_color)

# === Background Video ===
bg_clip = VideoFileClip(bg_video).resized((w, h)).subclipped(0, video_duration)

# === Logo Clip ===
logo_clip = (ImageClip(logo_image)
          .with_duration(video_duration)
          .resized(height=50)
          .with_position((20, 20))) # 20px from left, 20px from top

# === Text Animations ===
slide_duration = 1 # seconds for slide-in

text1_clip = (ImageClip("text1.png")
           .with_duration(video_duration)
           .with_position(lambda t: (
                  int(-text1_w + min(1, t / slide_duration) * (w // 2 + text1_w // 2)),
                  (h // 2) - text1_h - 20 # control center up/down
              )))

# text2_clip = (ImageClip("text2.png")
#.with_duration(video_duration)
#.with_position(lambda t: (
# int(-text2_w + min(1, t / slide_duration) * (w // 2 + text2_w // 2)),
# (h // 2) + 20 # Below center
# )))

# === Final Composite ===
final_clip = CompositeVideoClip([bg_clip, logo_clip, text1_clip])
final_clip.write_videofile(output_file, fps=bg_clip.fps, codec="libx264", audio_codec="aac")

print("✅ Video created with two animated texts and logo.")