#!/usr/bin/env python3
"""
Split Video Pro
Author: Harindu Jayakody
Website: https://infiax.com

Modern terminal video splitter with realtime FFmpeg statistics.
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

try:
    from rich import box
    from rich.console import Console, Group
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
    from rich.prompt import Confirm, IntPrompt, Prompt
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("Missing Python dependency: rich")
    print("Install it with: python -m pip install -r requirements.txt")
    sys.exit(1)

APP_NAME = "Split Video Pro"
VERSION = "1.1.0"
AUTHOR = "Harindu Jayakody"
WEBSITE = "Infiax.com"

console = Console()
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4v", ".flv", ".wmv",
    ".ts", ".mts", ".m2ts", ".mpg", ".mpeg",
}


def ensure_folders() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def format_seconds(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    whole = int(seconds)
    hours, rem = divmod(whole, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_bytes(size: float) -> str:
    size = max(0.0, float(size))
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:,.2f} {unit}"
        size /= 1024
    return f"{size:,.2f} TB"


def parse_duration(text: str) -> Optional[float]:
    """Accept 90, 90s, 5m, 1h, 02:30, or 01:02:30."""
    value = text.strip().lower()
    try:
        if value.endswith("ms"):
            return float(value[:-2]) / 1000
        if value.endswith("s"):
            return float(value[:-1])
        if value.endswith("m"):
            return float(value[:-1]) * 60
        if value.endswith("h"):
            return float(value[:-1]) * 3600
        if ":" in value:
            parts = [float(x) for x in value.split(":")]
            if len(parts) == 2:
                return parts[0] * 60 + parts[1]
            if len(parts) == 3:
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            return None
        return float(value)
    except ValueError:
        return None


def parse_ffmpeg_time(value: str) -> float:
    try:
        h, m, s = value.strip().split(":")
        return float(h) * 3600 + float(m) * 60 + float(s)
    except (ValueError, AttributeError):
        return 0.0


def get_media_info(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path),
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, check=True,
        encoding="utf-8", errors="replace",
    )
    data = json.loads(result.stdout)
    fmt = data.get("format", {})
    streams = data.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
    duration = float(fmt.get("duration") or video_stream.get("duration") or 0)
    width = video_stream.get("width")
    height = video_stream.get("height")
    return {
        "duration": duration,
        "size": float(fmt.get("size") or path.stat().st_size),
        "format": fmt.get("format_long_name") or fmt.get("format_name") or "Unknown",
        "video_codec": video_stream.get("codec_name") or "Unknown",
        "audio_codec": audio_stream.get("codec_name") or "None",
        "resolution": f"{width}x{height}" if width and height else "Unknown",
    }


def find_videos() -> list[Path]:
    return sorted(
        [p for p in INPUT_DIR.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS],
        key=lambda p: p.name.lower(),
    )


def select_video(videos: list[Path]) -> Path:
    if len(videos) == 1:
        console.print(f"[green]Selected:[/green] {videos[0].name}")
        return videos[0]

    table = Table(title="Videos in /input", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("#", justify="right", style="bold")
    table.add_column("File")
    table.add_column("Size", justify="right")
    for i, video in enumerate(videos, 1):
        table.add_row(str(i), video.name, format_bytes(video.stat().st_size))
    console.print(table)

    while True:
        choice = IntPrompt.ask("Choose video", default=1)
        if 1 <= choice <= len(videos):
            return videos[choice - 1]
        console.print("[red]Please enter a valid number.[/red]")


def choose_mode() -> str:
    console.print(Panel.fit(
        "[bold]How do you want to split the video?[/bold]\n\n"
        "[cyan]1[/cyan]  By clip duration\n"
        "[cyan]2[/cyan]  By number of parts",
        title="Split Mode", border_style="cyan",
    ))
    choice = Prompt.ask("Choose", choices=["1", "2"], default="1")
    return "duration" if choice == "1" else "parts"


def get_split_plan(total_duration: float, mode: str) -> tuple[float, int]:
    if mode == "duration":
        console.print("\n[dim]Examples: 30, 30s, 5m, 01:30, 00:05:00[/dim]")
        while True:
            raw = Prompt.ask("Clip duration")
            clip_duration = parse_duration(raw)
            if clip_duration is None or clip_duration <= 0:
                console.print("[red]Enter a valid duration greater than 0.[/red]")
                continue
            if clip_duration >= total_duration:
                console.print("[yellow]That duration is equal to or longer than the source video.[/yellow]")
                if Confirm.ask("Create one clip anyway?", default=False):
                    return total_duration, 1
                continue
            return clip_duration, math.ceil(total_duration / clip_duration)

    while True:
        parts = IntPrompt.ask("Number of parts", default=2)
        if parts < 1:
            console.print("[red]Number of parts must be at least 1.[/red]")
            continue
        return total_duration / parts, parts


def safe_output_dir(video: Path) -> Path:
    target = OUTPUT_DIR / video.stem
    target.mkdir(parents=True, exist_ok=True)
    return target


def source_info_panel(video: Path, info: dict) -> Panel:
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_row("File", video.name)
    table.add_row("Duration", format_seconds(info["duration"]))
    table.add_row("Input size", format_bytes(info["size"]))
    table.add_row("Resolution", info["resolution"])
    table.add_row("Video codec", info["video_codec"])
    table.add_row("Audio codec", info["audio_codec"])
    return Panel(table, title="Source Media", border_style="cyan")


def split_video(video: Path, total_duration: float, clip_duration: float, parts: int, output_dir: Path) -> None:
    """Split video while parsing FFmpeg -progress output for realtime stats."""
    stem = video.stem
    digits = max(2, len(str(parts)))
    started_at = time.monotonic()
    completed_output_bytes = 0

    progress = Progress(
        TextColumn("[bold cyan]Overall"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        expand=True,
    )
    overall_task = progress.add_task("overall", total=100.0)

    def build_dashboard(clip_index: int, clip_processed: float, current_duration: float, stats: dict, output_file: Path) -> Group:
        clip_fraction = min(max(clip_processed / current_duration, 0.0), 1.0) if current_duration > 0 else 0.0
        global_fraction = min(((clip_index - 1) + clip_fraction) / max(parts, 1), 1.0)
        progress.update(overall_task, completed=global_fraction * 100)

        elapsed = max(time.monotonic() - started_at, 0.001)
        eta = max((elapsed / global_fraction) - elapsed, 0.0) if global_fraction > 0 else 0.0
        current_size = output_file.stat().st_size if output_file.exists() else 0
        total_written = completed_output_bytes + current_size

        stat_table = Table(box=box.SIMPLE, expand=True, show_header=False)
        stat_table.add_column("Metric", style="bold cyan", ratio=1)
        stat_table.add_column("Value", ratio=2)
        stat_table.add_row("Current clip", f"{clip_index} / {parts}")
        stat_table.add_row("Clip progress", f"{format_seconds(clip_processed)} / {format_seconds(current_duration)}")
        stat_table.add_row("Frame", stats.get("frame", "0"))
        stat_table.add_row("FPS", stats.get("fps", "0"))
        stat_table.add_row("Encoding speed", stats.get("speed", "0x"))
        stat_table.add_row("Bitrate", stats.get("bitrate", "N/A"))
        stat_table.add_row("Written", format_bytes(total_written))
        stat_table.add_row("Elapsed", format_seconds(elapsed))
        stat_table.add_row("ETA", format_seconds(eta))
        stat_table.add_row("Output file", output_file.name)

        header = Panel(
            Text.from_markup(f"[bold cyan]{APP_NAME}[/bold cyan]  [dim]v{VERSION} • Realtime FFmpeg Monitor[/dim]"),
            border_style="cyan",
        )
        return Group(header, progress, Panel(stat_table, title="Realtime Stats", border_style="green"))

    for i in range(parts):
        start = i * clip_duration
        remaining = total_duration - start
        if remaining <= 0.01:
            continue

        current_duration = min(clip_duration, remaining)
        output_file = output_dir / f"{stem}_part_{i + 1:0{digits}d}.mp4"
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-stats_period", "0.5", "-progress", "pipe:1", "-nostats",
            "-ss", f"{start:.6f}", "-i", str(video), "-t", f"{current_duration:.6f}",
            "-map", "0:v:0?", "-map", "0:a:0?", "-map_metadata", "0",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(output_file),
        ]

        stats = {"frame": "0", "fps": "0", "speed": "0x", "bitrate": "N/A"}
        clip_processed = 0.0
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            encoding="utf-8", errors="replace", bufsize=1,
        )

        with Live(
            build_dashboard(i + 1, clip_processed, current_duration, stats, output_file),
            console=console, refresh_per_second=8, transient=True,
        ) as live:
            assert process.stdout is not None
            for raw_line in process.stdout:
                line = raw_line.strip()
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key == "frame":
                    stats["frame"] = value
                elif key == "fps":
                    stats["fps"] = value
                elif key == "speed":
                    stats["speed"] = value
                elif key == "bitrate":
                    stats["bitrate"] = value
                elif key == "out_time":
                    clip_processed = parse_ffmpeg_time(value)
                elif key == "progress" and value == "end":
                    clip_processed = current_duration
                live.update(build_dashboard(i + 1, clip_processed, current_duration, stats, output_file))

        return_code = process.wait()
        stderr_text = process.stderr.read().strip() if process.stderr is not None else ""
        if return_code != 0:
            console.print(Panel(
                f"[bold red]FFmpeg failed while creating:[/bold red]\n{output_file.name}\n\n"
                f"[dim]{stderr_text or 'No additional FFmpeg error text.'}[/dim]",
                title="Processing Error", border_style="red",
            ))
            raise RuntimeError("Video splitting failed.")

        if output_file.exists():
            completed_output_bytes += output_file.stat().st_size

    progress.update(overall_task, completed=100.0)


def show_plan(video: Path, total_duration: float, clip_duration: float, parts: int, output_dir: Path) -> None:
    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 1))
    table.add_column("Item", style="bold cyan")
    table.add_column("Value")
    table.add_row("Source", video.name)
    table.add_row("Video duration", format_seconds(total_duration))
    table.add_row("Parts", str(parts))
    table.add_row("Approx. clip length", format_seconds(clip_duration))
    table.add_row("Output format", "MP4 • H.264 video • AAC audio")
    table.add_row("Output folder", str(output_dir))
    console.print()
    console.print(Panel(table, title="Split Plan", border_style="cyan"))


def main() -> None:
    ensure_folders()
    console.print(Panel.fit(
        f"[bold cyan]{APP_NAME}[/bold cyan]\n"
        f"[dim]Modern terminal video splitter • v{VERSION}[/dim]\n\n"
        f"[bold]Author:[/bold] {AUTHOR}\n[bold]Website:[/bold] {WEBSITE}",
        border_style="cyan",
    ))

    if not check_ffmpeg():
        console.print(Panel(
            "[bold red]FFmpeg / FFprobe not found.[/bold red]\n\n"
            "Windows: double-click [bold]Split Video Pro.bat[/bold] so the launcher can check/install requirements.\n\n"
            "Otherwise install FFmpeg manually and ensure both [bold]ffmpeg[/bold] and [bold]ffprobe[/bold] are available in PATH.",
            title="Missing Requirement", border_style="red",
        ))
        sys.exit(1)

    videos = find_videos()
    if not videos:
        console.print(Panel(
            f"No supported videos were found.\n\nPut one or more video files inside:\n[bold]{INPUT_DIR}[/bold]\n\nThen run Split Video Pro again.",
            title="No Videos Found", border_style="yellow",
        ))
        return

    video = select_video(videos)
    try:
        with console.status("[cyan]Reading media information...[/cyan]"):
            info = get_media_info(video)
    except Exception as exc:
        console.print(f"[red]Could not read video information:[/red] {exc}")
        return

    total_duration = info["duration"]
    if total_duration <= 0:
        console.print("[red]Could not determine the source video duration.[/red]")
        return

    console.print()
    console.print(source_info_panel(video, info))
    mode = choose_mode()
    clip_duration, parts = get_split_plan(total_duration, mode)
    output_dir = safe_output_dir(video)
    show_plan(video, total_duration, clip_duration, parts, output_dir)

    if not Confirm.ask("\nStart splitting?", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        return

    try:
        split_video(video, total_duration, clip_duration, parts, output_dir)
    except RuntimeError as exc:
        console.print(f"[bold red]{exc}[/bold red]")
        sys.exit(1)

    console.print(Panel.fit(
        f"[bold green]Completed successfully![/bold green]\n\nCreated [bold]{parts}[/bold] clip(s)\nSaved to:\n[cyan]{output_dir}[/cyan]",
        title=APP_NAME, border_style="green",
    ))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user.[/yellow]")
        sys.exit(130)
