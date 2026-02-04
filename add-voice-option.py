from moviepy.editor import *

# Input files
video_file = "/home/tnt/Videos/Project Media/Liv Sesseions/text-revel/final/merged_output.mp4"
audio_file = "/home/tnt/Videos/Project Media/Liv Sesseions/text-revel/final/music-2 (mp3cut.net).mp3"  # replace with your audio file

# Load video and audio
video = VideoFileClip(video_file)
audio = AudioFileClip(audio_file)

# Slow down audio and trim to video duration
slow_audio = audio.fl_time(lambda t: 0.3*t).set_duration(video.duration)

# Set audio to video
final_video = video.set_audio(slow_audio)

# Output file
output_file = "output_with_slow_voice.mp4"
final_video.write_videofile(output_file)