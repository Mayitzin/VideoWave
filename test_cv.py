"""
Test Video and Frame conversion with OpenCV

@author: Mario Garcia
"""

import cv2
from video import Video
from audio import Audio
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

def show_frame(frames, index):
    """
    Show a frame from the given sequence.

    Wait for a 'q' keystroke to close the window.
    """
    while(True):
        cv2.imshow('Frame {}'.format(index), frames[index])
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

def get_frames(cap_obj, channel=None):
    """
    Return a list of frames from a given capture object.
    """
    frames = []
    while(cap_obj.isOpened()):
        ret, frame = cap_obj.read()
        if ret is False:
            break
        if channel is not None:
            frame = frame[:, :, channel]
        frames.append(frame)
    return frames

def play_sequence(frames):
    """
    Play a sequence of frames.
    """
    num_frames = len(frames)
    for idx, frame in enumerate(frames):
        cv2.imshow("Frame {}".format(idx), frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def play_video(capture):
    while(capture.isOpened()):
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def show_audio(data, samplerate, span=None):
    """
    Show audio channels
    """
    num_samples, num_channels = data.shape
    is_stereo = num_channels == 2
    start, end = 0, num_samples
    if span != None:
        start, end = span
    fig = plt.figure("Audio")
    if is_stereo:
        for i in range(2):
            ax = plt.subplot(2, 1, i+1)
            ax.plot(data[start:end, i])
    else:
        plt.plot(data[start:end])
    plt.show()

def show_spectrogram(data, samplerate):
    fps = 25.0
    fqs, times, spg = signal.spectrogram(data, samplerate, nperseg=int(samplerate/fps))
    plt.plot(spg.sum(axis=0))
    plt.plot(spg.sum(axis=1))
    # plt.pcolormesh(times, fqs, spg)
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    plt.show()

file_name = 'MexicoDeclaresWar.mp4'

audio = Audio(file_name)
# begin, end = 0.5, 3.5
# span = [int(begin*audio.samplerate), int(end*audio.samplerate)]
# show_audio(audio.data, audio.samplerate, span=span)
# print(audio.samplerate)
show_spectrogram(audio.data[:, 0], audio.samplerate)


# # cap = cv2.VideoCapture(file_name) # Opens capture with file
# # frames = get_frames(cap, 0)
# # play_sequence(frames)

# # cap.release()   # Closes cap
# # # cv2.destroyAllWindows()

# videoCap = Video(file_name)
# audio_data = videoCap.audio_data
# audio_samplerate = videoCap.audio_samplerate

# # secs_to_plot = 1
# # show_audio(audio_data, audio_samplerate, span=[0, secs_to_plot*audio_samplerate])
# frequencies, times, spectrogram = signal.spectrogram(audio_data[:, 1], audio_samplerate)
# print(spectrogram.shape)
# print(videoCap.num_frames)
# print("Reshape to {}:1".format(spectrogram.shape[1]/videoCap.num_frames))
# # plt.pcolormesh(times, frequencies, spectrogram)
# # plt.ylabel('Frequency [Hz]')
# # plt.xlabel('Time [sec]')
# # plt.show()

# del videoCap

