# Split Video Pro

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-007808?logo=ffmpeg&logoColor=white)
![Terminal UI](https://img.shields.io/badge/Terminal%20UI-Rich-8A2BE2)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Status](https://img.shields.io/badge/status-active-success)
![Website](https://img.shields.io/badge/Website-Infiax.com-black)

**Split Video Pro** is a modern terminal-based video splitting utility built with Python, Rich, FFmpeg, and FFprobe.

It can split a source video using either a custom clip duration or a custom number of equal parts, while displaying realtime FFmpeg processing statistics directly in the terminal.

## Author

**Harindu Jayakody**  
**Infiax.com**

Website: https://infiax.com

---

## Features

- Modern terminal UI powered by `rich`
- Automatically scans the `input` folder
- Lets you select a source video when multiple files are available
- Split by **clip duration**
- Split by **number of parts**
- Realtime FFmpeg progress dashboard
- Overall percentage
- Current clip number
- Current clip processed time
- FFmpeg frame count
- Realtime FPS
- Encoding speed
- Current bitrate
- Total data written
- Total elapsed time
- Estimated remaining time
- Current output filename
- Displays source duration, file size, resolution, and codecs
- Automatically creates output folders
- H.264 video output
- AAC audio output
- MP4 output for broad compatibility
- Windows `.bat` launcher
- Automatic Python dependency installation from `requirements.txt`
- Automatic FFmpeg / FFprobe detection
- Windows launcher can attempt FFmpeg installation through `winget`
- Keyboard interrupt handling
- GitHub-ready project structure

---

## Supported Input Formats

Split Video Pro currently scans for these common video extensions:

`MP4`, `MKV`, `MOV`, `AVI`, `WEBM`, `M4V`, `FLV`, `WMV`, `TS`, `MTS`, `M2TS`, `MPG`, and `MPEG`.

FFmpeg itself may support additional formats, but the extensions above are the formats automatically detected by the current script.

---

## Project Structure

```text
Split-Video-Pro/
├── split_video_pro.py
├── Split Video Pro.bat
├── requirements.txt
├── README.md
├── .gitignore
├── input/
│   └── Put source videos here
└── output/
    └── Generated clips are saved here
```

Each source video gets its own output directory.

Example:

```text
input/
└── holiday.mp4

output/
└── holiday/
    ├── holiday_part_01.mp4
    ├── holiday_part_02.mp4
    └── holiday_part_03.mp4
```

---

## Requirements

### Python

Python **3.9 or newer** is recommended.

Check your Python version:

```bash
python --version
```

### FFmpeg

Both `ffmpeg` and `ffprobe` must be available in your system `PATH`.

Check them with:

```bash
ffmpeg -version
ffprobe -version
```

### Python Package

The current Python dependency is:

```text
rich>=13.7.0,<15.0.0
```

Install dependencies manually with:

```bash
python -m pip install -r requirements.txt
```

---

## Windows Quick Start

The recommended Windows method is the included launcher.

1. Download or clone the project.
2. Put your video files inside the `input` folder.
3. Double-click:

```text
Split Video Pro.bat
```

The launcher automatically performs these checks:

1. Detect Python.
2. Detect `pip`.
3. Attempt to install `pip` if necessary.
4. Install/check Python packages from `requirements.txt`.
5. Detect FFmpeg and FFprobe.
6. If FFmpeg is missing and `winget` is available, attempt to install `Gyan.FFmpeg`.
7. Create `input` and `output` folders if needed.
8. Start `split_video_pro.py`.

If FFmpeg is installed during the first launcher run, Windows may require you to close the terminal and launch `Split Video Pro.bat` again so the updated `PATH` is visible.

---

## Manual Start

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python split_video_pro.py
```

On Linux or macOS you may need:

```bash
python3 split_video_pro.py
```

---

## How To Use

Put one or more videos inside:

```text
/input
```

Start Split Video Pro.

If multiple source videos exist, select the video number from the terminal list.

The application then displays source information such as:

- duration
- file size
- resolution
- video codec
- audio codec

Choose a split mode:

```text
1  By clip duration
2  By number of parts
```

### Split By Duration

Accepted duration examples:

```text
30
30s
5m
1h
01:30
00:05:00
```

Meaning:

- `30` = 30 seconds
- `30s` = 30 seconds
- `5m` = 5 minutes
- `1h` = 1 hour
- `01:30` = 1 minute 30 seconds
- `00:05:00` = 5 minutes

If the source duration is not evenly divisible by the requested duration, the final clip can be shorter.

### Split By Number Of Parts

Enter the total number of clips you want.

Example:

```text
10
```

Split Video Pro calculates the approximate duration of each part automatically.

---

## Realtime Terminal Stats

While FFmpeg is processing, Split Video Pro displays a live terminal dashboard.

| Stat | Description |
|---|---|
| Overall | Total video splitting progress |
| Current clip | Current clip number / total clip count |
| Clip progress | Processed duration inside the current clip |
| Frame | Current encoded frame reported by FFmpeg |
| FPS | Current encoding frames per second |
| Encoding speed | FFmpeg processing speed such as `1.8x` |
| Bitrate | Current FFmpeg output bitrate |
| Written | Approximate total output data written |
| Elapsed | Total wall-clock processing time |
| ETA | Estimated remaining processing time |
| Output file | File currently being created |

Realtime values come from FFmpeg's machine-readable progress output and can fluctuate during encoding.

---

## Output Encoding

The current output settings prioritize compatibility and quality:

```text
Container : MP4
Video     : H.264 / libx264
Preset    : medium
CRF       : 18
Audio     : AAC
Audio rate: 192 kbps
```

Because Split Video Pro re-encodes clips, split boundaries are more accurate than basic stream-copy splitting.

Re-encoding performance depends on factors such as:

- source resolution
- source duration
- CPU performance
- source codec
- number of generated clips

---

## Output Location

Generated clips are written to:

```text
/output/<source-video-name>/
```

Example:

```text
/output/my_video/my_video_part_01.mp4
```

Existing generated files with the same names are overwritten by FFmpeg.

---

## GitHub Installation

Clone your repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Split-Video-Pro
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Put videos in `input/`, then run:

```bash
python split_video_pro.py
```

Windows users can instead double-click:

```text
Split Video Pro.bat
```

---

## Troubleshooting

### FFmpeg / FFprobe Not Found

Make sure both commands work from a terminal:

```bash
ffmpeg -version
ffprobe -version
```

If Windows installed FFmpeg using `winget`, close your current terminal and open a new one so the updated `PATH` can load.

### Rich Module Not Found

Run:

```bash
python -m pip install -r requirements.txt
```

### No Videos Found

Place a supported source video inside:

```text
input/
```

Then restart the program.

### Processing Failed

Verify that the source file is readable and not corrupted.

You can test it with:

```bash
ffprobe "input/your_video.mp4"
```

---

## Notes

- Output clips are encoded as MP4 using H.264 and AAC.
- A source containing no audio can still be processed.
- The program maps the first available video stream and first available audio stream.
- Metadata is copied where FFmpeg can preserve it.
- The final duration-based clip may be shorter than the requested duration.
- Realtime ETA is an estimate and changes as encoding speed changes.
- Large or high-resolution videos can require significant CPU time and disk space.

---

## Contributing

Issues, feature ideas, UI improvements, performance improvements, and pull requests are welcome after the project is published on GitHub.

Possible future improvements:

- stream-copy / fast split mode
- hardware acceleration
- custom output codec selection
- output quality presets
- drag-and-drop support
- batch processing
- subtitle stream handling
- audio-only splitting
- configurable filename templates

---

## Credits

Built with:

- Python
- Rich
- FFmpeg
- FFprobe

Developed by **Harindu Jayakody**  
**Infiax.com**

https://infiax.com
