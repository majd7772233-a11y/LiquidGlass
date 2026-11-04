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
  if grep -Fq "$READY_MARKER" <<< "$LOG_OUTPUT"; then READY=1; break; fi
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
import json
import re
import subprocess
import xml.etree.ElementTree as ET

nodes = list(ET.parse("artifacts/android-window.xml").iter("node"))
def find(predicate, label):
    value = next((item for item in nodes if predicate(item.attrib)), None)
    if value is None:
        raise SystemExit("Missing accessible control: " + label)
    return value
connect = find(lambda a: a.get("content-desc") == "Connect the liquid lens", "Connect the liquid lens")
play = find(lambda a: a.get("content-desc") == "Pause optical preview", "Pause optical preview")
strength = find(lambda a: a.get("content-desc") == "Refraction strength", "Refraction strength")
def bounds(node, label):
    match = re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", node.attrib.get("bounds", ""))
    if not match: raise SystemExit("Invalid accessibility bounds: " + label)
    left, top, right, bottom = map(int, match.groups())
    return {"left":left,"top":top,"right":right,"bottom":bottom,
            "width_px":right-left,"height_px":bottom-top}
density_output = subprocess.check_output(["adb","shell","wm","density"], text=True)
values = re.findall(r"(?:Physical|Override) density:\s*(\d+)", density_output)
if not values: raise SystemExit("Unable to read display density")
dpi = int(values[-1]); scale = dpi / 160.0
items = {"connect":bounds(connect,"connect"),"play":bounds(play,"play"),"strength":bounds(strength,"strength")}
for name in ("connect","play"):
    if items[name]["height_px"] / scale < 48:
        raise SystemExit(name + " action target is below 48dp")
if items["strength"]["height_px"] / scale < 44:
    raise SystemExit("SeekBar target is below 44dp")
with open("artifacts/android-accessibility-report.json","w",encoding="utf-8") as f:
    json.dump({"density_dpi":dpi,"controls":items,"minimum_action_target_dp":48,"minimum_slider_target_dp":44},f,indent=2)
    f.write("\n")
rect = items["connect"]
subprocess.run(["adb","shell","input","tap",str((rect["left"]+rect["right"])//2),str((rect["top"]+rect["bottom"])//2)],check=True)
PY

sleep 2
adb shell screencap -p /sdcard/liquid-glass-android-l3.png
adb pull /sdcard/liquid-glass-android-l3.png artifacts/android-gles2-l3.png

# Medium-density portrait configuration.
adb shell wm size 720x1280
adb shell wm density 320
sleep 3
adb shell screencap -p /sdcard/liquid-glass-android-medium.png
adb pull /sdcard/liquid-glass-android-medium.png artifacts/android-gles2-medium-density.png

# Verify system accessibility preferences are consumed by the app.
adb shell settings put secure high_text_contrast_enabled 1
adb shell settings put global animator_duration_scale 0
adb shell am force-stop org.liquidglass.reference.debug
adb shell am start -n org.liquidglass.reference.debug/org.liquidglass.reference.MainActivity
sleep 3
adb logcat -d -s LiquidGlassDemo:I > artifacts/android-accessibility-settings.log
grep -Fq "GL_ACCESSIBILITY reduced_motion=true high_text_contrast=true" artifacts/android-accessibility-settings.log
adb shell settings put secure high_text_contrast_enabled 0
adb shell settings put global animator_duration_scale 1

# Landscape configuration; use 160 dpi so the 1280x720 logical viewport has room for the vertical controls.
# The Activity no longer pins itself to portrait.
adb shell settings put system accelerometer_rotation 0
adb shell settings put system user_rotation 1
adb shell wm size 1280x720
adb shell wm density 160
sleep 4
adb shell screencap -p /sdcard/liquid-glass-android-landscape.png
adb pull /sdcard/liquid-glass-android-landscape.png artifacts/android-gles2-landscape.png

# Restore defaults, then exercise four independent refractive SDF surfaces in one pass.
adb shell wm size reset
adb shell wm density reset
adb shell settings put system user_rotation 0
sleep 3
adb shell am force-stop org.liquidglass.reference.debug
adb logcat -c
adb shell am start -n org.liquidglass.reference.debug/org.liquidglass.reference.MainActivity --ei extra_surfaces 3
MULTI_READY=0
for attempt in $(seq 1 20); do
  adb logcat -d -s LiquidGlassDemo:I > artifacts/android-gl-multisurface.log
  if grep -Fq "SURFACE_COUNT main=1 additional=3 total=4" artifacts/android-gl-multisurface.log && grep -Fq "$READY_MARKER" artifacts/android-gl-multisurface.log; then MULTI_READY=1; break; fi
  sleep 1
done
if [[ "$MULTI_READY" != "1" ]]; then echo "Four-surface workload did not initialize." >&2; exit 1; fi
adb shell screencap -p /sdcard/liquid-glass-android-four-surfaces.png
adb pull /sdcard/liquid-glass-android-four-surfaces.png artifacts/android-gles2-four-surfaces.png

grep -Fq "$READY_MARKER" artifacts/android-gl.log
test -s artifacts/android-gles2-l3.png
test -s artifacts/android-gles2-medium-density.png
test -s artifacts/android-gles2-landscape.png
test -s artifacts/android-gles2-four-surfaces.png
test -s artifacts/android-accessibility-settings.log
