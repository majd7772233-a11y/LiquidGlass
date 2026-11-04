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

# Medium-density portrait configuration: restart after wm overrides and prove the app was redrawn.
adb shell wm size 720x1280
adb shell wm density 320
adb shell wm user-rotation lock 0
adb shell am force-stop org.liquidglass.reference.debug
adb logcat -c
adb shell am start -n org.liquidglass.reference.debug/org.liquidglass.reference.MainActivity > artifacts/android-medium-launch.txt
MEDIUM_READY=0
for attempt in $(seq 1 35); do
  adb logcat -d -s LiquidGlassDemo:I > artifacts/android-gl-medium.log
  if grep -Fq "ACTIVITY_RESUMED activity=MainActivity" artifacts/android-gl-medium.log \
    && grep -Fq "UI_READY activity=MainActivity" artifacts/android-gl-medium.log \
    && grep -Fq "$READY_MARKER" artifacts/android-gl-medium.log \
    && grep -Fq "WINDOW_FOCUS hasFocus=true" artifacts/android-gl-medium.log; then
    MEDIUM_READY=1
    break
  fi
  sleep 1
done
if [[ "$MEDIUM_READY" != "1" ]]; then
  echo "Medium-density portrait did not render a focused Liquid Glass Activity." >&2
  cat artifacts/android-gl-medium.log >&2
  exit 1
fi
adb shell wm size > artifacts/android-medium-display-size.txt
adb shell wm density > artifacts/android-medium-display-density.txt
adb shell uiautomator dump /sdcard/liquid-glass-medium.xml >/dev/null
adb pull /sdcard/liquid-glass-medium.xml artifacts/android-window-medium.xml
adb shell screencap -p /sdcard/liquid-glass-android-medium.png
adb pull /sdcard/liquid-glass-android-medium.png artifacts/android-gles2-medium-density.png
python3 - <<'PY'
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

xml_path = Path("artifacts/android-window-medium.xml")
root = ET.parse(xml_path).getroot()
nodes = list(root.iter("node"))
package = "org.liquidglass.reference.debug"
app = [node for node in nodes if node.attrib.get("package") == package]
if not app or not any(n.attrib.get("text") == "Light, held in motion." for n in app):
    raise SystemExit("Medium-density capture does not show the Liquid Glass Activity.")
if root.attrib.get("rotation") not in {"0", "2"}:
    raise SystemExit("Medium-density capture is not in portrait orientation.")
png = Path("artifacts/android-gles2-medium-density.png").read_bytes()
if len(png) < 100000 or png[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("Medium-density capture is empty or not a PNG.")
width, height = struct.unpack(">II", png[16:24])
if height <= width:
    raise SystemExit(f"Medium-density screenshot is not portrait: {width}x{height}")
PY

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

# Landscape configuration: rotate the actual emulator display, then validate app configuration and capture.
adb shell settings put system accelerometer_rotation 1
adb shell wm user-rotation free
adb shell wm size 1280x720
adb shell wm density 160
adb emu rotate
sleep 2
adb shell am force-stop org.liquidglass.reference.debug
adb logcat -c
adb shell am start -n org.liquidglass.reference.debug/org.liquidglass.reference.MainActivity > artifacts/android-landscape-launch.txt
LANDSCAPE_READY=0
for attempt in $(seq 1 35); do
  adb logcat -d -s LiquidGlassDemo:I > artifacts/android-gl-landscape.log
  if grep -Fq "ACTIVITY_RESUMED activity=MainActivity" artifacts/android-gl-landscape.log \
    && grep -Fq "UI_READY activity=MainActivity" artifacts/android-gl-landscape.log \
    && grep -Fq "orientation=2" artifacts/android-gl-landscape.log \
    && grep -Fq "$READY_MARKER" artifacts/android-gl-landscape.log \
    && grep -Fq "WINDOW_FOCUS hasFocus=true" artifacts/android-gl-landscape.log; then
    LANDSCAPE_READY=1
    break
  fi
  sleep 1
done
if [[ "$LANDSCAPE_READY" != "1" ]]; then
  echo "Actual emulator landscape rotation did not produce a focused landscape Activity." >&2
  cat artifacts/android-gl-landscape.log >&2
  exit 1
fi
adb shell wm size > artifacts/android-landscape-display-size.txt
adb shell wm density > artifacts/android-landscape-display-density.txt
adb shell wm user-rotation > artifacts/android-landscape-user-rotation.txt
adb shell uiautomator dump /sdcard/liquid-glass-landscape.xml >/dev/null
adb pull /sdcard/liquid-glass-landscape.xml artifacts/android-window-landscape.xml
adb shell screencap -p /sdcard/liquid-glass-android-landscape.png
adb pull /sdcard/liquid-glass-android-landscape.png artifacts/android-gles2-landscape.png
python3 - <<'PY'
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

log = Path("artifacts/android-gl-landscape.log").read_text(encoding="utf-8")
match = re.search(r"UI_READY activity=MainActivity width=(\d+) height=(\d+) orientation=(\d+) screen_width_dp=(\d+) screen_height_dp=(\d+)", log)
if not match:
    raise SystemExit("Could not read the app's actual display configuration.")
root_width, root_height, orientation, screen_width_dp, screen_height_dp = map(int, match.groups())
if orientation != 2 or root_width <= root_height or screen_width_dp <= screen_height_dp:
    raise SystemExit(
        f"Activity is not laid out in landscape: root={root_width}x{root_height}, "
        f"orientation={orientation}, dp={screen_width_dp}x{screen_height_dp}"
    )

hierarchy = ET.parse("artifacts/android-window-landscape.xml").getroot()
if hierarchy.attrib.get("rotation") not in {"1", "3"}:
    raise SystemExit("UIAutomator did not confirm a 90/270 degree display rotation.")
nodes = list(hierarchy.iter("node"))
package = "org.liquidglass.reference.debug"
app = [node for node in nodes if node.attrib.get("package") == package]
if not app or not any(node.attrib.get("text") == "Light, held in motion." for node in app):
    raise SystemExit("Landscape capture does not show the Liquid Glass Activity.")

display = Path("artifacts/android-landscape-display-size.txt").read_text(encoding="utf-8")
if not re.search(r"Override size:\s*1280x720", display):
    raise SystemExit("WindowManager did not retain the requested 1280x720 landscape viewport.")
user_rotation = Path("artifacts/android-landscape-user-rotation.txt").read_text(encoding="utf-8")
if "free" not in user_rotation and not re.search(r"lock [13]", user_rotation):
    raise SystemExit("The emulator did not report a landscape user rotation.")

png = Path("artifacts/android-gles2-landscape.png").read_bytes()
if len(png) < 100000 or png[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("Landscape capture is empty or not a PNG.")
width, height = struct.unpack(">II", png[16:24])
if width <= height:
    raise SystemExit(f"Landscape screencap is not horizontal: {width}x{height}")
PY

# Restore defaults, unlock the emulator, and exercise four independent refractive SDF surfaces.
adb shell wm size reset
adb shell wm density reset
adb shell settings put system accelerometer_rotation 1
adb shell wm user-rotation lock 0
adb shell settings put system user_rotation 0
adb shell input keyevent KEYCODE_WAKEUP || true
adb shell wm dismiss-keyguard >/dev/null 2>&1 || true
sleep 3
adb shell am force-stop org.liquidglass.reference.debug
adb logcat -c
adb shell am start -n org.liquidglass.reference.debug/org.liquidglass.reference.MainActivity --ei extra_surfaces 3 > artifacts/android-multisurface-launch.txt
MULTI_READY=0
for attempt in $(seq 1 35); do
  adb logcat -d -s LiquidGlassDemo:I > artifacts/android-gl-multisurface.log
  if grep -Fq "SURFACE_COUNT main=1 additional=3 total=4" artifacts/android-gl-multisurface.log \
    && grep -Fq "$READY_MARKER" artifacts/android-gl-multisurface.log \
    && grep -Fq "ACTIVITY_RESUMED activity=MainActivity" artifacts/android-gl-multisurface.log \
    && grep -Fq "UI_READY activity=MainActivity" artifacts/android-gl-multisurface.log \
    && grep -Fq "WINDOW_FOCUS hasFocus=true" artifacts/android-gl-multisurface.log; then
    MULTI_READY=1
    break
  fi
  sleep 1
done
if [[ "$MULTI_READY" != "1" ]]; then
  echo "Four-surface workload did not reach a focused, laid-out Activity." >&2
  cat artifacts/android-gl-multisurface.log >&2
  exit 1
fi

adb shell dumpsys activity activities > artifacts/android-multisurface-activities.txt
adb shell uiautomator dump /sdcard/liquid-glass-multisurface.xml >/dev/null
adb pull /sdcard/liquid-glass-multisurface.xml artifacts/android-window-multisurface.xml
python3 - <<'PY'
import xml.etree.ElementTree as ET

root = ET.parse("artifacts/android-window-multisurface.xml").getroot()
nodes = list(root.iter("node"))
package = "org.liquidglass.reference.debug"
app_nodes = [node for node in nodes if node.attrib.get("package") == package]
if not app_nodes:
    raise SystemExit("The four-surface capture is not displaying the Liquid Glass app window.")
descriptions = {node.attrib.get("content-desc", "") for node in app_nodes}
required = {"Connect the liquid lens", "Pause optical preview", "Refraction strength"}
missing = required - descriptions
if missing:
    raise SystemExit("The four-surface app view is incomplete; missing accessibility nodes: " + ", ".join(sorted(missing)))
texts = {node.attrib.get("text", "") for node in app_nodes}
if "Light, held in motion." not in texts:
    raise SystemExit("The four-surface capture does not contain the Liquid Glass Activity title.")
PY

adb shell screencap -p /sdcard/liquid-glass-android-four-surfaces.png
adb pull /sdcard/liquid-glass-android-four-surfaces.png artifacts/android-gles2-four-surfaces.png
MULTI_CAPTURE_BYTES="$(wc -c < artifacts/android-gles2-four-surfaces.png)"
if [[ "$MULTI_CAPTURE_BYTES" -lt 100000 ]]; then
  echo "Four-surface screenshot is too small to contain the rendered app scene: $MULTI_CAPTURE_BYTES bytes." >&2
  exit 1
fi

grep -Fq "$READY_MARKER" artifacts/android-gl.log
test -s artifacts/android-gles2-l3.png
test -s artifacts/android-gles2-medium-density.png
test -s artifacts/android-gles2-landscape.png
test -s artifacts/android-gles2-four-surfaces.png
test -s artifacts/android-accessibility-settings.log
