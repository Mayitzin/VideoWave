"""
Test Video and Frame manipulation with VideoWave

@author: Mario Garcia
"""

import VideoWave as vw
wave_clip = vw.Waver("clip.mp4")
wave_clip.export("my_new_video.mp4", size=(640, 480))
