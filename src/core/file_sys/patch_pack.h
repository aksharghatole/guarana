// SPDX-FileCopyrightText: Copyright 2026 Eden Emulator Project
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include <array>
#include <filesystem>
#include <optional>
#include <span>
#include <string>
#include <string_view>
#include <vector>
#include "common/common_types.h"
#include "core/file_sys/patch_manager.h"

// Built-in patches as data: patch packs, JSON files shipped next to the program
// (dist/patch-packs, docs/patch-packs.md). PatchManager applies and lists their patches as it does
// the built-ins compiled into patch_manager.cpp, after them.
namespace FileSys {

// A run of bytes a pack patch writes over its module.
struct PatchPackRecord {
    size_t offset{}; // From the module's start, as main+0x... in the log
    std::vector<u8> bytes;
    // In the executable padding after the module's text, which must be zero. Otherwise the record
    // writes over the game's code, whose original_size bytes must hash to original_sha256.
    bool cave{};
    std::array<u8, 32> original_sha256{};
    size_t original_size{};
};

struct PatchPackPatch {
    std::string name; // Also its [DisabledAddOns] key: never rename a patch that has shipped
    std::string description;
    BuiltinPatchLevel level{BuiltinPatchLevel::Standard};
    std::string group;
    std::string replaces;
    bool off_by_default{};
    size_t state_offset{};
    size_t state_size{};
    std::vector<PatchPackRecord> records;
};

struct PatchPack {
    std::string source; // The file name, for messages
    u64 title_id{};
    std::string module;
    std::string build_id; // Upper case without trailing zeros, as PatchNSO compares it
    std::vector<PatchPackPatch> patches;
};

// Reads and checks one pack. When anything in it is wrong, returns nothing and adds one line per
// problem to `errors`: "<source>: <field>: <problem>".
[[nodiscard]] std::optional<PatchPack> ParsePatchPack(std::string_view text,
                                                      std::string_view source,
                                                      std::vector<std::string>& errors);

struct PatchPackLoad {
    std::vector<PatchPack> packs;
    std::vector<std::string> errors;
};

// Every *.json file in `directory`, in file name order. A pack with any problem is left out whole.
[[nodiscard]] PatchPackLoad LoadPatchPacks(const std::filesystem::path& directory);

// Where the packs shipped with the program are: patch-packs next to the executable, or in
// Contents/Resources of a macOS bundle. Empty where the executable cannot be found.
[[nodiscard]] std::filesystem::path ShippedPatchPackDirectory();

[[nodiscard]] bool PatchPackSha256(std::span<const u8> data, std::array<u8, 32>& digest);

// Implemented in patch_manager.cpp, which merges the packs with the built-ins compiled in.

// Why a pack PatchManager uses was left out: its own problems, a missing folder, and a patch name
// another built-in of the same title already has. Empty when every pack is in use.
[[nodiscard]] std::vector<std::string> PatchPackErrors();

// For tests: PatchManager uses `packs` instead of the shipped ones, until this is called with
// nothing.
void UsePatchPacksForTesting(std::optional<std::vector<PatchPack>> packs);

} // namespace FileSys
