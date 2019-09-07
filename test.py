"""
Test Video and Frame conversion with OpenCV

@author: Mario Garcia
"""

import cv2
from video import Video
from audio import Audio

file_name = 'MexicoDeclaresWar.mp4'

video = Video(file_name)
audio = Audio(file_name)

num_bits = 30
swaves = audio.spectral_waves((video.num_frames, num_bits), 1e-3, int(audio.samplerate/video.fps)).transpose()

new_video = Video()
new_video.create_frames(video.frames, swaves)
new_video.save_frames("./frames/")
new_video.export_from_images("my_new_video.mp4", "./frames/",
                            audio="MexicoDeclaresWar.wav",
                            fps=video.fps,
                            size=tuple(reversed((video.shape))))


# out_file = "output.mp4"
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# # fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter(out_file, fourcc, video.fps, video.shape)
# for frame in new_frames:
#     out.write(frame)
# out.release()
