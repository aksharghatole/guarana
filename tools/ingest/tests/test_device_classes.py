#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for tools/ingest/device_classes.py: a report's GPU family is the one the engine would give
its GPU. No network.

  python -I tools/ingest/tests/test_device_classes.py
"""

import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # -I leaves the script's directory off sys.path.

import device_classes as dc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def family(name, **kwargs):
    found = dc.classify(bench_gpus=[name], **kwargs)
    return found["family"] if found["status"] == "family" else found["status"]


class EngineTableTests(unittest.TestCase):
    """The Python copy must say what src/common/device_profile.cpp says."""

    def test_family_rows_match_the_engine(self):
        source = read("src", "common", "device_profile.cpp")
        block = source[source.index("constexpr std::array FamilyRows{"):]
        block = block[:block.index("};")]
        vendors = {"VendorIntel": dc.INTEL, "VendorAmd": dc.AMD}
        rows = tuple((vendors[vendor], int(device, 16), part or "", name) for vendor, device, part, name in re.findall(
            r'FamilyRow\{(Vendor\w+), 0x([0-9A-Fa-f]+), (?:\{\}|"([^"]*)"), GpuFamily::(\w+)\}', block))
        self.assertGreater(len(rows), 10)
        self.assertEqual(rows, dc.FAMILY_ROWS)

    def test_families_match_the_engine_enum_and_names(self):
        header = read("src", "common", "device_profile.h")
        body = header[header.index("enum class GpuFamily"):]
        body = body[body.index("{") + 1:body.index("};")]
        names = [name for name in re.findall(r"^\s*(\w+),", body, re.M) if name not in ("None", "Count")]
        self.assertEqual(names, list(dc.FAMILIES))
        source = read("src", "common", "device_profile.cpp")
        returned = dict(re.findall(r'case GpuFamily::(\w+):\s*return "(\w+)";', source))
        self.assertEqual(returned, {name: name for name in names})

    def test_every_family_has_a_label_and_rows(self):
        for name, text in dc.FAMILIES.items():
            self.assertTrue(text)
            self.assertIn(name, {row[3] for row in dc.FAMILY_ROWS})


class NameTests(unittest.TestCase):
    def test_known_names_map_to_their_family(self):
        cases = [
            ("Intel(R) Arc(TM) 140T GPU (16GB)", "IntelArrowLakeH"),
            ("Intel(R) Arc(TM) 130T GPU (16GB)", "IntelArrowLakeH"),
            ("Intel Arc 140T GPU", "IntelArrowLakeH"),
            ("Intel(R) Arc(TM) 140V GPU (16GB)", "IntelArcLunarLake"),
            ("Intel(R) Arc(TM) 130V GPU (8GB)", "IntelArcLunarLake"),
            ("Intel(R) Arc(TM) B390 GPU", "IntelArcB390"),
            ("Intel(R) Arc(TM) Pro B370 GPU", "IntelArcB370"),
            ("AMD Radeon 780M Graphics", "AmdRadeon780M"),
            ("AMD Radeon(TM) 880M", "AmdRadeon880M"),
            ("AMD Radeon(TM) 890M Graphics", "AmdRadeon890M"),
            ("AMD Radeon(TM) 8060S Graphics", "AmdRadeon8060S"),
            ("AMD Custom GPU 0405", "AmdCustomGpu0405"),
            ("AMD Custom GPU 0932 (RADV VANGOGH)", "AmdCustomGpu0932"),
            ("Advanced Micro Devices, Inc. [AMD/ATI] VanGogh [AMD Custom GPU 0405]", "AmdCustomGpu0405"),
        ]
        for name, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(family(name), expected)

    def test_names_outside_every_family_are_none(self):
        for name in ("NVIDIA GeForce RTX 4060 Laptop GPU", "Intel(R) Iris(R) Xe Graphics", "Intel(R) UHD Graphics 620",
                     "Intel(R) HD Graphics 520", "AMD Radeon 760M Graphics", "AMD Radeon(TM) 740M",
                     "AMD Radeon(TM) Graphics", "AMD Radeon RX 7600", "Intel(R) Arc(TM) A770 Graphics",
                     "Intel(R) Arc(TM) A370M Graphics", "Intel(R) Arc(TM) B580 Graphics",
                     "Microsoft Basic Render Driver", "llvmpipe (LLVM 19.1.7, 256 bits)"):
            with self.subTest(name=name):
                self.assertEqual(family(name), "none")

    def test_a_generic_intel_name_is_unresolved_with_the_families_matched_by_id_alone(self):
        for name in ("Intel(R) Arc(TM) Graphics", "Intel(R) Graphics"):
            with self.subTest(name=name):
                found = dc.classify(bench_gpus=[name])
                self.assertEqual((found["status"], found["family"]), ("unresolved", None))
                self.assertEqual(found["candidates"], ["IntelArcMeteorLake", "IntelArrowLakeH", "IntelArcLunarLake",
                                                       "IntelGraphicsPantherLake", "IntelArcB370", "IntelArcB390"])
        # The form's answer narrows the candidates; it never decides.
        found = dc.classify("Intel Arc (Meteor Lake)", "intel", "integrated", ["Intel(R) Arc(TM) Graphics"])
        self.assertEqual((found["status"], found["candidates"]), ("unresolved", ["IntelArcMeteorLake"]))

    def test_names_are_kept_short_and_without_trademark_signs(self):
        found = dc.classify(bench_gpus=["Intel(R) Arc(TM) 140T GPU (16GB)"])
        self.assertEqual((found["name"], found["from"]), ("Intel Arc 140T GPU", dc.FROM_BENCH))


class PciTests(unittest.TestCase):
    def test_a_pci_id_takes_the_engines_table_name_part_included(self):
        cases = [
            ((dc.INTEL, 0x7D51), "Intel(R) Graphics", ("family", "IntelArrowLakeH")),
            ((dc.INTEL, 0x7DD1), "Intel(R) Arc(TM) 140T GPU", ("family", "IntelArrowLakeH")),
            ((dc.INTEL, 0x7DD1), "Intel(R) Graphics", ("none", None)),
            ((dc.INTEL, 0x7D55), "Intel(R) Graphics", ("family", "IntelArcMeteorLake")),
            ((dc.INTEL, 0x7D45), "Intel(R) Graphics", ("none", None)),
            ((dc.AMD, 0x15BF), "AMD Radeon 780M Graphics", ("family", "AmdRadeon780M")),
            ((dc.AMD, 0x15BF), "AMD Radeon(TM) Graphics", ("none", None)),
            ((dc.AMD, 0x150E), "AMD Radeon 890M Graphics", ("family", "AmdRadeon890M")),
            ((dc.AMD, 0x163F), "anything", ("family", "AmdCustomGpu0405")),
            ((0x10DE, 0x28E0), "NVIDIA GeForce RTX 4060 Laptop GPU", ("none", None)),
        ]
        for pci, name, expected in cases:
            with self.subTest(pci=pci, name=name):
                found = dc.classify(report_gpu=name, report_pci=pci)
                self.assertEqual((found["status"], found["family"]), expected)
                self.assertEqual(found["from"], dc.FROM_PCI)

    def test_an_id_whose_family_needs_a_name_without_one_is_unresolved(self):
        found = dc.classify(report_pci=(dc.AMD, 0x150E))
        self.assertEqual((found["status"], found["candidates"]), ("unresolved", ["AmdRadeon880M", "AmdRadeon890M"]))

    def test_pci_id_text(self):
        self.assertEqual(dc.parse_pci(r"PCI\VEN_8086&DEV_7D51&SUBSYS_3D9017AA&REV_08"), (0x8086, 0x7D51))
        self.assertEqual(dc.parse_pci("[8086:7d51]"), (0x8086, 0x7D51))
        self.assertEqual(dc.parse_pci("1002:15BF"), (0x1002, 0x15BF))
        self.assertIsNone(dc.parse_pci("at 12:30, 2880x1800"))
        self.assertIsNone(dc.parse_pci("10de:28e0:extra"))


class LauncherLineTests(unittest.TestCase):
    NOTES = ("Filled in by the Guarana launcher's \"Share my numbers\" from the last session's log; nothing was sent "
             "automatically. GPU: Intel(R) Arc(TM) 140T GPU (16GB). Display 2880x1800 at 120 Hz. Shown-frame "
             "intervals: median 16.7 ms.")

    def test_the_launchers_gpu_line(self):
        self.assertEqual(dc.report_gpu_line(self.NOTES), ("Intel(R) Arc(TM) 140T GPU (16GB)", None))
        with_id = self.NOTES.replace("(16GB).", "(16GB) [8086:7D51].")
        self.assertEqual(dc.report_gpu_line(with_id), ("Intel(R) Arc(TM) 140T GPU (16GB)", (0x8086, 0x7D51)))
        self.assertEqual(dc.report_gpu_line("GPU: AMD Radeon 780M Graphics"), ("AMD Radeon 780M Graphics", None))

    def test_lines_that_name_no_gpu(self):
        self.assertIsNone(dc.report_gpu_line("GPU: 68 °C after ten minutes. iGPU: shared memory 16 GB."))
        self.assertIsNone(dc.report_gpu_line("Nothing else running."))
        self.assertIsNone(dc.report_gpu_line(""))


class FormAnswerTests(unittest.TestCase):
    def test_the_answer_alone_gives_candidates_never_a_family(self):
        cases = [
            ("Intel Arc 140T / 140V", "intel", "integrated", ["IntelArrowLakeH", "IntelArcLunarLake"]),
            ("Intel Arc 130T / 130V", "intel", "integrated", ["IntelArrowLakeH", "IntelArcLunarLake"]),
            ("Intel Arc (Meteor Lake)", "intel", "integrated", ["IntelArcMeteorLake"]),
            ("Intel Arc (Panther Lake)", "intel", "integrated", ["IntelGraphicsPantherLake", "IntelArcB370",
                                                                 "IntelArcB390"]),
            ("AMD Radeon 780M / 760M", "amd", "integrated", ["AmdRadeon780M"]),
            ("AMD Radeon 880M / 890M", "amd", "integrated", ["AmdRadeon880M", "AmdRadeon890M"]),
            ("Steam Deck", "amd", "integrated", ["AmdCustomGpu0405", "AmdCustomGpu0932"]),
            ("AMD Ryzen Z1 / Z2", "amd", "integrated", []),
            ("Other", "other", "unknown", []),
        ]
        for option, vendor, kind, candidates in cases:
            with self.subTest(option=option):
                found = dc.classify(option, vendor, kind)
                self.assertEqual((found["status"], found["family"], found["candidates"], found["from"]),
                                 ("unresolved", None, candidates, dc.FROM_ANSWER))

    def test_discrete_cards_and_old_intel_graphics_are_in_no_family(self):
        for option, vendor, kind in (("NVIDIA RTX 40 series", "nvidia", "discrete"),
                                     ("Intel Arc A / B series", "intel", "discrete"),
                                     ("AMD RX 7000 series", "amd", "discrete"),
                                     ("Intel Iris Xe / UHD", "intel", "integrated")):
            with self.subTest(option=option):
                self.assertEqual(dc.classify(option, vendor, kind)["status"], "none")
        # The emulator ran on the discrete card the answer names, whatever else the machine has.
        found = dc.classify("NVIDIA RTX 40 series", "nvidia", "discrete", ["Intel(R) Arc(TM) 140T GPU (16GB)"])
        self.assertEqual(found["status"], "none")

    def test_the_answers_vendor_picks_among_the_machines_gpus(self):
        gpus = ["NVIDIA GeForce RTX 4060 Laptop GPU", "Intel(R) Arc(TM) 140T GPU (16GB)"]
        self.assertEqual(family(gpus[1], option="Intel Arc 140T / 140V", vendor="intel", kind="integrated"),
                         "IntelArrowLakeH")
        found = dc.classify("Intel Arc 140T / 140V", "intel", "integrated", gpus)
        self.assertEqual((found["status"], found["family"]), ("family", "IntelArrowLakeH"))
        # An integrated answer and two GPUs of one vendor: the integrated one ran.
        found = dc.classify("Intel Arc 140T / 140V", "intel", "integrated",
                            ["Intel(R) Arc(TM) A370M Graphics", "Intel(R) Arc(TM) 140T GPU (16GB)"])
        self.assertEqual(found["family"], "IntelArrowLakeH")
        # Without an answer that says which GPU ran, two that disagree leave it open.
        found = dc.classify("Other", "other", "unknown", gpus)
        self.assertEqual((found["status"], found["candidates"]), ("unresolved", ["IntelArrowLakeH"]))

    def test_a_name_beats_the_answer_and_names_that_disagree_leave_it_open(self):
        found = dc.classify("Intel Arc 140T / 140V", "intel", "integrated", report_gpu="Intel(R) Arc(TM) 140V GPU (16GB)")
        self.assertEqual((found["family"], found["from"]), ("IntelArcLunarLake", dc.FROM_REPORT))
        found = dc.classify("Intel Arc 140T / 140V", "intel", "integrated", ["Intel(R) Arc(TM) 140T GPU (16GB)"],
                            report_gpu="Intel(R) Arc(TM) 140V GPU (16GB)")
        self.assertEqual((found["status"], found["candidates"]), ("unresolved", ["IntelArrowLakeH", "IntelArcLunarLake"]))


if __name__ == "__main__":
    unittest.main()
