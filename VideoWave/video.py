"""
Video Capture Class
"""

import cv2
import os
import sys
import subprocess
import numpy as np
from scipy.io import wavfile

class Video:
    """
    Video capture class
    """
    def __init__(self, filename=None):
        self.input_file = filename
        self.frames = []
        self.fps = None
        if self.input_file is not None:
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
        """
        Extract audio information and save it as a WAV file.
        """
        extension = kwargs.get("extension", "wav")
        audio_file = kwargs.get("output", self.input_file[:-4] + "." + extension)
        if os.path.exists(audio_file) and not force:
            return audio_file
        call = ["ffmpeg", "-i", self.input_file, "-f", extension, "-ab", "192000", "-vn", audio_file]
        completed_process = subprocess.run(call, check=True)
        if completed_process.returncode == 0:
            return audio_file
        return None

    def show_frame(self, index):
        """
        Show a frame from the given sequence.

        Wait for a 'q' keystroke to close the window.
        """
        while(True):
            image = self.frames[index]
            cv2.imshow('Frame {}'.format(index), image)
            if cv2.waitKey(0) == ord('q'):
                break

    def play(self, **kwargs):
        """
        Play video sequence
        """
        fps = kwargs.get("fps", self.fps)
        if fps is None:
            fps = 0
        step = 1 if fps == 0 else int(1000/fps)
        for idx, frame in enumerate(self.frames):
            cv2.imshow('frame', frame)
            if cv2.waitKey(step) & 0xFF == ord('q'):
                break
        if cv2.waitKey(0) & 0xFF == ord('q'):
            return None

    def save_frame(self, idx, name):
        """
        Save a single frame with the given name.
        """
        cv2.imwrite(name, self.frames[idx])

    def save_frames(self, path_to_frames, frames=None):
        """
        Save each frame of the video in the given folder
        """
        if frames is None:
            frames = self.frames
        num_frames = len(frames)
        if num_frames < 1:
            sys.exit("There are no frames to save.")
        if not os.path.exists(path_to_frames):
            os.mkdir(path_to_frames)
        num_digits = len(str(num_frames))
        for i, f in enumerate(frames):
            cv2.imwrite("{}/{:0{n}d}.png".format(path_to_frames, i, n=num_digits), f)

    def create_frames(self, frames, waves):
        height, width, ch = frames[0].shape
        num_frames, num_bits = waves.shape
        v_mid = height//2
        h_mid = width//2
        area = (10, width-10, v_mid+50, v_mid-50) # left, right, down, up
        x_line = np.linspace(area[0], area[1], num_bits, dtype='int')
        win_name = "Video"
        self.frames = []
        for i, frame in enumerate(frames):
            for bit in range(num_bits):
                p1 = (x_line[bit], v_mid - int(100*waves[i][bit]))   # Up
                p2 = (x_line[bit], v_mid + int(100*waves[i][bit]))   # Down
                cv2.line(frame, p1, p2, (255, 255, 255), thickness=5, lineType=cv2.LINE_AA)
            self.frames.append(frame)

    def export_from_images(self, output_file, path_to_frames, **kwargs):
        audio = kwargs.get("audio", None)
        fps = kwargs.get("fps", 29)
        size = kwargs.get("size", (1920, 1080))
        vcodec = kwargs.get("vcodec", "libx264")
        quality = kwargs.get("quality", 15)
        pix_fmt = kwargs.get("pix_fmt", "yuv420p")
        call = ["ffmpeg"]
        call += ["-i", path_to_frames+"%03d.png"]
        if audio is not None:
            call += ["-i", audio]
        call += ["-r", str(fps)]
        call += ["-s", "x".join([str(s) for s in size])]
        call += ["-vcodec", vcodec]
        call += ["-crf", str(quality)]
        call += ["-pix_fmt", pix_fmt]
        call += [output_file]
        completed_process = subprocess.run(call, check=True)

    def __del__(self):
        if hasattr(self, 'capture'):
            self.capture.release()
