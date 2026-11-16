// SPDX-FileCopyrightText: Copyright 2025 Eden Emulator Project
// SPDX-License-Identifier: GPL-3.0-or-later

#include "symlink.h"

#ifdef _WIN32
#include <string>
#include <windows.h>
#endif

#include <boost/filesystem.hpp>

namespace fs = std::filesystem;

// The sole purpose of this file is to treat symlinks like symlinks on POSIX,
// or treat them as directory junctions on Windows.
// This is because, for some inexplicable reason, Microsoft has locked symbolic
// links behind a "security policy", whereas directory junctions--functionally identical
// for directories, by the way--are not. Why? I don't know.
// And no, they do NOT provide a standard API for this (at least to my knowledge).
// CreateSymbolicLink, even when EXPLICITLY TOLD to create a junction, still fails
// because of their security policy.
// I don't know what kind of drugs the Windows developers have been on since NT started.

// Microsoft still has not implemented any of this in their std::filesystem implemenation,
// which ALSO means that it DOES NOT FOLLOW ANY DIRECTORY JUNCTIONS... AT ALL.
// Nor does any of their command line utilities or APIs. So you're quite literally
// on your own.

namespace Common::FS {

bool CreateSymlink(fs::path from, fs::path to)
{
    from.make_preferred();
    to.make_preferred();

    std::error_code ec;
    fs::create_directory_symlink(from, to, ec);
#ifdef _WIN32
    if (ec) {
        // mklink is built into cmd. Run it from the system folder and without a window: system()
        // flashed a console in front of the emulator.
        wchar_t system_dir[MAX_PATH]{};
        const UINT length = GetSystemDirectoryW(system_dir, MAX_PATH);
        if (length == 0 || length >= MAX_PATH) {
            return false;
        }
        const std::wstring shell = std::wstring(system_dir, length) + L"\\cmd.exe";
        std::wstring command =
            L"cmd.exe /d /c mklink /J \"" + to.wstring() + L"\" \"" + from.wstring() + L"\"";
        STARTUPINFOW startup{};
        startup.cb = sizeof(startup);
        PROCESS_INFORMATION process{};
        if (!CreateProcessW(shell.c_str(), command.data(), nullptr, nullptr, FALSE,
                            CREATE_NO_WINDOW, nullptr, nullptr, &startup, &process)) {
            return false;
        }
        WaitForSingleObject(process.hProcess, INFINITE);
        DWORD code = 1;
        GetExitCodeProcess(process.hProcess, &code);
        CloseHandle(process.hThread);
        CloseHandle(process.hProcess);
        return code == 0;
    }
#endif

    return !ec;
}

bool IsSymlink(const fs::path &path)
{
    return boost::filesystem::is_symlink(boost::filesystem::path{path});
}

} // namespace Common::FS
