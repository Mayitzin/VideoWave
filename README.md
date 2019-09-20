# VideoWave

This small application creates a sound wave and superimpose it on each frame of a video.

## Requirements

- [ffmpeg](https://ffmpeg.org/)
- [opencv](https://pypi.org/project/opencv-python/)
- [scipy](https://www.scipy.org/)
- [numpy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

## Usage

```python
import VideoWave as vw
wave_clip = vw.Waver("clip.mp4")
wave_clip.export("new_clip.mp4")
```

And that's it. You have now a clip with audio waves on top of the image.
