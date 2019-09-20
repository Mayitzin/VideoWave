"""
Video Wave Creation Class
"""

from .video import Video
from .audio import Audio

class Waver:
    def __init__(self, input_video, **kw):
        self.input_video_file = input_video
        self.audio_file = kw.get("audio", None)
        self.bits = kw.get("bits", 30)

    def export(self, new_file_name):
        video = Video(self.input_video_file)
        audio = Audio(self.audio_file) if self.audio_file is not None else Audio(self.input_video_file)
        # Build waves from audio
        wave_dims = (video.num_frames, self.bits)
        waves = audio.spectral_waves(wave_dims, 1e-3, int(audio.samplerate/video.fps)).transpose()
        # Create a new video
        new_video = Video()
        new_video.create_frames(video.frames, waves)    # Put waves on top of each frame
        new_video.save_frames("./frames/")
        new_video.export_from_images(new_file_name, "./frames/", audio=audio.file_name)
