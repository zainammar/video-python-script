from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip
)
from moviepy.audio.fx.all import audio_loop

video = VideoFileClip("merged_output.mp4")

video_audio = video.audio
music = AudioFileClip("music.mp3")

# Repeat music till end of video
music = audio_loop(music, duration=video.duration)

# Background music volume
music = music.volumex(0.15)

# Mix voice + music
final_audio = CompositeAudioClip([video_audio, music])

final_video = video.set_audio(final_audio)

final_video.write_videofile(
    "final_with_music.mp4",
    codec="libx264",
    audio_codec="aac"
)