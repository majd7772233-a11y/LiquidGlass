#!/usr/bin/env bash
set -euo pipefail

mkdir -p artifacts
adb logcat -c
adb install -r examples/android-gles/app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n org.liquidglass.reference.debug/org.liquidglass.reference.MainActivity

READY_MARKER="GL_READY tier=L3 renderer=GLES2_APP_OWNED_FBO"
READY=0
for attempt in $(seq 1 35); do
  LOG_OUTPUT="$(adb logcat -d -s LiquidGlassDemo:I || true)"
  if grep -Fq "$READY_MARKER" <<< "$LOG_OUTPUT"; then
    READY=1
    break
  fi
  sleep 2
done

adb logcat -d -s LiquidGlassDemo:I > artifacts/android-gl.log
cat artifacts/android-gl.log

if [[ "$READY" != "1" ]]; then
  echo "Android GL did not reach the GLES2 app-owned framebuffer path." >&2
  exit 1
fi

adb shell uiautomator dump /sdcard/liquid-glass-window.xml >/dev/null
adb pull /sdcard/liquid-glass-window.xml artifacts/android-window.xml

python3 - <<'PY'
import re
import subprocess
import xml.etree.ElementTree as ET

tree = ET.parse("artifacts/android-window.xml")
nodes = list(tree.iter("node"))
target = next((node for node in nodes if node.attrib.get("text") == "Connect lens"), None)
if target is None:
    raise SystemExit("The native Connect lens control was not present in the accessibility tree.")

match = re.fullmatch(r"\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]", target.attrib["bounds"])
if not match:
    raise SystemExit("Could not parse Android accessibility bounds for Connect lens.")

left, top, right, bottom = map(int, match.groups())
subprocess.run(
    ["adb", "shell", "input", "tap", str((left + right) // 2), str((top + bottom) // 2)],
    check=True,
)
PY

sleep 2
adb shell screencap -p /sdcard/liquid-glass-android-l3.png
adb pull /sdcard/liquid-glass-android-l3.png artifacts/android-gles2-l3.png

grep -Fq "$READY_MARKER" artifacts/android-gl.log
test -s artifacts/android-gles2-l3.png
