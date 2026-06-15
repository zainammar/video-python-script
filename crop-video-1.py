from moviepy.editor import VideoFileClip

# === INPUT SETTINGS ===
input_video = "input.webm"      # Input video file
output_video = "cut_video.mp4" # Output file
start_time = 0           # Start time in seconds
end_time = 27    # End time in seconds

# === LOAD VIDEO ===
video = VideoFileClip(input_video)

# === CUT VIDEO ===
cut_video = video.subclip(start_time, end_time)

# === EXPORT RESULT ===
cut_video.write_videofile(output_video, codec="libx264", audio_codec="aac")
