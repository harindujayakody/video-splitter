# Split Video Pro

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-007808?logo=ffmpeg&logoColor=white)
![Terminal UI](https://img.shields.io/badge/Terminal%20UI-Rich-8A2BE2)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Status](https://img.shields.io/badge/status-active-success)

Split Video Pro is a lightweight terminal utility for splitting long videos into smaller, manageable clips with real-time FFmpeg feedback.

Built for fast workflow, clean control, and a simple command-line experience, it helps you divide a source video by duration or by a fixed number of parts without leaving the terminal.

## Why Use It?

- Split videos into equal or custom-length segments
- Choose a source file from a friendly terminal menu
- Track progress live while FFmpeg encodes each clip
- Output clean MP4 files with H.264 video and AAC audio
- Keep your workflow simple and script-friendly

---

## Features

- Modern terminal interface powered by `rich`
- Auto-scans the `input` folder for supported video files
- Lets you select a video when multiple sources are present
- Split by custom clip duration
- Split by total number of parts
- Live FFmpeg stats dashboard
- Current clip, elapsed time, FPS, bitrate, and ETA
- Automatic output folder generation
- H.264 + AAC MP4 export for broad compatibility
- Windows launcher script support
- Dependency checks for Python and FFmpeg
- Keyboard interrupt handling

---

## Supported Input Formats

The app automatically detects common video extensions such as:

`MP4`, `MKV`, `MOV`, `AVI`, `WEBM`, `M4V`, `FLV`, `WMV`, `TS`, `MTS`, `M2TS`, `MPG`, and `MPEG`.

FFmpeg may support more formats than the list above, but these are the extensions actively scanned by the current script.

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

Each source video gets its own output folder.

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

Python 3.9 or newer is recommended.

Check your version:

```bash
python --version
```

### FFmpeg

Both `ffmpeg` and `ffprobe` must be available in your system `PATH`.

> FFmpeg is an external system dependency, not a Python package: it is **not**
> installed by `pip install -r requirements.txt` (which only installs the
> `rich` terminal UI library). Install it from https://ffmpeg.org/download.html
> or your OS package manager, then re-run the tool.

Verify with:

```bash
ffmpeg -version
ffprobe -version
```

### Python Package

Install the required dependency:

```bash
python -m pip install -r requirements.txt
```

Current package requirement:

```text
rich>=13.7.0,<15.0.0
```

---

## Quick Start

### Windows

Double-click the launcher:

```text
Split Video Pro.bat
```

The launcher can:

1. Detect Python
2. Check `pip`
3. Install requirements if needed
4. Verify FFmpeg and FFprobe
5. Create missing `input` and `output` folders
6. Launch the app

### Manual Start

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python split_video_pro.py
```

On Linux or macOS:

```bash
python3 split_video_pro.py
```

---

## How to Use

1. Place one or more supported videos in the `input` folder.
2. Start the application.
3. Select the desired source video if multiple are available.
4. Choose a split mode:

```text
1  By clip duration
2  By number of parts
```

### Split by Duration

Examples:

```text
30
30s
5m
1h
01:30
00:05:00
```

These values represent:

- `30` = 30 seconds
- `30s` = 30 seconds
- `5m` = 5 minutes
- `1h` = 1 hour
- `01:30` = 1 minute 30 seconds
- `00:05:00` = 5 minutes

### Split by Number of Parts

Enter how many clips you want to generate.

Example:

```text
10
```

The program calculates the appropriate segment length automatically.

---

## Live Terminal Stats

While FFmpeg is processing, Split Video Pro shows a live dashboard with:

| Stat | Description |
|---|---|
| Overall | Total splitting progress |
| Current clip | Current segment number / total |
| Clip progress | Time processed in the current clip |
| Frame | Current encoded frame count |
| FPS | Current processing rate |
| Encoding speed | FFmpeg speed multiplier |
| Bitrate | Output bitrate in use |
| Written | Approximate total output written |
| Elapsed | Total processing time |
| ETA | Estimated remaining time |
| Output file | File currently being generated |

These values are reported directly by FFmpeg and may fluctuate depending on the source and machine speed.

---

## Output Settings

By default clips use **fast stream copy**: the original video and audio
codecs are copied untouched, so splitting takes seconds and quality is
identical to the source. Splits land on keyframes, so cut points may be up
to a few seconds off the requested time.

Choose **Re-encode H.264 CRF 18** at the prompt when you need frame-accurate
cuts or a normalised output codec:

```text
Container : MP4
Video     : H.264 / libx264
Preset    : medium
CRF       : 18
Audio     : AAC
Audio rate: 192 kbps
```

Because clips are re-encoded in that mode, split boundaries are typically more precise than stream-copy splitting.

---

## Output Location

Generated clips are stored in:

```text
/output/<source-video-name>/
```

Example:

```text
/output/my_video/my_video_part_01.mp4
```

Existing files with the same names are **never overwritten silently**: Split Video Pro asks before overwriting each existing clip, and skips it if you decline.

---

## Troubleshooting

### FFmpeg / FFprobe Not Found

Make sure both commands work from a terminal:

```bash
ffmpeg -version
ffprobe -version
```

If Windows installed FFmpeg with `winget`, reopen the terminal after installation so the updated `PATH` is loaded.

### Rich Module Not Found

Run:

```bash
python -m pip install -r requirements.txt
```

### No Videos Found

Place supported videos inside:

```text
input/
```

Then restart the app.

### Processing Failed

Verify that the source file is readable and not corrupted.

---

<footer>
  <p>Created by Harindu Jayakody</p>
  <p>Infiax.com</p>
</footer>

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

---

## License

MIT License — see [LICENSE](LICENSE).
