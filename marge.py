from moviepy.editor import VideoFileClip, concatenate_videoclips

# List of video files to merge
video_files = [
    "video1.mp4",
    "video2.mp4",
    "video3.mp4",
    "video4.mp4",
    "video5.mp4"
    # "video6.mp4"
    # "video7.mp4",
    # "video8.mp4"
]

# Load video clips
clips = [VideoFileClip(v) for v in video_files]

# Merge videos (no effects)
final_video = concatenate_videoclips(clips, method="compose")

# Export final video
final_video.write_videofile("merged_output.mp4", codec="libx264", audio_codec="aac")
