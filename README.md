# VideoWave

This small application creates a sound wave and superimposes it on each frame of a video.

Check the reasoning behind the curtain in its [original post](https://mariogc.com/post/videowave/).

## Requirements

- [ffmpeg](https://ffmpeg.org/) to handle video encoding/decoding
- [opencv](https://pypi.org/project/opencv-python/) to create the visuals (waves)
- [scipy](https://www.scipy.org/) to get the spectral information of the audio
- [numpy](https://numpy.org/) to handle the data
- [Matplotlib](https://matplotlib.org/) is not really needed, but shows the intermediate data, if you want to know what's happening behind scenes.

## Usage

```python
from VideoWave import Waver
wave_clip = Waver("clip.mp4")
wave_clip.export("new_clip.mp4")
```

And that's it. You have now a new clip with audio waves on top of the image looking like this:

![](videowaved.gif)

## Installation

You can install the latest version of VideoWave directly from the repository using `git` and `pip`:

```
git clone https://github.com/Mayitzin/VideoWave.git
cd VideoWave
pip install .
```
