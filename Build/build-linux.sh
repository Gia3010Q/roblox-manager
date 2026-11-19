#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$project_root"
python3 Build/restore-linux.py
dotnet msbuild "RBX Alt Manager/RBX Alt Manager.csproj" /t:Rebuild \
  /p:Configuration=Release /p:Platform=AnyCPU /p:BuildOnLinux=true \
  /p:AutomaticallyUseReferenceAssemblyPackages=false \
  "/p:TargetFrameworkRootPath=$project_root/packages/Microsoft.NETFramework.ReferenceAssemblies.net472.1.0.3/build/" \
  /v:minimal
