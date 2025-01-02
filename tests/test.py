"""
Test Video and Frame manipulation with VideoWave


The options of showspectrumpic can be set to get the desired output. See
https://ffmpeg.org/ffmpeg-filters.html#showspectrumpic for more information.

@author: Mario Garcia
"""

import subprocess
import re

class FFMPEG:
    def __init__(self, input_file, **kwargs):
        self.input_file = input_file
        self.call = ["ffmpeg", "-i", self.input_file]

    def _execute(self, call):
        completed_process = subprocess.run(call, check=True)
        if completed_process.returncode == 0:
            print("Process completed successfully.")
        else:
            print("Error executing process.")
            print(completed_process.stderr)

    def parse_resolution(self, resolution):
        if isinstance(resolution, str):
            pair = resolution.split("x")
        return tuple(map(int, pair))

    def get_metadata(self):
        """Get video metadata with ffmpeg and regex"""
        # Call ffmpeg and read the output
        call = self.call + "-hide_banner -f mp4 /dev/null -n".split()
        completed_process = subprocess.run(call, check=True, stdin=subprocess.PIPE, capture_output=True, text=True)
        if completed_process.returncode == 0:
            print("Metadata obtained.")
        else:
            print("Error getting metadata.")
            print(completed_process.stderr)
        metadata = dict.fromkeys(['Duration', 'start', 'bitrate', 'codec', 'pixel_format', 'resolution', 'bitrate', 'fps', 'tbr'], '')
        # Update Duration line in metadata dict
        pattern_duration = re.compile(r"Duration: (\d{2}:\d{2}:\d{2}\.\d{2}), start: (\d+\.\d+), bitrate: (\d+ kb/s)")
        matches = pattern_duration.search(completed_process.stderr)
        if len(matches.groups()) != 3:
            raise ValueError(f"Expected 3 matches from Duration line. Got {len(matches.groups())}.")
        metadata['Duration'], metadata['start'], metadata['bitrate'] = matches.groups()
        # Update Video line in metadata dict
        pattern_video = r"Video: (\w+) \(\w+\) \(\w+ / \w+\), (\w+\(progressive\)), (\d+x\d+), (\d+ kb/s), (\d+) fps, (\d+) tbr"
        matches = re.search(pattern_video, completed_process.stderr)
        if len(matches.groups()) != 6:
            raise ValueError(f"Expected 6 matches from Video line. Got {len(matches.groups())}.")
        metadata.update(dict(zip(['codec', 'pixel_format', 'resolution', 'bitrate', 'fps', 'tbr'], matches.groups())))
        #     print(matches.groups())
        #     # metadata.update(dict(zip(['codec', 'pixel_format', 'resolution', 'bitrate', 'fps', 'tbr'], matches.groups())))
        #     # codec = matches.group(1)
        #     # pixel_format = matches.group(2)
        #     # resolution = matches.group(3)
        #     # bitrate = matches.group(4)
        #     # fps = matches.group(5)
        #     # tbr = matches.group(6)
        #     # print(codec, pixel_format, resolution, bitrate, fps, tbr)
        print(metadata)
        # Extract the metadata from the lines
        # Return the metadata as dictionary


    def create_spectrogram(self, output_file):
        call_str = f"-lavfi showspectrumpic=s=675x30:legend=False -update 1 -frames:v 1 {output_file}"
        self.call += call_str.split()
        # call = call_str.split()lip.mp4 -lavfi showspectrumpic=s=675x30:legend=False -update 1 -frames:v 1 spectrogram.png"
        completed_process = subprocess.run(self.call, check=True)
        if completed_process.returncode == 0:
            print("Spectrogram created.")
        else:
            print("Error creating spectrogram.")

def main():
    import VideoWave as vw
    wave_clip = vw.Waver("clip.mp4")
    wave_clip.export("my_new_video.mp4", size=(640, 480))

def test_ffmpeg():
    """Test ffmpeg call to create a spectrogram from a video clip
    """
    # call_str = "ffmpeg -i clip.mp4 -lavfi showspectrumpic=s=675x30:legend=False -update 1 -frames:v 1 spectrogram.png"
    # call = call_str.split()
    input_file = "clip.mp4"
    ffmpeg = FFMPEG(input_file)
    ffmpeg.get_metadata()

if __name__ == "__main__":
    test_ffmpeg()
