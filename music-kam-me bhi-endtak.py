from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_loop

video = VideoFileClip("merged_output.mp4")

# Music load
music = AudioFileClip("music.mp3")

# Music ko video duration tak repeat karo
music = audio_loop(music, duration=video.duration)

# Volume kam karni ho to
music = music.volumex(0.2)

# Music set karo
final_video = video.set_audio(music)

final_video.write_videofile(
    "final_with_music.mp4",
    codec="libx264",
    audio_codec="aac"
)

video.close()
music.close()
final_video.close()from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_loop

video = VideoFileClip("merged_output.mp4")

# Music load
music = AudioFileClip("music.mp3")

# Music ko video duration tak repeat karo
music = audio_loop(music, duration=video.duration)

# Volume kam karni ho to
music = music.volumex(0.2)

# Music set karo
final_video = video.set_audio(music)

final_video.write_videofile(
    "final_with_music.mp4",
    codec="libx264",
    audio_codec="aac"
)

video.close()
music.close()
final_video.close()