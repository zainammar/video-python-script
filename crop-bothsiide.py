from moviepy.editor import VideoFileClip

# Load video
clip = VideoFileClip("cut_video.mp4")

# Define how many pixels to cut from left & right
cut_left = 400
cut_right = 400

# Crop (x1, y1, x2, y2)
cropped = clip.crop(x1=cut_left, y1=0, x2=clip.w - cut_right, y2=clip.h)

# Save output
cropped.write_videofile("output_crop.mp4", codec="libx264")
