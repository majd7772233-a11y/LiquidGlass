#!/usr/bin/env bash
set -euo pipefail

PACKAGE="org.liquidglass.reference.debug"
mkdir -p artifacts

adb shell dumpsys gfxinfo "$PACKAGE" reset >/dev/null 2>&1 || true
adb logcat -c
adb shell am force-stop "$PACKAGE"
adb shell input keyevent KEYCODE_WAKEUP || true
adb shell wm dismiss-keyguard >/dev/null 2>&1 || true
adb shell am start -W -n "$PACKAGE/org.liquidglass.reference.MainActivity" --ei extra_surfaces 3 > artifacts/android-performance-launch.txt
sleep 12

adb logcat -d -s LiquidGlassDemo:I > artifacts/android-performance.log
adb shell dumpsys gfxinfo "$PACKAGE" > artifacts/android-gfxinfo.txt
adb shell dumpsys gfxinfo "$PACKAGE" framestats > artifacts/android-gfxinfo-framestats.txt
adb shell dumpsys meminfo "$PACKAGE" > artifacts/android-meminfo.txt
adb shell dumpsys battery > artifacts/android-battery.txt
adb shell dumpsys thermalservice > artifacts/android-thermal.txt 2>&1 || true
adb shell dumpsys SurfaceFlinger --list > artifacts/android-surface-list.txt 2>&1 || true
adb shell wm size > artifacts/android-display-size.txt
adb shell wm density > artifacts/android-display-density.txt
adb shell settings get global animator_duration_scale > artifacts/android-animator-scale.txt

PID="$(adb shell pidof "$PACKAGE" | tr -d '\r' || true)"
if [[ -n "$PID" ]]; then
  adb shell top -b -n 1 -p "$PID" > artifacts/android-top.txt 2>&1 || true
fi

python3 - <<'PY'
import json
import re
from pathlib import Path

log_path = Path("artifacts/android-performance.log")
log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
perf = re.findall(r"PERF [^\r\n]+", log)
multisurface_path = Path("artifacts/android-gl-multisurface.log")
multisurface_log = multisurface_path.read_text(encoding="utf-8", errors="replace") if multisurface_path.exists() else ""
device = re.findall(r"GL_DEVICE [^\r\n]+", log + "\n" + multisurface_log)
report = {
    "schemaVersion": 1,
    "environment": "Android API 35 x86_64 emulator with SwiftShader",
    "evidenceScope": "Emulator-only diagnostic capture; not physical-device GPU, battery, or thermal validation.",
    "glDevice": device[-1] if device else None,
    "framePacingSamples": perf,
    "memory": "See android-meminfo.txt; renderer log separately estimates the app-owned RGBA FBO texture only.",
    "gpuExecutionTime": "Not measured. cpu_submit_p95_ms is CPU-side GL command submission time, not GPU execution time.",
    "thermalAndBattery": "Raw emulator snapshots are retained for diagnostics only and are not representative device endurance measurements.",
    "rawFiles": [
        "android-gfxinfo.txt", "android-gfxinfo-framestats.txt", "android-meminfo.txt",
        "android-battery.txt", "android-thermal.txt", "android-surface-list.txt",
        "android-display-size.txt", "android-display-density.txt", "android-animator-scale.txt",
        "android-top.txt", "android-performance.log", "android-performance-launch.txt",
        "android-window-performance.xml", "android-multisurface-activities.txt",
        "android-window-multisurface.xml", "android-accessibility-settings.log", "android-gl-multisurface.log"
    ]
}
Path("artifacts/android-performance-summary.json").write_text(
    json.dumps(report, indent=2) + "\n", encoding="utf-8"
)
print("Captured Android frame pacing, CPU submission, memory, display, battery, thermal, and surface diagnostics.")
if not perf:
    raise SystemExit("No PERF sample was emitted during the 12-second profiling window.")
PY
