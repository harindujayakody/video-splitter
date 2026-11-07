# Split Video Pro

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-007808?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![Terminal UI](https://img.shields.io/badge/Terminal%20UI-Rich-8A2BE2)](https://github.com/Textualize/rich)
[![License: MIT](https://img.shields.io/badge/License-MIT-A3BE8C?style=flat)](LICENSE)
![Version](https://img.shields.io/badge/version-1.2.0-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

Split Video Pro is a lightweight terminal utility for splitting long videos into smaller, manageable clips with real-time FFmpeg feedback.

Built for fast workflow, clean control, and a simple command-line experience, it helps you divide a source video by duration or by a fixed number of parts without leaving the terminal.

## Why Use It?

- **Fast Stream-Copy:** Split clips in seconds without quality loss using keyframe-based stream copy (`-c copy`).
- **Re-encode Mode:** Frame-accurate cuts re-encoded to high-compatibility H.264 video and AAC audio.
- **Safety First:** Prevents silent overwriting of existing output files by alerting and prompting upfront.
- **Rich Live Dashboard:** Real-time progress bar, FPS, processing speed, ETA, and total data written.
- **Cross-Platform:** Works seamlessly on Windows, macOS, and Linux.

---

## Features

- Modern terminal interface powered by `rich`
- Auto-scans the `input` folder for supported video files
- Interactive selection when multiple videos are present
- Split by custom clip duration (e.g. `30s`, `5m`, `01:30`) or by total number of parts
- Two splitting engines:
  - **Stream Copy (Fast & Lossless)**: Instantaneous, keyframe-accurate cuts with no transcoding overhead
  - **Re-encode (Slow & Exact)**: Frame-accurate cuts re-encoded to H.264 + AAC MP4
- Overwrite protection before writing clips
- Live FFmpeg stats dashboard (clip index, elapsed time, FPS, bitrate, and ETA)
- Automatic output directory creation per source video
- Windows launcher script (`Split Video Pro.bat`) with automatic dependency checks
- Unit test suite for verification

---

## Requirements

### 1. Python

Python 3.9 or newer is required.

Check your version:
```bash
python --version
```

### 2. FFmpeg & FFprobe (System Requirement)

Both `ffmpeg` and `ffprobe` must be installed and accessible in your system `PATH`.

#### Installation by OS:

- **Windows:**
  - Automated: double-click `Split Video Pro.bat` (uses `winget` if missing)
  - Manual with winget:
    ```powershell
    winget install Gyan.FFmpeg
    ```
  - Manual with Scoop:
    ```powershell
    scoop install ffmpeg
    ```

- **macOS:**
  ```bash
  brew install ffmpeg
  ```

- **Linux (Debian / Ubuntu):**
  ```bash
  sudo apt update && sudo apt install -y ffmpeg
  ```

- **Linux (Fedora):**
  ```bash
  sudo dnf install ffmpeg
  ```

- **Linux (Arch):**
  ```bash
  sudo pacman -S ffmpeg
  ```

Verify the installation:
```bash
ffmpeg -version
ffprobe -version
```

### 3. Python Package

Install the required Python package:

```bash
python -m pip install -r requirements.txt
```

---

## Quick Start

### Windows Launcher

Double-click:
```text
Split Video Pro.bat
```
The launcher will verify Python and pip, install requirements, verify FFmpeg, create `input` and `output` folders, and run the program.

### Manual Terminal Run

```bash
# 1. Place your video in input/
# 2. Run the script:
python split_video_pro.py
```
*(On Linux/macOS use `python3 split_video_pro.py`)*

---

## How to Use

1. Place one or more video files in `input/`.
2. Start the application: `python split_video_pro.py`.
3. Select your source video.
4. Choose split mode:
   - **1 — By clip duration** (e.g., `30`, `45s`, `5m`, `02:00`)
   - **2 — By number of parts** (e.g., `4` parts)
5. Choose processing method:
   - **1 — Stream Copy (Fast & Lossless)**: Best for speed and preservation of original quality.
   - **2 — Re-encode (Slow & Exact)**: Best for frame-perfect cut accuracy or converting to MP4.
6. Review the split plan and confirm.

---

## Running Unit Tests

Run the test suite with:

```bash
python -m unittest test_split_video_pro.py
```

---

## License

[MIT](LICENSE) © 2026 Harindu Jayakody. Free to use, modify, and distribute.
