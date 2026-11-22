// SPDX-FileCopyrightText: Copyright 2026 Eden Emulator Project
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include <array>
#include <atomic>
#include <cstdlib>
#include "common/common_types.h"
#include "core/hardware_properties.h"

// EDEN_NX2_SVC_FASTPATH=1: after a supervisor call that leaves its thread runnable with no
// interrupt pending, PhysicalCore::RunThread continues the JIT loop in place instead of
// returning to the scheduler round trip (off by default). The outer guest-thread loop
// (CpuManager::MultiCoreRunGuestThread) re-enters RunThread with the same thread under exactly
// these conditions, so continuing skips only the round trip. A SVC that blocks or yields to
// another thread has already switched fibers inside Svc::Call; one that terminates, suspends
// or migrates leaves the thread non-runnable or the core interrupted, and still returns to
// the scheduler. Single-core is excluded: its loop must advance CoreTiming after every return.
namespace Kernel::Nx2SvcFastpath {

[[nodiscard]] inline bool ParseEnabled(const char* value) {
    return value != nullptr && std::strtoul(value, nullptr, 10) != 0;
}

[[nodiscard]] inline bool Enabled() {
    static const bool enabled = ParseEnabled(std::getenv("EDEN_NX2_SVC_FASTPATH"));
    return enabled;
}

/// The continue decision, as a pure function so the unit tests can hold the whole truth table.
[[nodiscard]] inline bool ContinueAfterSvc(bool enabled, bool single_core, bool interrupted,
                                           bool runnable) {
    return enabled && !single_core && !interrupted && runnable;
}

/// In-place continues per core, so a GUEST_THREAD_STATS window can prove the switch fired.
inline std::array<std::atomic<u64>, Core::Hardware::NUM_CPU_CORES> g_continues{};

} // namespace Kernel::Nx2SvcFastpath