import os
import tempfile
import unittest
from pathlib import Path
from split_video_pro import (
    format_seconds,
    format_bytes,
    parse_duration,
    parse_ffmpeg_time,
    build_ffmpeg_cmd,
    safe_output_dir,
)

class TestSplitVideoPro(unittest.TestCase):
    def test_format_seconds(self):
        self.assertEqual(format_seconds(0), "00:00")
        self.assertEqual(format_seconds(45), "00:45")
        self.assertEqual(format_seconds(65), "01:05")
        self.assertEqual(format_seconds(3665), "01:01:05")

    def test_format_bytes(self):
        self.assertEqual(format_bytes(500), "500.00 B")
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1024 * 1024), "1.00 MB")
        self.assertEqual(format_bytes(1024 * 1024 * 1024), "1.00 GB")

    def test_parse_duration(self):
        self.assertEqual(parse_duration("90"), 90.0)
        self.assertEqual(parse_duration("90s"), 90.0)
        self.assertEqual(parse_duration("5m"), 300.0)
        self.assertEqual(parse_duration("1h"), 3600.0)
        self.assertEqual(parse_duration("02:30"), 150.0)
        self.assertEqual(parse_duration("01:02:30"), 3750.0)
        self.assertEqual(parse_duration("500ms"), 0.5)
        self.assertIsNone(parse_duration("invalid"))

    def test_parse_ffmpeg_time(self):
        self.assertEqual(parse_ffmpeg_time("00:01:30.50"), 90.5)
        self.assertEqual(parse_ffmpeg_time("01:00:00.00"), 3600.0)
        self.assertEqual(parse_ffmpeg_time("invalid"), 0.0)

    def test_build_ffmpeg_cmd_stream_copy(self):
        video = Path("input/sample.mp4")
        out = Path("output/sample/sample_part_01.mp4")

        # Stream copy without overwrite
        cmd_no_ow = build_ffmpeg_cmd(video, 0.0, 60.0, out, method="copy", overwrite=False)
        self.assertIn("-c", cmd_no_ow)
        self.assertIn("copy", cmd_no_ow)
        self.assertIn("-n", cmd_no_ow)
        self.assertNotIn("-y", cmd_no_ow)

        # Stream copy with overwrite
        cmd_ow = build_ffmpeg_cmd(video, 0.0, 60.0, out, method="copy", overwrite=True)
        self.assertIn("-y", cmd_ow)
        self.assertNotIn("-n", cmd_ow)

    def test_build_ffmpeg_cmd_reencode(self):
        video = Path("input/sample.mp4")
        out = Path("output/sample/sample_part_01.mp4")

        cmd = build_ffmpeg_cmd(video, 60.0, 30.0, out, method="reencode", overwrite=False)
        self.assertIn("-c:v", cmd)
        self.assertIn("libx264", cmd)
        self.assertIn("-c:a", cmd)
        self.assertIn("aac", cmd)
        self.assertIn("-n", cmd)

    def test_safe_output_dir(self):
        video = Path("input/my_holiday.mov")
        out_dir = safe_output_dir(video)
        self.assertTrue(out_dir.exists())
        self.assertEqual(out_dir.name, "my_holiday")

if __name__ == "__main__":
    unittest.main()
