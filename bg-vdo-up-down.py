from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip  # ✅ Works on v2.2.1

# === Config ===
bg_video = "background.mp4"  # Background video
logo_image = "logo.png"      # Logo file
output_file = "final_video.mp4"
video_duration = 1           # Fixed duration in seconds
w, h = 1280, 720

# Text settings
text1 = "Revolution"
text_color = "white"
font_size = 80
font_path = "DejaVuSans-Bold.ttf"  # Font file

# === Create Text Image with Pillow ===
def create_text_image(text, filename, font_size, color):
    dummy_img = Image.new("RGBA", (2, 2))
    draw = ImageDraw.Draw(dummy_img)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()
    text_w, text_h = draw.textsize(text, font)

    padding = 20
    img_w = text_w + padding * 2
    img_h = text_h + padding * 2

    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), text, font=font, fill=color)
    img.save(filename)
    return img_w, img_h

# === Create Text Image ===
text1_w, text1_h = create_text_image(text1, "text1.png", font_size, text_color)

# === Background Video ===
bg_clip = VideoFileClip(bg_video).resize((w, h)).subclip(0, video_duration)

# === Logo Clip ===
logo_clip = (ImageClip(logo_image)
             .set_duration(video_duration)
             .resize(height=50)
             .set_position(("center", "top"))
             .margin(left=20, top=20, opacity=0))

# === Text Animation (Up → Down) ===
slide_duration = 0.5  # seconds for slide-in

text1_clip = (ImageClip("text1.png")
              .set_duration(video_duration)
              .set_position(lambda t: (
                  (w - text1_w) // 2,  # Keep X centered 2 / Right : 1  / Left :8
                  int(-text1_h + min(1, t / slide_duration) * ((h // 1.5) - text1_h // 1.5))
              )))

# === Final Composite ===
final_clip = CompositeVideoClip([bg_clip, logo_clip, text1_clip])
final_clip.write_videofile(output_file, fps=bg_clip.fps, codec="libx264", audio_codec="aac")

print("✅ Video created with text sliding from TOP to CENTER and logo.")
