from moviepy.editor import VideoFileClip, AudioFileClip

video = VideoFileClip("merged_output.mp4")
music = AudioFileClip("music.mp3")

music = music.subclip(0, min(music.duration, video.duration))

final_video = video.set_audio(music)

final_video.write_videofile(
    "final_with_music.mp4",
    codec="libx264",
    audio_codec="aac"
)

video.close()
music.close()