// SPDX-FileCopyrightText: Copyright 2026 Eden Emulator Project
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include <filesystem>

namespace VideoCommon::GpuTrace {

/// Writes a small synthetic trace that needs no game: one Switch 2 channel whose frames are
/// CPU-written images and 3D engine clears (whole and scissored), each presented.
/// With `presents` false the same stream is written without its presents: what a recording
/// that ends before its first frame leaves, and what a replay refuses.
/// Returns false if the file can't be written.
bool WriteSampleTrace(const std::filesystem::path& path, bool presents = true);

} // namespace VideoCommon::GpuTrace
