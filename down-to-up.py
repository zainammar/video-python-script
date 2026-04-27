from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

# === Config ===
bg_video = "background.mp4"
logo_image = "logo.png"
output_file = "final_video.mp4"
video_duration = 2
w, h = 1280, 720

# Text settings
text1 = "Study\n Learning\n Management\n System"
text_color = "white"
font_size = 40
font_path = "DejaVuSans-Bold.ttf"

# === Create Text Image with Pillow 10+ ===
def create_text_image(text, filename, font_size, color):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    dummy_img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

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
bg_clip = VideoFileClip(bg_video).resized((w, h)).subclipped(0, video_duration)

# === Logo Clip ===
logo_clip = (ImageClip(logo_image)
          .with_duration(video_duration)
          .resized(height=100)
          .with_position(("center", 20))) # 20px from top

# === Text Animation (Bottom → Center) ===
slide_duration = 0.5

# Fix: Remove.resized() if you're animating position manually
# This keeps the clip size constant so masking works
start_y = h # Start below screen
end_y = (h - text1_h) // 2 # End at center

text1_clip = (ImageClip("text1.png")
           .with_duration(video_duration)
           .with_position(lambda t: (
                "center", # X: auto-center, avoids mask errors
                int(start_y - min(1, t / slide_duration) * (start_y - end_y)) # Y: bottom to center
            )))

# === Final Composite ===
final_clip = CompositeVideoClip([bg_clip, logo_clip, text1_clip], size=(w, h))
final_clip.write_videofile(output_file, fps=bg_clip.fps, codec="libx264", audio_codec="aac")

print("✅ Video created with text sliding from BOTTOM to CENTER and logo.")