"""
Test Video and Frame manipulation with VideoWave

New method with ffmpeg:

  ffmpeg -i clip.mp4 -lavfi showspectrumpic=s=675x30:legend=False spectrogram.png

- Useful to get the values faster than with the previous method.
- It can get rid of the need for scipy for the spectrogram.
- The options of showspectrumpic can be set to get the desired output. See
  https://ffmpeg.org/ffmpeg-filters.html#showspectrumpic

@author: Mario Garcia
"""

import VideoWave as vw
wave_clip = vw.Waver("clip.mp4")
wave_clip.export("my_new_video.mp4", size=(640, 480))
