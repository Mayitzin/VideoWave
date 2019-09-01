"""
Video Capture Class
"""

import cv2
import os
import subprocess
from scipy.io import wavfile

class Video:
    """
    Video capture class
    """
    def __init__(self, filename):
        self.input_file = filename
        self.capture = cv2.VideoCapture(filename)
        self.update_info()

    def update_info(self):
        self.fps = float(self.capture.get(cv2.CAP_PROP_FPS))
        self.num_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.shape = (int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
        self.height, self.width = self.shape
        self.monochrome = self.capture.get(cv2.CAP_PROP_MONOCHROME)
        self.frames = self.get_frames()
        self.audio_file = self.set_audio_file()
        if os.path.exists(self.audio_file):
            self.audio_samplerate, self.audio_data = wavfile.read(self.audio_file)

    def get_frames(self, channel=None):
        """
        Return a list of frames from a given capture object.
        """
        frames = []
        while(self.capture.isOpened()):
            ret, frame = self.capture.read()
            if ret is False:
                break
            if channel is not None:
                frame = frame[:, :, channel]
            frames.append(frame)
        return frames

    def set_audio_file(self, force=False, **kwargs):
        extension = kwargs.get("extension", "wav")
        audio_file = kwargs.get("output", self.input_file[:-4] + "." + extension)
        if os.path.exists(audio_file) and not force:
            return audio_file
        call = ["ffmpeg", "-i", self.input_file, "-f", extension, "-ab", "192000", "-vn", audio_file]
        completed_process = subprocess.run(call, check=True)
        if completed_process.returncode == 0:
            return audio_file
        return None

    def __del__(self):
        self.capture.release()
