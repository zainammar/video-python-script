from moviepy.editor import *

# Input files
video_file = "/home/tnt/Videos/Project Media/Liv Sesseions/text-revel/final/a5.mp4"
audio_file = "/home/tnt/Videos/Project Media/Liv Sesseions/text-revel/final/a5.mp3"  # replace with your audio file

# Load video and audio
video = VideoFileClip(video_file)
audio = AudioFileClip(audio_file)

# Set audio to video
final_video = video.set_audio(audio)

# Output file
output_file = "output_with_music.mp4"
final_video.write_videofile(output_file)