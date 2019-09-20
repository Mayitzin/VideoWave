"""
Audio Class
"""

import os
import subprocess
import numpy as np
import cv2
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

FFMPEG_SUPPORTED_VIDEO_FORMATS = [
"3dostr", "3g2", "3gp", "4xm", "a64", "aa", "aac", "ac3", "acm", "act", "adf",
"adp", "ads", "adts", "adx", "aea", "afc", "aiff", "aix", "alaw", "alias_pix",
"amr", "amrnb", "amrwb", "anm", "apc", "ape", "apng", "aptx", "aptx_hd",
"aqtitle", "asf", "asf_o", "asf_stream", "ass", "ast", "au", "avi", "avisynth",
"avm2", "avr", "avs", "avs2", "bethsoftvid", "bfi", "bfstm", "bin", "bink",
"bit", "bmp_pipe", "bmv", "boa", "brender_pix", "brstm", "c93", "caf",
"cavsvideo", "cdg", "cdxl", "cine", "codec2", "codec2raw", "concat", "crc",
"dash", "data", "daud", "dcstr", "dds_pipe", "dfa", "dhav", "dirac", "dnxhd",
"dpx_pipe", "dsf", "dshow", "dsicin", "dss", "dts", "dtshd", "dv", "dvbsub",
"dvbtxt", "dvd", "dxa", "ea", "ea_cdata", "eac3", "epaf", "exr_pipe", "f32be",
"f32le", "f4v", "f64be", "f64le", "ffmetadata", "fifo", "fifo_test",
"film_cpk", "filmstrip", "fits", "flac", "flic", "flv", "framecrc",
"framehash", "framemd5", "frm", "fsb", "g722", "g723_1", "g726", "g726le",
"g729", "gdigrab", "gdv", "genh", "gif", "gif_pipe", "gsm", "gxf", "h261",
"h263", "h264", "hash", "hcom", "hds", "hevc", "hls", "hnm", "ico", "idcin",
"idf", "iff", "ifv", "ilbc", "image2", "image2pipe", "ingenient", "ipmovie",
"ipod", "ircam", "ismv", "iss", "iv8", "ivf", "ivr", "j2k_pipe", "jacosub",
"jpeg_pipe", "jpegls_pipe", "jv", "kux", "latm", "lavfi", "libopenmpt",
"live_flv", "lmlm4", "loas", "lrc", "lvf", "lxf", "m4v", "matroska",
"matroska", "md5", "mgsts", "microdvd", "mjpeg", "mjpeg_2000",
"mkvtimestamp_v2", "mlp", "mlv", "mm", "mmf", "mov", "mov", "mp2", "mp3",
"mp4", "mpc", "mpc8", "mpeg", "mpeg1video", "mpeg2video", "mpegts",
"mpegtsraw", "mpegvideo", "mpjpeg", "mpl2", "mpsub", "msf", "msnwctcp", "mtaf",
"mtv", "mulaw", "musx", "mv", "mvi", "mxf", "mxf_d10", "mxf_opatom", "mxg",
"nc", "nistsphere", "nsp", "nsv", "null", "nut", "nuv", "oga", "ogg", "ogv",
"oma", "opus", "paf", "pam_pipe", "pbm_pipe", "pcx_pipe", "pgm_pipe",
"pgmyuv_pipe", "pictor_pipe", "pjs", "pmp", "png_pipe", "ppm_pipe", "psd_pipe",
"psp", "psxstr", "pva", "pvf", "qcp", "qdraw_pipe", "r3d", "rawvideo",
"realtext", "redspark", "rl2", "rm", "roq", "rpl", "rsd", "rso", "rtp",
"rtp_mpegts", "rtsp", "s16be", "s16le", "s24be", "s24le", "s32be", "s32le",
"s337m", "s8", "sami", "sap", "sbc", "sbg", "scc", "sdl", "sdp", "sdr2", "sds",
"sdx", "segment", "ser", "sgi_pipe", "shn", "siff", "singlejpeg", "sln",
"smjpeg", "smk", "smoothstreaming", "smush", "sol", "sox", "spdif", "spx",
"srt", "stl", "subviewer", "subviewer1", "sunrast_pipe", "sup", "svag", "svcd",
"svg_pipe", "swf", "tak", "tedcaptions", "tee", "thp", "tiertexseq",
"tiff_pipe", "tmv", "truehd", "tta", "tty", "txd", "ty", "u16be", "u16le",
"u24be", "u24le", "u32be", "u32le", "u8", "v210", "v210x", "vag", "vc1",
"vc1test", "vcd", "vfwcap", "vidc", "vividas", "vivo", "vmd", "vob", "vobsub",
"voc", "vpk", "vplayer", "vqf", "w64", "wav", "wc3movie", "webm", "webp",
"webp_pipe", "webvtt", "wsaud", "wsd", "wsvqa", "wtv", "wv", "wve", "xa",
"xbin", "xmv", "xpm_pipe", "xvag", "xwd_pipe", "xwma", "yop", "yuv4mpegpipe"]

class Audio:
    """
    Audio capture class
    """
    def __init__(self, filename, **kwargs):
        self.input_file = filename if os.path.exists(filename) else None
        self.audio_format = kwargs.get("fmt", "wav")
        self.is_video = self.is_video_file()
        self.file_name = self.input_file[:-4]+"."+self.audio_format if self.is_video else self.input_file
        if not os.path.exists(self.file_name):
            self.file_name = self.from_video(output=self.file_name)
        self.samplerate, self.data = wavfile.read(self.file_name)
        self.samples = self.data.shape[0]
        self.channels, self.is_stereo = 1, False
        if self.data.ndim > 1:
            self.channels = self.data.shape[1]
            self.is_stereo = True

    def from_video(self, **kwargs):
        extension = kwargs.get("format", "wav")
        audio_file = kwargs.get("output", self.input_file[:-4]+"."+extension)
        call = ["ffmpeg", "-i", self.input_file, "-f", extension, "-vn", audio_file]
        completed_process = subprocess.run(call)
        if completed_process.returncode == 0:
            return audio_file
        return None

    def is_video_file(self):
        if os.path.splitext(self.input_file)[1][1:] in FFMPEG_SUPPORTED_VIDEO_FORMATS:
            return True
        return False

    def spectral_waves(self, shape, threshold, nps=None):
        _, _, spg = signal.spectrogram(self.data[:, 0], self.samplerate, nperseg=nps)
        spg /= spg.max()    # Normalize spectrogram
        # Remove empty spaces
        _, th_bin = cv2.threshold(spg, threshold, 1.0, cv2.THRESH_BINARY)
        nzrs = np.nonzero(th_bin.sum(axis=1))
        _, th_trc = cv2.threshold(spg[np.min(nzrs):np.max(nzrs), :], threshold, 1.0, cv2.THRESH_TRUNC)
        # Reshape spectrogram
        resized = cv2.resize(th_trc, shape, interpolation=cv2.INTER_AREA)
        resized /= resized.max()
        return resized

    def show_data(self, span=None):
        """
        Show audio channels

        Parameters
        ----------
        span : list
            Start and end, in seconds, of audio to show.

        Examples
        --------
        >>> audio = Audio('some_file.mp4')
        >>> audio.show_data([1.5, 3.5])

        """
        num_samples, num_channels = self.data.shape
        is_stereo = num_channels == 2
        start, end = 0, num_samples
        if span != None:
            # start, end = span
            start = int(span[0]*self.samplerate)
            end = int(span[1]*self.samplerate)
        fig = plt.figure("Audio")
        if is_stereo:
            for i in range(2):
                ax = plt.subplot(2, 1, i+1)
                ax.plot(self.data[start:end, i], lw=0.5)
        else:
            plt.plot(self.data[start:end])
        plt.show()

