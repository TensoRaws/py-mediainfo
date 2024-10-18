# py-mediainfo

[![codecov](https://codecov.io/gh/TensoRaws/py-mediainfo/graph/badge.svg?token=b8S3S9br5B)](https://codecov.io/gh/TensoRaws/py-mediainfo)
[![CI-test](https://github.com/TensoRaws/py-mediainfo/actions/workflows/CI-test.yml/badge.svg)](https://github.com/TensoRaws/py-mediainfo/actions/workflows/CI-test.yml)
[![Release-pypi](https://github.com/TensoRaws/py-mediainfo/actions/workflows/Release-pypi.yml/badge.svg)](https://github.com/TensoRaws/py-mediainfo/actions/workflows/Release-pypi.yml)
[![PyPI version](https://badge.fury.io/py/py-mediainfo.svg)](https://badge.fury.io/py/py-mediainfo)

### a modern fork from https://github.com/sbraz/pymediainfo

```
This small package is a wrapper around the MediaInfo library.

It works on Linux, Mac OS (arm64/x64) and Windows (x64) and is tested with Python 3.8 to 3.13 and PyPy3.

See https://pymediainfo.readthedocs.io/ for more information.
```

### Requirements

```
pip install py-mediainfo
```

On Linux, you will need to install the MediaInfo library. On Debian-based systems, you can do this with:

```
apt install libmediainfo-dev -y
```

This is a simple wrapper around the MediaInfo library, which you can find at https://mediaarea.net/en/MediaInfo.

Note:

- Without the library, this package cannot parse media files, which severely limits its functionality.

- Binary wheels containing a bundled library version are provided for Windows and Mac OS X.

- Packages are available for several major Linux distributions. They depend on the library most of the time and are the preferred way to use pymediainfo on Linux unless a specific version of the package is required.

### Using MediaInfo

There isn’t much to this library so instead of a lot of documentation it is probably best to just demonstrate how it works:

Getting information from an image:

```python
from pymediainfo import MediaInfo

media_info = MediaInfo.parse("/home/user/image.jpg")
# Tracks can be accessed via the 'tracks' attribute or through shortcuts
# such as 'image_tracks', 'audio_tracks', 'video_tracks', etc.
general_track = media_info.general_tracks[0]
image_track = media_info.image_tracks[0]
print(
    f"{image_track.format} of {image_track.width}×{image_track.height} pixels"
    f" and {general_track.file_size} bytes."
)
```

Will return something like:

```
JPEG of 828×828 pixels and 19098 bytes.
```

Getting information from a video

```python
from pprint import pprint
from pymediainfo import MediaInfo

media_info = MediaInfo.parse("my_video_file.mp4")
for track in media_info.tracks:
    if track.track_type == "Video":
        print("Bit rate: {t.bit_rate}, Frame rate: {t.frame_rate}, "
              "Format: {t.format}".format(t=track)
        )
        print("Duration (raw value):", track.duration)
        print("Duration (other values:")
        pprint(track.other_duration)
    elif track.track_type == "Audio":
        print("Track data:")
        pprint(track.to_data())
```

Will return something like:

```
Bit rate: 3117597, Frame rate: 23.976, Format: AVC
Duration (raw value): 958
Duration (other values):
['958 ms',
 '958 ms',
 '958 ms',
 '00:00:00.958',
 '00:00:00;23',
 '00:00:00.958 (00:00:00;23)']
Track data:
{'bit_rate': 236392,
 'bit_rate_mode': 'VBR',
 'channel_layout': 'L R',
 'channel_positions': 'Front: L R',
 'channel_s': 2,
 'codec_id': 'mp4a-40-2',
 'commercial_name': 'AAC',
 'compression_mode': 'Lossy',
 …
}
```

### Dumping objects

In order to make debugging easier, `pymediainfo.MediaInfo` and `pymediainfo.Track` objects can be converted to _dict_ using `pymediainfo.MediaInfo.to_data()` and `pymediainfo.Track.to_data()` respectively. The previous example demonstrates that.

### Parsing existing MediaInfo output

If you already have the XML data in a string in memory (e.g. you have previously parsed the file or were sent the dump from `mediainfo --output=OLDXML` by someone else), you can call the constructor directly:

```python
from pymediainfo import MediaInfo
media_info = MediaInfo(raw_xml_string)
```

### Accessing Track attributes

Since the attributes on the `pymediainfo.Track` objects are being dynamically added as the XML output from MediaInfo is being parsed, there isn’t a firm definition of what will be available at runtime. In order to make consuming the objects easier so that you can avoid having to use hasattr or try/except blocks, the **getattribute** method has been overriden and will just return None when and if an attribute is referenced but doesn’t exist.

This will enable you to write consuming code like:

```python
from pymediainfo import MediaInfo
media_info = MediaInfo.parse("my_video_file.mp4")
for track in media_info.tracks:
    if track.bit_rate is None:
        print("""{} tracks do not have bit rate
                 associated with them.""".format(track.track_type))
    else:
        print("{}: {}".format(track.track_type, track.bit_rate))
```

Output:

```
General tracks do not have bit rate associated with them.
Video: 46033920
Audio: 1536000
Menu tracks do not have bit rate associated with them.
```
