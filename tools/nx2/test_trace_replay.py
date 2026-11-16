#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright 2026 Eden Emulator Project
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests trace_replay.py's PNG reader, frame comparison and paired bench."""

import math
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trace_replay  # noqa: E402


def chunk(kind, body):
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))


def write_png(path, width, height, pixels, filters):
    """RGBA PNG whose rows use the given filter types (1-4 encoded properly, 0 raw)."""
    stride = width * 4
    raw = b""
    previous = bytes(stride)
    for y in range(height):
        line = pixels[y * stride:(y + 1) * stride]
        kind = filters[y % len(filters)]
        encoded = bytearray(stride)
        for i in range(stride):
            left = line[i - 4] if i >= 4 else 0
            up = previous[i]
            corner = previous[i - 4] if i >= 4 else 0
            if kind == 0:
                predictor = 0
            elif kind == 1:
                predictor = left
            elif kind == 2:
                predictor = up
            elif kind == 3:
                predictor = (left + up) >> 1
            else:
                p = left + up - corner
                pa, pb, pc = abs(p - left), abs(p - up), abs(p - corner)
                predictor = left if pa <= pb and pa <= pc else up if pb <= pc else corner
            encoded[i] = (line[i] - predictor) & 0xFF
        raw += bytes([kind]) + bytes(encoded)
        previous = line
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) +
                           chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


class TraceReplayTest(unittest.TestCase):
    def test_png_filters_round_trip(self):
        width, height = 7, 5
        pixels = bytes((x * 37 + y * 11 + c * 5) & 0xFF
                       for y in range(height) for x in range(width) for c in range(4))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "frame.png"
            write_png(path, width, height, pixels, [0, 1, 2, 3, 4])
            self.assertEqual(trace_replay.read_png(path), (width, height, pixels))

    def test_difference(self):
        a = (2, 1, bytes([0, 0, 0, 255, 10, 10, 10, 255]))
        self.assertEqual(trace_replay.difference(a, a)["psnr"], math.inf)
        b = (2, 1, bytes([0, 0, 0, 255, 10, 10, 14, 255]))
        result = trace_replay.difference(a, b)
        self.assertEqual(result["max"], 4)
        self.assertAlmostEqual(result["mean"], 0.5)
        self.assertTrue(trace_replay.difference(a, (1, 1, bytes(4)))["size_differs"])

    def test_device_class(self):
        self.assertEqual(trace_replay.device_class("llvmpipe"), "lavapipe")
        self.assertEqual(trace_replay.device_class("NVIDIA GeForce RTX 4090"), "nvidia")

    def test_compare_runs_marks_differing_frames(self):
        with tempfile.TemporaryDirectory() as directory:
            base, head = Path(directory) / "base", Path(directory) / "head"
            base.mkdir()
            head.mkdir()
            write_png(base / "frame-0000.png", 1, 1, bytes([1, 2, 3, 255]), [0])
            write_png(head / "frame-0000.png", 1, 1, bytes([1, 2, 9, 255]), [0])
            frames = {"frames": [{"index": 0, "file": "frame-0000.png", "hash": "a"}]}
            changed = {"frames": [{"index": 0, "file": "frame-0000.png", "hash": "b"}]}
            rows = trace_replay.compare_runs(base, frames, head, changed)
            self.assertFalse(rows[0]["equal"])
            self.assertEqual(rows[0]["difference"]["max"], 6)
            self.assertTrue(trace_replay.compare_runs(base, frames, base, frames)[0]["equal"])


def frames(hashes, times, key="replay_ms"):
    return {"renderer": "Test GPU", "program_id": "0000000000000001",
            "frames": [{"index": index, "hash": value, "ms": time + 5.0, key: time}
                       for index, (value, time) in enumerate(zip(hashes, times))]}


class BenchTest(unittest.TestCase):
    def test_parse_variant(self):
        self.assertEqual(trace_replay.parse_variant("base"), ("base", {}))
        self.assertEqual(trace_replay.parse_variant("gm0=EDEN_NX2_GM=0,EDEN_NX2_SPLIT=2"),
                         ("gm0", {"EDEN_NX2_GM": "0", "EDEN_NX2_SPLIT": "2"}))
        for bad in ("=EDEN_NX2_GM=0", "gm0=EDEN_NX2_GM"):
            with self.assertRaises(ValueError, msg=bad):
                trace_replay.parse_variant(bad)

    def test_percentile(self):
        self.assertIsNone(trace_replay.percentile([], 0.5))
        self.assertEqual(trace_replay.percentile([4.0], 0.95), 4.0)
        self.assertEqual(trace_replay.percentile([1.0, 3.0, 2.0], 0.5), 2.0)
        self.assertAlmostEqual(trace_replay.percentile([1.0, 2.0, 3.0, 4.0], 0.5), 2.5)

    def test_variants_run_in_turn_and_are_compared_with_the_baseline(self):
        order = []

        def run(cli, trace, out, extra, switches):
            order.append((Path(out).parent.name, Path(out).name, cli, tuple(extra)))
            fast = switches.get("EDEN_NX2_GM") == "11"
            changed = switches.get("EDEN_NX2_BROKEN") == "1"
            hashes = ["a", "b", "x" if changed else "c", "d"]
            return frames(hashes, [50.0, 8.0 if fast else 10.0, 8.0 if fast else 10.0,
                                   8.0 if fast else 10.0])

        variants = [{"name": "base", "cli": "cli-a", "switches": {}},
                    {"name": "gm", "cli": "cli-a", "switches": {"EDEN_NX2_GM": "11"}},
                    {"name": "broken", "cli": "cli-b", "switches": {"EDEN_NX2_BROKEN": "1"}}]
        with tempfile.TemporaryDirectory() as directory:
            report = trace_replay.bench(variants, "scene.lxtrace", directory, repeat=2, skip=1,
                                        extra=["--no-images"], run=run)
        self.assertEqual([entry[:2] for entry in order],
                         [("base", "run-1"), ("gm", "run-1"), ("broken", "run-1"),
                          ("base", "run-2"), ("gm", "run-2"), ("broken", "run-2")])
        self.assertEqual(order[2][2:], ("cli-b", ("--no-images",)))
        self.assertEqual(report["timing"], "replay_ms")
        base, gm, broken = report["variants"]
        self.assertEqual((base["median_ms"], gm["median_ms"]), (10.0, 8.0))
        self.assertAlmostEqual(gm["change_percent"], -20.0)
        self.assertTrue(gm["identical_to_baseline"])
        self.assertFalse(broken["identical_to_baseline"])
        self.assertEqual(broken["differing_frames"], [2])
        self.assertNotIn("change_percent", base)
        table = trace_replay.bench_table(report)
        self.assertIn("identical", table[3])
        self.assertIn("1 frames differ", table[4])

    def test_a_variant_whose_runs_differ_is_not_identical(self):
        calls = []

        def run(cli, trace, out, extra, switches):
            calls.append(out)
            return frames(["a", "b" if len(calls) < 2 else "z"], [9.0, 9.0])

        with tempfile.TemporaryDirectory() as directory:
            report = trace_replay.bench([{"name": "base", "cli": "cli", "switches": {}}],
                                        "scene.lxtrace", directory, repeat=2, skip=0, run=run)
        self.assertFalse(report["variants"][0]["repeats_itself"])
        self.assertFalse(report["variants"][0]["identical_to_baseline"])
        self.assertIn("its own runs differ", trace_replay.bench_table(report)[2])

    def test_a_replay_without_frames_is_not_identical(self):
        def run(cli, trace, out, extra, switches):
            return frames([], [])

        with tempfile.TemporaryDirectory() as directory:
            report = trace_replay.bench([{"name": "base", "cli": "cli", "switches": {}},
                                         {"name": "other", "cli": "cli", "switches": {}}],
                                        "scene.lxtrace", directory, repeat=1, skip=0, run=run)
        self.assertFalse(report["variants"][0]["identical_to_baseline"])
        self.assertFalse(report["variants"][1]["identical_to_baseline"])
        self.assertIn("no frames", trace_replay.bench_table(report)[3])

    def test_older_builds_are_timed_by_ms(self):
        def run(cli, trace, out, extra, switches):
            return frames(["a", "b"], [9.0, 9.0], key="replay_ms" if cli == "new" else "other")

        with tempfile.TemporaryDirectory() as directory:
            report = trace_replay.bench([{"name": "base", "cli": "old", "switches": {}},
                                         {"name": "head", "cli": "new", "switches": {}}],
                                        "scene.lxtrace", directory, repeat=1, skip=0, run=run)
        self.assertEqual(report["timing"], "ms")
        self.assertEqual(report["variants"][1]["median_ms"], 14.0)

    def test_frames_without_images_compare_by_hash(self):
        base = {"frames": [{"index": 0, "hash": "a"}]}
        head = {"frames": [{"index": 0, "hash": "b"}]}
        rows = trace_replay.compare_runs("base", base, "head", head)
        self.assertFalse(rows[0]["equal"])
        self.assertNotIn("difference", rows[0])


if __name__ == "__main__":
    unittest.main()
