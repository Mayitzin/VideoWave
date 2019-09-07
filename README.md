# VideoWaves

This small application creates a sound wave and super impose it on each frame of a video.

## Requirements

- opencv
- scipy
- numpy

## Usage

```python
from video import Video
from audio import Audio
file_name = 'some_video.mp4'
video = Video(file_name)
audio = Audio(file_name)

num_bits = 30
waves = audio.spectral_waves((video.num_frames, num_bits), 1e-3, int(audio.samplerate/video.fps)).transpose()
new_video = Video()
new_video.create_frames(video.frames, waves)
new_video.save_frames("./frames/")
new_video.export_from_images("my_new_video.mp4", "./frames/", audio="some_audio.wav")
```
