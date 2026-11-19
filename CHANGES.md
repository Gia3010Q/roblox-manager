# Roblox Manager — changes from the reference

This edition was copied from `~/workspace/ram-analysis` to `~/workspace/ram-parallel`, excluding `.git`. The reference is not modified. The solution/project names, namespaces, account encryption and serialization, data filenames, icons, and existing resources are retained. The changes below separate the two application identities and resolve shared-resource conflicts; no features were removed.

The new identity GUID is `576c62a0-f2cc-409b-8829-6997b5ce0e75`. It replaces every occurrence of the original project GUID in the copied source, including all solution configuration mappings.

## Modified files

| File | Change | Reason |
| --- | --- | --- |
| `RBX Alt Manager/Classes/Program.cs` | Use the new GUID for the application single-instance mutex. Change the message body to `Roblox Manager is already running!`. | The original and Parallel no longer reject each other as duplicate instances. Each edition still has its own single-instance guard in Release builds. |
| `RBX Alt Manager/RBX Alt Manager.csproj` | Use the same new `ProjectGuid`; change `AssemblyName` to `Roblox Manager`. Replace the post-build copy of the old binary launcher with a `BuildParallelLauncher` target that compiles root `Launcher.cs` into the existing `RBX Alt Manager.exe` entry point. | Generate a distinctly named main executable, maintain project identity consistency, and preserve the legacy launcher after the main EXE is renamed. The original binary launcher hardcodes the old main EXE name. |
| `RBX Alt Manager.sln` | Use the new project GUID in the project declaration and all 12 build/configuration mappings. | Keep the solution connected to the renamed-identity project in every existing configuration. The solution filename remains unchanged. |
| `RBX Alt Manager/Properties/AssemblyInfo.cs` | Set `AssemblyTitle` and `AssemblyProduct` to `Roblox Manager`; set the assembly `Guid` to the same new GUID. | Distinguish assembly/product identity. `Application.ProductName` now supplies a separate value name under `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`, so the existing startup feature does not overwrite the original's entry. |
| `RBX Alt Manager/AccountManager.Designer.cs` | Set the main form title to `Roblox Manager`. | Make the two running windows distinguishable. Other UI strings, icons, and resources are unchanged. |
| `RBX Alt Manager/AccountManager.cs` | Default `CheckForUpdates` to `false`; change both the WebServerPort default and fallback from `7963` to `7964`; change the NexusPort default from `5242` to `5243`. | Avoid automatic replacement by upstream releases and separate the HTTP/WebSocket listener ports. These remain defaults: existing INI values are not overwritten. |
| `RBX Alt Manager/AccountManager.cs` | In `UpdateMultiRoblox()`, retain the mutex handle and return success when the nonblocking `WaitOne` returns false because another instance owns `ROBLOX_singletonMutex`. Treat `AbandonedMutexException` as successful acquisition. Keep the original constructor, create-first acquisition behavior, signature, other exception behavior, and close-only disable path. | Allow Parallel to cooperate with the original's Multi Roblox mutex. No `ReleaseMutex` is added; disabling closes only Parallel's own handle, and process exit closes its handles. |
| `RBX Alt Manager/AccountManager.cs` | Rename the two shared temporary basenames to `ram-parallel-vcredist.tmp` and `ram-parallel-manual-install.html`. | Prevent the two editions from writing/executing the same downloaded prerequisite file or overwriting browser installation instructions containing different installation paths. The download/execution behavior and file contents are unchanged. |
| `RAMAccount.lua` | Default the HTTP API port to `7964`. | Route this edition's Lua account API to Parallel instead of the original. |
| `RBX Alt Manager/Nexus/Nexus.lua` | Default the Nexus host to `localhost:5243`. | Route this edition's Nexus client to Parallel's listener. |
| `RBX Alt Manager/Nexus/NexusDocs.md` | Document the default host as `localhost:5243`. | Keep the local Nexus API documentation consistent with the new default. |
| `RBX Alt Manager/Nexus/AccountControl.cs` | When exporting the existing embedded Nexus loader, replace both parameterless `Nexus:Connect()` calls with `Nexus:Connect('localhost:5243')`. The resource itself is unchanged. | The GUI exports a loader that downloads/caches the upstream script. Without this fix, that path would still select upstream's original default port despite the checked-in Lua change. |

## Added files

| File | Purpose |
| --- | --- |
| `Launcher.cs` | Source for the legacy `RBX Alt Manager.exe` launcher. It matches the supplied launcher's decoded behavior: combine the current directory with the main EXE name, start it if present, then exit with code 0. Only the main EXE basename changes to `Roblox Manager.exe`. The supplied root `Launcher` binary remains untouched and is no longer copied by the build. |
| `CHANGES.md` | This file-by-file record, conflict audit notes, and verification limits. |
| `HUONG_DAN.md` | Vietnamese instructions for building, installing, migrating accounts, and running both editions. |

## Coexistence conditions and audit notes

- Keep each edition in its own installation folder **and working directory**. `RAMSettings.ini`, `AccountData.json`, `RecentGames.json`, `RAMTheme.ini`, Nexus state, and other local files retain their original names/formats and are separated by the current directory. A shortcut's **Start in** folder matters.
- Account migration is a copy of `AccountData.json` on the same PC, preferably under the same Windows account. Password-encrypted files still need their existing password. Encryption code, entropy, headers, and formats are unchanged. Do not copy `RAMSettings.ini`: it can restore the original ports and enable upstream update checks.
- Keep **Check for Updates** off in Parallel and do not use **Force Update** or the `-update` argument. The existing updater is intentionally retained and still downloads upstream releases; it also contains original process/shortcut names. It is not a Parallel updater.
- Multi Roblox can be enabled in either edition before Roblox starts; only one edition needs it enabled. Parallel can also attach to a mutex already held by the original. The unmodified original still has its old warning behavior if Parallel owns the mutex first and Multi Roblox is subsequently enabled in the original. If enabling it in both, start/enable the original first, then Parallel.
- The separation is between manager instances and their local files, not separate installations of Roblox. Existing operations on all `RobloxPlayerBeta` processes, shared Roblox client settings, and same-account `AutoCloseLastProcess` behavior remain unchanged. Separate manager folders do not isolate those actions.
- The existing optional Roblox cookie-file lock already skips a file held by another process. Its original check/open race remains; opening the managers one after the other avoids deliberately exercising that startup race. No global browser-profile path or additional fixed application listener port was found in the source audit.
- If either default port is already occupied by another program, choose distinct free ports and update the corresponding Lua clients. The exported Nexus loader explicitly targets the new default `5243`; edit its host if using a custom port.

## Verification

The full recursive diff against the reference was reviewed, including every edited C# hunk in context. Unchanged files and the reference tree were checked by SHA-256. The C# source changes were syntax-parsed, including both preprocessor variants of `Program.cs`, and the project XML was parsed. All original binary/resource files were retained byte for byte.

This Linux environment cannot validate a Windows .NET Framework 4.7.2 build, the new MSBuild launcher target in Visual Studio, Windows mutex/registry/listener behavior, account decryption on the owner's PC, or Roblox integration. No compilation or successful Windows runtime test is claimed. Follow the build and runtime checks in `HUONG_DAN.md` on Windows.

> Rename note (2026-11-19): at the owner's request the edition's product/executable name was set to **Roblox Manager** (EXE `Roblox Manager.exe`, window title `Roblox Manager`). The identity GUID, ports and all coexistence fixes are unchanged.
